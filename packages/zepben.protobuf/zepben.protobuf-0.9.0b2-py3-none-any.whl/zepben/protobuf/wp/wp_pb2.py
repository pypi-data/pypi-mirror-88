# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/wp/wp.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='zepben/protobuf/wp/wp.proto',
  package='zepben.wp',
  syntax='proto3',
  serialized_options=b'\n\026com.zepben.protobuf.wpP\001\252\002\022Zepben.Protobuf.WP',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1bzepben/protobuf/wp/wp.proto\x12\tzepben.wp2\x11\n\x0fWeatherProducerB/\n\x16\x63om.zepben.protobuf.wpP\x01\xaa\x02\x12Zepben.Protobuf.WPb\x06proto3'
)



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None

_WEATHERPRODUCER = _descriptor.ServiceDescriptor(
  name='WeatherProducer',
  full_name='zepben.wp.WeatherProducer',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=42,
  serialized_end=59,
  methods=[
])
_sym_db.RegisterServiceDescriptor(_WEATHERPRODUCER)

DESCRIPTOR.services_by_name['WeatherProducer'] = _WEATHERPRODUCER

# @@protoc_insertion_point(module_scope)
