# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/cim/iec61970/base/wires/PerLengthImpedance.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.protobuf.cim.iec61970.base.wires import PerLengthLineParameter_pb2 as zepben_dot_protobuf_dot_cim_dot_iec61970_dot_base_dot_wires_dot_PerLengthLineParameter__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='zepben/protobuf/cim/iec61970/base/wires/PerLengthImpedance.proto',
  package='zepben.protobuf.cim.iec61970.base.wires',
  syntax='proto3',
  serialized_options=b'\n+com.zepben.protobuf.cim.iec61970.base.wiresP\001\252\002\'Zepben.Protobuf.CIM.IEC61970.Base.Wires',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n@zepben/protobuf/cim/iec61970/base/wires/PerLengthImpedance.proto\x12\'zepben.protobuf.cim.iec61970.base.wires\x1a\x44zepben/protobuf/cim/iec61970/base/wires/PerLengthLineParameter.proto\"a\n\x12PerLengthImpedance\x12K\n\x02lp\x18\x01 \x01(\x0b\x32?.zepben.protobuf.cim.iec61970.base.wires.PerLengthLineParameterBY\n+com.zepben.protobuf.cim.iec61970.base.wiresP\x01\xaa\x02\'Zepben.Protobuf.CIM.IEC61970.Base.Wiresb\x06proto3'
  ,
  dependencies=[zepben_dot_protobuf_dot_cim_dot_iec61970_dot_base_dot_wires_dot_PerLengthLineParameter__pb2.DESCRIPTOR,])




_PERLENGTHIMPEDANCE = _descriptor.Descriptor(
  name='PerLengthImpedance',
  full_name='zepben.protobuf.cim.iec61970.base.wires.PerLengthImpedance',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='lp', full_name='zepben.protobuf.cim.iec61970.base.wires.PerLengthImpedance.lp', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=179,
  serialized_end=276,
)

_PERLENGTHIMPEDANCE.fields_by_name['lp'].message_type = zepben_dot_protobuf_dot_cim_dot_iec61970_dot_base_dot_wires_dot_PerLengthLineParameter__pb2._PERLENGTHLINEPARAMETER
DESCRIPTOR.message_types_by_name['PerLengthImpedance'] = _PERLENGTHIMPEDANCE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PerLengthImpedance = _reflection.GeneratedProtocolMessageType('PerLengthImpedance', (_message.Message,), {
  'DESCRIPTOR' : _PERLENGTHIMPEDANCE,
  '__module__' : 'zepben.protobuf.cim.iec61970.base.wires.PerLengthImpedance_pb2'
  # @@protoc_insertion_point(class_scope:zepben.protobuf.cim.iec61970.base.wires.PerLengthImpedance)
  })
_sym_db.RegisterMessage(PerLengthImpedance)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
