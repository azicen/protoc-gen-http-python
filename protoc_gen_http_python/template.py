from typing import List
from jinja2 import Template


class TypeDesc:
    pascal_case_name: str
    snake_case_name: str
    alias: str  # api_dot_helloworld_dot_helloworld__pb2.TypeName
    use: str  # from api.helloworld import helloworld_pb2 as api_dot_helloworld_dot_helloworld__pb2


class MethodDesc:
    # method
    pascal_case_name: str
    snake_case_name: str
    request: TypeDesc
    reply: TypeDesc
    comment: List[str]
    # http
    path: str
    method: str
    has_vars: bool
    has_body: bool
    body: str
    body_type: TypeDesc


class ServiceDesc:
    entity_package: str  # hello_world_pd2
    pascal_case_name: str  # HelloWorld
    snake_case_name: str  # hello_world
    metadata: str  # api/helloworld/helloworld.proto
    comment: List[str]
    uses: List[str]
    methods: List[MethodDesc]


def execute(services: List[ServiceDesc], uses: List[str]) -> str:
    template = Template(http_template)
    return template.render(services=services, uses=uses)


http_template = '''# Generated by the protoc-gen-py-http protocol compiler plugin. DO NOT EDIT!
"""Server classes corresponding to protoc_gen_http_python-defined services."""
from typing import Callable as _Callable, Any as _Any, Dict as _Dict
from google.protobuf.message import Message as _Message
from google.protobuf.json_format import ParseDict as _ParseDict

{%- for use in uses %}
{{ use }}
{%- endfor %}


{%- for service in services %}


class {{ service.pascal_case_name }}Servicer(object):
    """
    {% for comment in service.comment -%}
    {{ comment }}
    {% endfor -%}
    """
    {%- for method in service.methods %}

    def {{ method.snake_case_name }}(
            self,
            request: {{ method.request.alias }}
    ) -> {{ method.reply.alias }}:
        """
        {% for comment in method.comment -%}
        {{ comment }}
        {% endfor -%}
        """
        raise NotImplementedError('Method not implemented!')
    {%- endfor %}


def register_{{ service.snake_case_name }}_http_server(
        register: _Callable[[str, str, _Callable[[_Dict[str, _Any], bytes], _Any]], _Any],
        servicer: {{ service.pascal_case_name }}Servicer,
        parse_request: _Callable[[_Message, bytes], _Message],
        parse_reply: _Callable[[_Message], bytes]):
    service = {{ service.pascal_case_name }}(servicer, parse_request, parse_reply)
    {%- for method in service.methods %}
    register("{{ method.method }}", "{{ method.path }}", service.{{ method.snake_case_name }})
    {%- endfor %}


class {{ service.pascal_case_name }}(object):
    servicer: {{ service.pascal_case_name }}Servicer
    parse_request: _Callable[[_Message, bytes], _Message]
    parse_reply: _Callable[[_Message], _Any]

    def __init__(
            self,
            servicer: {{ service.pascal_case_name }}Servicer,
            parse_request: _Callable[[_Message, bytes], _Message],
            parse_reply: _Callable[[_Message], _Any]):
        self.servicer = servicer
        self.parse_request = parse_request
        self.parse_reply = parse_reply

    {%- for method in service.methods %}
    
    def {{ method.snake_case_name }}(self, {{- ' ' -}}
            {%- if method.has_vars %}path_params{% else %}_{% endif %}: _Dict[str, _Any], {{- ' ' -}}
            {%- if method.has_body %}body{% else %}__{% endif %}: bytes):
        _request = {{ method.request.alias }}()
        {%- if method.has_vars %}
        _ParseDict(path_params, _request)
        {%- endif %}
        {%- if method.has_body %}
        {%- if method.body is not defined or method.body == "" %}
        _request = self.parse_request(_request, body)
        {%- else %}
        _request_body = {{ method.body_type.alias }}()
        _request_body = self.parse_request(_request_body, body)
        _request.{{ method.body }} = _request_body
        {%- endif %}
        {%- endif %}
        assert isinstance(_request, {{ method.request.alias }})
        _reply = self.servicer.{{ method.snake_case_name }}(_request)
        return self.parse_reply(_reply)
    {%- endfor %}

{%- endfor %}

'''
