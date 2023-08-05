# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grebble_flow/grpc/proto/app.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='grebble_flow/grpc/proto/app.proto',
  package='grebble_flow.grpc.proto',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n!grebble_flow/grpc/proto/app.proto\x12\x17grebble_flow.grpc.proto\"\x10\n\x0e\x41ppInfoRequest\"\x1d\n\rProcessorInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\"M\n\x0f\x41ppInfoResponse\x12:\n\nProcessors\x18\x01 \x03(\x0b\x32&.grebble_flow.grpc.proto.ProcessorInfo2e\n\x03\x41pp\x12^\n\x07\x41ppInfo\x12\'.grebble_flow.grpc.proto.AppInfoRequest\x1a(.grebble_flow.grpc.proto.AppInfoResponse\"\x00\x62\x06proto3'
)




_APPINFOREQUEST = _descriptor.Descriptor(
  name='AppInfoRequest',
  full_name='grebble_flow.grpc.proto.AppInfoRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=62,
  serialized_end=78,
)


_PROCESSORINFO = _descriptor.Descriptor(
  name='ProcessorInfo',
  full_name='grebble_flow.grpc.proto.ProcessorInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='grebble_flow.grpc.proto.ProcessorInfo.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=80,
  serialized_end=109,
)


_APPINFORESPONSE = _descriptor.Descriptor(
  name='AppInfoResponse',
  full_name='grebble_flow.grpc.proto.AppInfoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Processors', full_name='grebble_flow.grpc.proto.AppInfoResponse.Processors', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=111,
  serialized_end=188,
)

_APPINFORESPONSE.fields_by_name['Processors'].message_type = _PROCESSORINFO
DESCRIPTOR.message_types_by_name['AppInfoRequest'] = _APPINFOREQUEST
DESCRIPTOR.message_types_by_name['ProcessorInfo'] = _PROCESSORINFO
DESCRIPTOR.message_types_by_name['AppInfoResponse'] = _APPINFORESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AppInfoRequest = _reflection.GeneratedProtocolMessageType('AppInfoRequest', (_message.Message,), {
  'DESCRIPTOR' : _APPINFOREQUEST,
  '__module__' : 'grebble_flow.grpc.proto.app_pb2'
  # @@protoc_insertion_point(class_scope:grebble_flow.grpc.proto.AppInfoRequest)
  })
_sym_db.RegisterMessage(AppInfoRequest)

ProcessorInfo = _reflection.GeneratedProtocolMessageType('ProcessorInfo', (_message.Message,), {
  'DESCRIPTOR' : _PROCESSORINFO,
  '__module__' : 'grebble_flow.grpc.proto.app_pb2'
  # @@protoc_insertion_point(class_scope:grebble_flow.grpc.proto.ProcessorInfo)
  })
_sym_db.RegisterMessage(ProcessorInfo)

AppInfoResponse = _reflection.GeneratedProtocolMessageType('AppInfoResponse', (_message.Message,), {
  'DESCRIPTOR' : _APPINFORESPONSE,
  '__module__' : 'grebble_flow.grpc.proto.app_pb2'
  # @@protoc_insertion_point(class_scope:grebble_flow.grpc.proto.AppInfoResponse)
  })
_sym_db.RegisterMessage(AppInfoResponse)



_APP = _descriptor.ServiceDescriptor(
  name='App',
  full_name='grebble_flow.grpc.proto.App',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=190,
  serialized_end=291,
  methods=[
  _descriptor.MethodDescriptor(
    name='AppInfo',
    full_name='grebble_flow.grpc.proto.App.AppInfo',
    index=0,
    containing_service=None,
    input_type=_APPINFOREQUEST,
    output_type=_APPINFORESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_APP)

DESCRIPTOR.services_by_name['App'] = _APP

# @@protoc_insertion_point(module_scope)
