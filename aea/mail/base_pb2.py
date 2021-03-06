# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: base.proto

import sys

_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode("latin1"))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor.FileDescriptor(
    name="base.proto",
    package="fetch.aea",
    syntax="proto3",
    serialized_options=None,
    serialized_pb=_b(
        '\n\nbase.proto\x12\tfetch.aea"Y\n\x08\x45nvelope\x12\n\n\x02to\x18\x01 \x01(\t\x12\x0e\n\x06sender\x18\x02 \x01(\t\x12\x13\n\x0bprotocol_id\x18\x03 \x01(\t\x12\x0f\n\x07message\x18\x04 \x01(\x0c\x12\x0b\n\x03uri\x18\x05 \x01(\tb\x06proto3'
    ),
)


_ENVELOPE = _descriptor.Descriptor(
    name="Envelope",
    full_name="fetch.aea.Envelope",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="to",
            full_name="fetch.aea.Envelope.to",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="sender",
            full_name="fetch.aea.Envelope.sender",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="protocol_id",
            full_name="fetch.aea.Envelope.protocol_id",
            index=2,
            number=3,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="message",
            full_name="fetch.aea.Envelope.message",
            index=3,
            number=4,
            type=12,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b(""),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="uri",
            full_name="fetch.aea.Envelope.uri",
            index=4,
            number=5,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=_b("").decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=25,
    serialized_end=114,
)

DESCRIPTOR.message_types_by_name["Envelope"] = _ENVELOPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Envelope = _reflection.GeneratedProtocolMessageType(
    "Envelope",
    (_message.Message,),
    dict(
        DESCRIPTOR=_ENVELOPE,
        __module__="base_pb2"
        # @@protoc_insertion_point(class_scope:fetch.aea.Envelope)
    ),
)
_sym_db.RegisterMessage(Envelope)


# @@protoc_insertion_point(module_scope)
