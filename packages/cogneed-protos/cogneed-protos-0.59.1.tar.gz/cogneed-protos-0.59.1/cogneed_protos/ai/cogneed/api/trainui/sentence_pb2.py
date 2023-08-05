# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cogneed-protos/ai/cogneed/api/trainui/sentence.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from cogneed_protos.ai.cogneed.api import common_pb2 as cogneed__protos_dot_ai_dot_cogneed_dot_api_dot_common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='cogneed-protos/ai/cogneed/api/trainui/sentence.proto',
  package='ai.cogneed.api.trainui.sentence',
  syntax='proto3',
  serialized_options=_b('\n\037ai.cogneed.api.trainui.sentenceP\001'),
  serialized_pb=_b('\n4cogneed-protos/ai/cogneed/api/trainui/sentence.proto\x12\x1f\x61i.cogneed.api.trainui.sentence\x1a*cogneed-protos/ai/cogneed/api/common.proto\">\n\x06\x43reate\x12\x10\n\x08use_case\x18\x01 \x01(\t\x12\x14\n\x0ckeyword_uuid\x18\x02 \x01(\t\x12\x0c\n\x04text\x18\x03 \x01(\t\"\x14\n\x04Read\x12\x0c\n\x04uuid\x18\x01 \x01(\t\"S\n\x04List\x12\x10\n\x08use_case\x18\x01 \x01(\t\x12\x14\n\x0ckeyword_uuid\x18\x02 \x01(\t\x12\x0c\n\x04page\x18\x03 \x01(\x05\x12\x15\n\rrows_per_page\x18\x04 \x01(\x05\"\x16\n\x06\x44\x65lete\x12\x0c\n\x04uuid\x18\x01 \x01(\t\"f\n\x08Sentence\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x10\n\x08use_case\x18\x02 \x01(\t\x12\x14\n\x0ckeyword_uuid\x18\x03 \x01(\t\x12\x0c\n\x04text\x18\x04 \x01(\t\x12\x16\n\x0enum_recordings\x18\x05 \x01(\x05\"Y\n\x0cListResponse\x12\r\n\x05\x63ount\x18\x01 \x01(\x05\x12:\n\x07results\x18\x02 \x03(\x0b\x32).ai.cogneed.api.trainui.sentence.Sentence2\xbb\x03\n\x0fSentenceService\x12N\n\x06\x63reate\x12\'.ai.cogneed.api.trainui.sentence.Create\x1a\x1b.ai.cogneed.api.AckResponse\x12X\n\x04read\x12%.ai.cogneed.api.trainui.sentence.Read\x1a).ai.cogneed.api.trainui.sentence.Sentence\x12\\\n\x04list\x12%.ai.cogneed.api.trainui.sentence.List\x1a-.ai.cogneed.api.trainui.sentence.ListResponse\x12P\n\x06update\x12).ai.cogneed.api.trainui.sentence.Sentence\x1a\x1b.ai.cogneed.api.AckResponse\x12N\n\x06\x64\x65lete\x12\'.ai.cogneed.api.trainui.sentence.Delete\x1a\x1b.ai.cogneed.api.AckResponseB#\n\x1f\x61i.cogneed.api.trainui.sentenceP\x01\x62\x06proto3')
  ,
  dependencies=[cogneed__protos_dot_ai_dot_cogneed_dot_api_dot_common__pb2.DESCRIPTOR,])




_CREATE = _descriptor.Descriptor(
  name='Create',
  full_name='ai.cogneed.api.trainui.sentence.Create',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='use_case', full_name='ai.cogneed.api.trainui.sentence.Create.use_case', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='keyword_uuid', full_name='ai.cogneed.api.trainui.sentence.Create.keyword_uuid', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='text', full_name='ai.cogneed.api.trainui.sentence.Create.text', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=133,
  serialized_end=195,
)


_READ = _descriptor.Descriptor(
  name='Read',
  full_name='ai.cogneed.api.trainui.sentence.Read',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uuid', full_name='ai.cogneed.api.trainui.sentence.Read.uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=197,
  serialized_end=217,
)


_LIST = _descriptor.Descriptor(
  name='List',
  full_name='ai.cogneed.api.trainui.sentence.List',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='use_case', full_name='ai.cogneed.api.trainui.sentence.List.use_case', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='keyword_uuid', full_name='ai.cogneed.api.trainui.sentence.List.keyword_uuid', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='page', full_name='ai.cogneed.api.trainui.sentence.List.page', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rows_per_page', full_name='ai.cogneed.api.trainui.sentence.List.rows_per_page', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=219,
  serialized_end=302,
)


_DELETE = _descriptor.Descriptor(
  name='Delete',
  full_name='ai.cogneed.api.trainui.sentence.Delete',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uuid', full_name='ai.cogneed.api.trainui.sentence.Delete.uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=304,
  serialized_end=326,
)


_SENTENCE = _descriptor.Descriptor(
  name='Sentence',
  full_name='ai.cogneed.api.trainui.sentence.Sentence',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uuid', full_name='ai.cogneed.api.trainui.sentence.Sentence.uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='use_case', full_name='ai.cogneed.api.trainui.sentence.Sentence.use_case', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='keyword_uuid', full_name='ai.cogneed.api.trainui.sentence.Sentence.keyword_uuid', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='text', full_name='ai.cogneed.api.trainui.sentence.Sentence.text', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='num_recordings', full_name='ai.cogneed.api.trainui.sentence.Sentence.num_recordings', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=328,
  serialized_end=430,
)


_LISTRESPONSE = _descriptor.Descriptor(
  name='ListResponse',
  full_name='ai.cogneed.api.trainui.sentence.ListResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='count', full_name='ai.cogneed.api.trainui.sentence.ListResponse.count', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='results', full_name='ai.cogneed.api.trainui.sentence.ListResponse.results', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=432,
  serialized_end=521,
)

_LISTRESPONSE.fields_by_name['results'].message_type = _SENTENCE
DESCRIPTOR.message_types_by_name['Create'] = _CREATE
DESCRIPTOR.message_types_by_name['Read'] = _READ
DESCRIPTOR.message_types_by_name['List'] = _LIST
DESCRIPTOR.message_types_by_name['Delete'] = _DELETE
DESCRIPTOR.message_types_by_name['Sentence'] = _SENTENCE
DESCRIPTOR.message_types_by_name['ListResponse'] = _LISTRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Create = _reflection.GeneratedProtocolMessageType('Create', (_message.Message,), dict(
  DESCRIPTOR = _CREATE,
  __module__ = 'cogneed_protos.ai.cogneed.api.trainui.sentence_pb2'
  # @@protoc_insertion_point(class_scope:ai.cogneed.api.trainui.sentence.Create)
  ))
_sym_db.RegisterMessage(Create)

Read = _reflection.GeneratedProtocolMessageType('Read', (_message.Message,), dict(
  DESCRIPTOR = _READ,
  __module__ = 'cogneed_protos.ai.cogneed.api.trainui.sentence_pb2'
  # @@protoc_insertion_point(class_scope:ai.cogneed.api.trainui.sentence.Read)
  ))
_sym_db.RegisterMessage(Read)

List = _reflection.GeneratedProtocolMessageType('List', (_message.Message,), dict(
  DESCRIPTOR = _LIST,
  __module__ = 'cogneed_protos.ai.cogneed.api.trainui.sentence_pb2'
  # @@protoc_insertion_point(class_scope:ai.cogneed.api.trainui.sentence.List)
  ))
_sym_db.RegisterMessage(List)

Delete = _reflection.GeneratedProtocolMessageType('Delete', (_message.Message,), dict(
  DESCRIPTOR = _DELETE,
  __module__ = 'cogneed_protos.ai.cogneed.api.trainui.sentence_pb2'
  # @@protoc_insertion_point(class_scope:ai.cogneed.api.trainui.sentence.Delete)
  ))
_sym_db.RegisterMessage(Delete)

Sentence = _reflection.GeneratedProtocolMessageType('Sentence', (_message.Message,), dict(
  DESCRIPTOR = _SENTENCE,
  __module__ = 'cogneed_protos.ai.cogneed.api.trainui.sentence_pb2'
  # @@protoc_insertion_point(class_scope:ai.cogneed.api.trainui.sentence.Sentence)
  ))
_sym_db.RegisterMessage(Sentence)

ListResponse = _reflection.GeneratedProtocolMessageType('ListResponse', (_message.Message,), dict(
  DESCRIPTOR = _LISTRESPONSE,
  __module__ = 'cogneed_protos.ai.cogneed.api.trainui.sentence_pb2'
  # @@protoc_insertion_point(class_scope:ai.cogneed.api.trainui.sentence.ListResponse)
  ))
_sym_db.RegisterMessage(ListResponse)


DESCRIPTOR._options = None

_SENTENCESERVICE = _descriptor.ServiceDescriptor(
  name='SentenceService',
  full_name='ai.cogneed.api.trainui.sentence.SentenceService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=524,
  serialized_end=967,
  methods=[
  _descriptor.MethodDescriptor(
    name='create',
    full_name='ai.cogneed.api.trainui.sentence.SentenceService.create',
    index=0,
    containing_service=None,
    input_type=_CREATE,
    output_type=cogneed__protos_dot_ai_dot_cogneed_dot_api_dot_common__pb2._ACKRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='read',
    full_name='ai.cogneed.api.trainui.sentence.SentenceService.read',
    index=1,
    containing_service=None,
    input_type=_READ,
    output_type=_SENTENCE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='list',
    full_name='ai.cogneed.api.trainui.sentence.SentenceService.list',
    index=2,
    containing_service=None,
    input_type=_LIST,
    output_type=_LISTRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='update',
    full_name='ai.cogneed.api.trainui.sentence.SentenceService.update',
    index=3,
    containing_service=None,
    input_type=_SENTENCE,
    output_type=cogneed__protos_dot_ai_dot_cogneed_dot_api_dot_common__pb2._ACKRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='delete',
    full_name='ai.cogneed.api.trainui.sentence.SentenceService.delete',
    index=4,
    containing_service=None,
    input_type=_DELETE,
    output_type=cogneed__protos_dot_ai_dot_cogneed_dot_api_dot_common__pb2._ACKRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SENTENCESERVICE)

DESCRIPTOR.services_by_name['SentenceService'] = _SENTENCESERVICE

# @@protoc_insertion_point(module_scope)
