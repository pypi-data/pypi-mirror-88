# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cogneed-protos/ai/cogneed/api/common.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='cogneed-protos/ai/cogneed/api/common.proto',
  package='ai.cogneed.api',
  syntax='proto3',
  serialized_options=_b('\n\016ai.cogneed.apiP\001'),
  serialized_pb=_b('\n*cogneed-protos/ai/cogneed/api/common.proto\x12\x0e\x61i.cogneed.api\"\r\n\x0b\x41\x63kResponseB\x12\n\x0e\x61i.cogneed.apiP\x01\x62\x06proto3')
)




_ACKRESPONSE = _descriptor.Descriptor(
  name='AckResponse',
  full_name='ai.cogneed.api.AckResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
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
  serialized_end=75,
)

DESCRIPTOR.message_types_by_name['AckResponse'] = _ACKRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AckResponse = _reflection.GeneratedProtocolMessageType('AckResponse', (_message.Message,), dict(
  DESCRIPTOR = _ACKRESPONSE,
  __module__ = 'cogneed_protos.ai.cogneed.api.common_pb2'
  # @@protoc_insertion_point(class_scope:ai.cogneed.api.AckResponse)
  ))
_sym_db.RegisterMessage(AckResponse)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
