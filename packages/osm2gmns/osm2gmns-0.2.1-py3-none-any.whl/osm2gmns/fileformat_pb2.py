# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fileformat.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='fileformat.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x10\x66ileformat.proto\"l\n\x04\x42lob\x12\x0b\n\x03raw\x18\x01 \x01(\x0c\x12\x10\n\x08raw_size\x18\x02 \x01(\x05\x12\x11\n\tzlib_data\x18\x03 \x01(\x0c\x12\x11\n\tlzma_data\x18\x04 \x01(\x0c\x12\x1f\n\x13OBSOLETE_bzip2_data\x18\x05 \x01(\x0c\x42\x02\x18\x01\"?\n\nBlobHeader\x12\x0c\n\x04type\x18\x01 \x02(\t\x12\x11\n\tindexdata\x18\x02 \x01(\x0c\x12\x10\n\x08\x64\x61tasize\x18\x03 \x02(\x05'
)




_BLOB = _descriptor.Descriptor(
  name='Blob',
  full_name='Blob',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='raw', full_name='Blob.raw', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='raw_size', full_name='Blob.raw_size', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='zlib_data', full_name='Blob.zlib_data', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lzma_data', full_name='Blob.lzma_data', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='OBSOLETE_bzip2_data', full_name='Blob.OBSOLETE_bzip2_data', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=20,
  serialized_end=128,
)


_BLOBHEADER = _descriptor.Descriptor(
  name='BlobHeader',
  full_name='BlobHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='BlobHeader.type', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='indexdata', full_name='BlobHeader.indexdata', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='datasize', full_name='BlobHeader.datasize', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=130,
  serialized_end=193,
)

DESCRIPTOR.message_types_by_name['Blob'] = _BLOB
DESCRIPTOR.message_types_by_name['BlobHeader'] = _BLOBHEADER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Blob = _reflection.GeneratedProtocolMessageType('Blob', (_message.Message,), {
  'DESCRIPTOR' : _BLOB,
  '__module__' : 'fileformat_pb2'
  # @@protoc_insertion_point(class_scope:Blob)
  })
_sym_db.RegisterMessage(Blob)

BlobHeader = _reflection.GeneratedProtocolMessageType('BlobHeader', (_message.Message,), {
  'DESCRIPTOR' : _BLOBHEADER,
  '__module__' : 'fileformat_pb2'
  # @@protoc_insertion_point(class_scope:BlobHeader)
  })
_sym_db.RegisterMessage(BlobHeader)


_BLOB.fields_by_name['OBSOLETE_bzip2_data']._options = None
# @@protoc_insertion_point(module_scope)
