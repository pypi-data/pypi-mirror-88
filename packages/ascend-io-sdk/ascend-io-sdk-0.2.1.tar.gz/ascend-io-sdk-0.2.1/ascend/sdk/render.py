"""Utility functions to download Ascend resource definitions."""

import glog
from google.protobuf import descriptor
from google.protobuf.message import Message as ProtoMessage
import jinja2
import networkx as nx
import os
import pathlib
from typing import Dict, List, Optional, Tuple

from ascend.sdk.applier import _component_id_map_from_list
from ascend.sdk.builder import dataflow_from_proto, data_service_from_proto
from ascend.sdk.client import Client
from ascend.sdk.definitions import Component, Dataflow, DataService, Definition, Transform


class InlineCode:
  """ Represents the result of extraction of inline code from a component - such as
  a sql statement or PySpark code. Contains all of the metadata needed to render
  a component definition, with the inline code written to a separate file, and a reference
  to this code stored in the component.
  """
  def __init__(self, code: str, component_attribute: str, resource_path: str, base_path: str):
    """
    Parameters:
    - code: inline code
    - component_attribute: name of the attribute in the component protobuf definition that
    contains the inline code
    - resource_path: file path to which inline code is written
    - base_path: base path of dataflow or data service resource definition
    """
    self.code = code
    self.resource_path = resource_path
    self.component_attribute = component_attribute
    self._rel_path = os.path.relpath(os.path.realpath(resource_path), os.path.realpath(base_path))

  def loader(self) -> str:
    return f'''pathlib.Path(os.path.join(os.path.dirname(os.path.realpath(__file__)), "{self._rel_path}")).read_text()'''


def download_dataflow(client: Client,
                      data_service_id: str,
                      dataflow_id: str,
                      hostname: str,
                      resource_base_path: str = "."):
  """
  Downloads a Dataflow and writes its definition to a file named `{dataflow_id}.py` under
  `resource_base_path`. Inline code for PySpark and SQL Transforms are written as separate
  files to a sub-folder - `resource_base_path`/`{dataflow_id}`/ with the file names derived
  from the id of the component to which the code belongs. Raises a `ValueError` if
  `resource_base_path` does not exist.

  Parameters:
  - client: SDK client
  - data_service_id: DataService id
  - dataflow_id: Dataflow id
  - hostname: Ascend hostname
  - resource_base_path: path to which Dataflow definition and resource files
  are written
  """
  if not os.path.isdir(resource_base_path):
    raise ValueError(f"Specified resource path ({resource_base_path}) must be a directory")

  df_proto = client.get_dataflow(data_service_id=data_service_id, dataflow_id=dataflow_id).data
  dataflow = dataflow_from_proto(client, data_service_id, df_proto)

  dataflow_resource_path = os.path.join(resource_base_path, f"{dataflow.id}")
  dataflow_path = os.path.join(resource_base_path, f"{dataflow.id}.py")
  glog.info(f"Writing dataflow definition to ({dataflow_path})"
            f" and dataflow resource files to ({dataflow_resource_path})")

  pathlib.Path(dataflow_resource_path).mkdir(parents=True, exist_ok=True)

  rendered_dataflow, inline_code_list = render_dataflow(data_service_id, dataflow, hostname,
                                                        dataflow_resource_path, resource_base_path)
  for inline_code in inline_code_list:
    with open(inline_code.resource_path, "w") as f:
      f.write(inline_code.code)

  with open(dataflow_path, "w") as f:
    f.write(rendered_dataflow)


def download_data_service(client: Client,
                          data_service_id: str,
                          hostname: str,
                          resource_base_path: str = "."):
  """
  Downloads a DataService and writes its definition to a file named `{data_service_id}.py`
  under `resource_base_path`. Inline code for PySpark and SQL Transforms are written as separate
  files to sub-folders - `resource_base_path`/`{dataflow_id}`/ with the file name derived from
  the id of the component to which the code belongs. Raises `ValueError` if `resource_base_path`
  does not exist.

  Parameters:
  - client: SDK client
  - data_service_id: DataService id
  - hostname: Ascend hostname
  - resource_base_path: base path to which DataService definition and resource
  files are written
  """
  if not os.path.isdir(resource_base_path):
    raise ValueError(f"Specified resource path ({resource_base_path}) must be a directory")

  ds_proto = client.get_data_service(data_service_id=data_service_id).data
  data_service = data_service_from_proto(client, ds_proto)

  data_service_path = os.path.join(resource_base_path, f"{data_service.id}.py")
  dataflow_resource_paths = [
      os.path.join(resource_base_path, f"{dataflow.id}") for dataflow in data_service.dataflows
  ]
  glog.info(f"Writing data service definition to ({data_service_path})"
            f" and dataflow resource files to ({','.join(dataflow_resource_paths)})")

  for path in dataflow_resource_paths:
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

  rendered_data_service, inline_code_list = render_data_service(data_service, hostname,
                                                                resource_base_path)
  for inline_code in inline_code_list:
    with open(inline_code.resource_path, "w") as f:
      f.write(inline_code.code)

  with open(data_service_path, "w") as f:
    f.write(rendered_data_service)


def render_dataflow(data_service_id: str, dataflow: Dataflow, hostname: str, resource_path: str,
                    base_path: str) -> Tuple[str, List[InlineCode]]:
  inline_code_list: List[InlineCode] = []
  inline_code_map: Dict[Tuple[str, str], InlineCode] = {}

  for component in dataflow.components:
    ic = _inline_code_for(component, resource_path, base_path)
    if ic:
      inline_code_map[(dataflow.id, component.id)] = ic
      inline_code_list.append(ic)

  env = _jinja_env()
  tmpl = env.get_template("dataflow.jinja")
  rendered = tmpl.render(data_service_id=data_service_id,
                         dataflow=dataflow,
                         hostname=hostname,
                         renderer=_render_definition,
                         proto_mods=_proto_mods,
                         gmod_classes=_gmod_classes,
                         ordered_components=_components_ordered_by_dependency,
                         inline_code_map=inline_code_map,
                         classname_map=_classname_map())
  return rendered, inline_code_list


def render_data_service(data_service: DataService, hostname: str, resource_path: str) -> str:
  inline_code_list: List[InlineCode] = []
  inline_code_map: Dict[Tuple[str, str], InlineCode] = {}

  for dataflow in data_service.dataflows:
    dataflow_resource_path = os.path.join(resource_path, f"{dataflow.id}")
    for component in dataflow.components:
      ic = _inline_code_for(component, dataflow_resource_path, resource_path)
      if ic:
        inline_code_map[(dataflow.id, component.id)] = ic
        inline_code_list.append(ic)

  env = _jinja_env()
  tmpl = env.get_template("data_service.jinja")
  rendered = tmpl.render(data_service=data_service,
                         hostname=hostname,
                         renderer=_render_definition,
                         proto_mods=_proto_mods,
                         gmod_classes=_gmod_classes,
                         ordered_components=_components_ordered_by_dependency,
                         inline_code_map=inline_code_map,
                         classname_map=_classname_map())
  return rendered, inline_code_list


_proto_mods = [
    "ascend", "component", "content_encoding", "core", "expression", "format", "function", "io",
    "operator", "pattern", "schema", "text"
]

_gmod_classes = [("google.protobuf.wrappers_pb2", "DoubleValue"),
                 ("google.protobuf.wrappers_pb2", "Int64Value"),
                 ("google.protobuf.duration_pb2", "Duration"),
                 ("google.protobuf.timestamp_pb2", "Timestamp"),
                 ("google.protobuf.empty_pb2", "Empty")]


def _classname_map() -> dict:
  classname_map: dict = {}

  for defclass in [
      'DataService', 'Dataflow', 'ReadConnector', 'WriteConnector', 'Transform', 'ComponentGroup',
      'DataFeed', 'DataFeedConnector'
  ]:
    classname_map[defclass] = f"definitions.{defclass}"

  for _, cls in _gmod_classes:
    classname_map[f"google.protobuf.{cls}"] = cls

  return classname_map


def _inline_code_for(component: Component, resource_path_prefix: str,
                     base_path: str) -> Optional[InlineCode]:
  if isinstance(component, Transform) and component.operator:
    if component.operator.HasField(
        "spark_function") and component.operator.spark_function.executable.code.source.HasField(
            "inline"):
      return InlineCode(code=component.operator.spark_function.executable.code.source.inline,
                        resource_path=os.path.join(resource_path_prefix, f"{component.id}.py"),
                        base_path=base_path,
                        component_attribute="inline")
    elif component.operator.HasField("sql_query"):
      return InlineCode(code=component.operator.sql_query.sql,
                        resource_path=os.path.join(resource_path_prefix, f"{component.id}.sql"),
                        base_path=base_path,
                        component_attribute="sql")
    else:
      return None
  else:
    return None


def _jinja_env():
  module_dir = os.path.dirname(os.path.abspath(__file__))
  template_dir = os.path.join(module_dir, "templates")
  return jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                            trim_blocks=True,
                            lstrip_blocks=True)


def _render_definition(val: Definition,
                       indent=0,
                       classname_map: dict = {},
                       attribute_overrides: dict = {}):
  cls = classname_map.get(val.classname(), val.classname())
  tmpl = jinja2.Template('''{{cls}}(
{% for k, v in vars(val).items() %}\
{% if attribute_overrides.get(k) %}\
{{_spaces_for(indent+2)}}{{k}}=\
{{attribute_overrides.get(k)}},\n\
{% else %}\
{{_spaces_for(indent+2)}}{{k}}=\
{{_render_value(v, indent+2, classname_map, attribute_overrides)}},\n\
{% endif %}\
{% endfor %}\
{{_spaces_for(indent)}})''')
  return tmpl.render(val=val,
                     vars=vars,
                     _render_value=_render_value,
                     _spaces_for=_spaces_for,
                     indent=indent,
                     classname_map=classname_map,
                     attribute_overrides=attribute_overrides,
                     cls=cls)


def _render_value(val, indent=0, classname_map: dict = {}, attribute_overrides: dict = {}):
  """ Renders values in Python definition form. Support is limited to
  resource definitions, proto messages, and native types.
  """
  if isinstance(val, list):
    return _render_array(val, indent, classname_map, attribute_overrides)
  elif isinstance(val, dict):
    return _render_map(val, indent, classname_map, attribute_overrides)
  elif isinstance(val, ProtoMessage):
    return _render_message(val, indent, classname_map, attribute_overrides)
  elif isinstance(val, Definition):
    return _render_definition(val, indent, classname_map, attribute_overrides)
  elif isinstance(val, str):
    return f"'''{val}'''"
  else:
    return val


def _render_array(arr, indent=0, classname_map: dict = {}, attribute_overrides: dict = {}):
  tmpl = jinja2.Template('''[
{% for v in arr %}\
{{_spaces_for(indent+2)}}{{ _render_value(v, indent+2, classname_map, attribute_overrides) }},\n\
{% endfor %}\
{{_spaces_for(indent)}}]''')
  return tmpl.render(arr=arr,
                     _render_value=_render_value,
                     _spaces_for=_spaces_for,
                     indent=indent,
                     classname_map=classname_map,
                     attribute_overrides=attribute_overrides)


def _render_map(mp, indent=0, classname_map: dict = {}, attribute_overrides: dict = {}):
  tmpl = jinja2.Template('''{
{% for k, v in mp.items() %}\
{{_spaces_for(indent+2)}}{{_render_value(k, indent+2, classname_map, attribute_overrides)}}: \
{{ _render_value(v, indent+2, classname_map, attribute_overrides) }},\n\
{% endfor %}\
{{_spaces_for(indent)}}}''')
  return tmpl.render(mp=mp,
                     _render_value=_render_value,
                     _spaces_for=_spaces_for,
                     indent=indent,
                     classname_map=classname_map,
                     attribute_overrides=attribute_overrides)


def _render_message(message: ProtoMessage,
                    indent=0,
                    classname_map: dict = {},
                    attribute_overrides: dict = {}):
  def render_message_field(field_descriptor, val, indent):
    if field_descriptor.label == descriptor.FieldDescriptor.LABEL_REPEATED:
      if hasattr(val, 'items'):
        return _render_map(val, indent, classname_map, attribute_overrides)
      else:
        return _render_array(val, indent, classname_map, attribute_overrides)
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_MESSAGE:
      return _render_message(val, indent, classname_map, attribute_overrides)
    elif field_descriptor.type == descriptor.FieldDescriptor.TYPE_STRING:
      return f"'''{val}'''"
    else:
      return val

  cls = message.DESCRIPTOR.full_name
  cls = classname_map.get(cls, cls)
  tmpl = jinja2.Template('''{{cls}}(
{% for field in message.ListFields() %}\
{{ _spaces_for(indent+2) }}{{ field[0].name }}=\
{{ attribute_overrides.get(field[0].name, render_message_field(field[0], field[1], indent+2)) }},\n\
{% endfor %}\
{{_spaces_for(indent)}})''')
  return tmpl.render(message=message,
                     cls=cls,
                     render_message_field=render_message_field,
                     _spaces_for=_spaces_for,
                     indent=indent,
                     attribute_overrides=attribute_overrides)


def _spaces_for(indent):
  return " " * indent


def _components_ordered_by_dependency(components: List[Component]) -> List[Component]:
  ordered: List[Component] = []

  id_to_component = _component_id_map_from_list(components)
  g = nx.DiGraph()
  for component in components:
    g.add_node(component.id)
    for dep in component.dependencies():
      g.add_edge(component.id, dep)

  for component_id in reversed(list(nx.topological_sort(g))):
    component = id_to_component[component_id]
    ordered.append(component)

  return ordered
