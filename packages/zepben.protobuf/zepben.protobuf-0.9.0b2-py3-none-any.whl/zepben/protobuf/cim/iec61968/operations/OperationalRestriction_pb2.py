# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/cim/iec61968/operations/OperationalRestriction.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.protobuf.cim.iec61968.common import Document_pb2 as zepben_dot_protobuf_dot_cim_dot_iec61968_dot_common_dot_Document__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='zepben/protobuf/cim/iec61968/operations/OperationalRestriction.proto',
  package='zepben.protobuf.cim.iec61968.operations',
  syntax='proto3',
  serialized_options=b'\n+com.zepben.protobuf.cim.iec61968.operationsP\001\252\002\'Zepben.Protobuf.CIM.IEC61968.Operations',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nDzepben/protobuf/cim/iec61968/operations/OperationalRestriction.proto\x12\'zepben.protobuf.cim.iec61968.operations\x1a\x32zepben/protobuf/cim/iec61968/common/Document.proto\"l\n\x16OperationalRestriction\x12:\n\x03\x64oc\x18\x01 \x01(\x0b\x32-.zepben.protobuf.cim.iec61968.common.Document\x12\x16\n\x0e\x65quipmentMRIDs\x18\x02 \x03(\tBY\n+com.zepben.protobuf.cim.iec61968.operationsP\x01\xaa\x02\'Zepben.Protobuf.CIM.IEC61968.Operationsb\x06proto3'
  ,
  dependencies=[zepben_dot_protobuf_dot_cim_dot_iec61968_dot_common_dot_Document__pb2.DESCRIPTOR,])




_OPERATIONALRESTRICTION = _descriptor.Descriptor(
  name='OperationalRestriction',
  full_name='zepben.protobuf.cim.iec61968.operations.OperationalRestriction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='doc', full_name='zepben.protobuf.cim.iec61968.operations.OperationalRestriction.doc', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='equipmentMRIDs', full_name='zepben.protobuf.cim.iec61968.operations.OperationalRestriction.equipmentMRIDs', index=1,
      number=2, type=9, cpp_type=9, label=3,
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
  serialized_start=165,
  serialized_end=273,
)

_OPERATIONALRESTRICTION.fields_by_name['doc'].message_type = zepben_dot_protobuf_dot_cim_dot_iec61968_dot_common_dot_Document__pb2._DOCUMENT
DESCRIPTOR.message_types_by_name['OperationalRestriction'] = _OPERATIONALRESTRICTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

OperationalRestriction = _reflection.GeneratedProtocolMessageType('OperationalRestriction', (_message.Message,), {
  'DESCRIPTOR' : _OPERATIONALRESTRICTION,
  '__module__' : 'zepben.protobuf.cim.iec61968.operations.OperationalRestriction_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.cim.iec61968.operations.OperationalRestriction)
  })
_sym_db.RegisterMessage(OperationalRestriction)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
