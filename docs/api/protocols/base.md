<a name="aea.protocols.base"></a>
# aea.protocols.base

This module contains the base message and serialization definition.

<a name="aea.protocols.base.Message"></a>
## Message Objects

```python
class Message()
```

This class implements a message.

<a name="aea.protocols.base.Message.Performative"></a>
## Performative Objects

```python
class Performative(Enum)
```

Performatives for the base message.

<a name="aea.protocols.base.Message.Performative.__str__"></a>
#### `__`str`__`

```python
 | __str__()
```

Get the string representation.

<a name="aea.protocols.base.Message.__init__"></a>
#### `__`init`__`

```python
 | __init__(body: Optional[Dict] = None, **kwargs)
```

Initialize a Message object.

**Arguments**:

- `body`: the dictionary of values to hold.
- `kwargs`: any additional value to add to the body. It will overwrite the body values.

<a name="aea.protocols.base.Message.has_sender"></a>
#### has`_`sender

```python
 | @property
 | has_sender() -> bool
```

Check if it has a sender.

<a name="aea.protocols.base.Message.sender"></a>
#### sender

```python
 | @property
 | sender() -> Address
```

Get the sender of the message in Address form.

:return the address

<a name="aea.protocols.base.Message.sender"></a>
#### sender

```python
 | @sender.setter
 | sender(sender: Address) -> None
```

Set the sender of the message.

<a name="aea.protocols.base.Message.has_to"></a>
#### has`_`to

```python
 | @property
 | has_to() -> bool
```

Check if it has a sender.

<a name="aea.protocols.base.Message.to"></a>
#### to

```python
 | @property
 | to() -> Address
```

Get address of receiver.

<a name="aea.protocols.base.Message.to"></a>
#### to

```python
 | @to.setter
 | to(to: Address) -> None
```

Set address of receiver.

<a name="aea.protocols.base.Message.has_counterparty"></a>
#### has`_`counterparty

```python
 | @property
 | has_counterparty() -> bool
```

Check if the counterparty is set.

<a name="aea.protocols.base.Message.counterparty"></a>
#### counterparty

```python
 | @property
 | counterparty() -> Address
```

Get the counterparty of the message in Address form.

:return the address

<a name="aea.protocols.base.Message.counterparty"></a>
#### counterparty

```python
 | @counterparty.setter
 | counterparty(counterparty: Address) -> None
```

Set the counterparty of the message.

<a name="aea.protocols.base.Message.is_incoming"></a>
#### is`_`incoming

```python
 | @property
 | is_incoming() -> bool
```

Get the is_incoming value of the message.

:return whether the message is incoming or is out going

<a name="aea.protocols.base.Message.is_incoming"></a>
#### is`_`incoming

```python
 | @is_incoming.setter
 | is_incoming(is_incoming: bool) -> None
```

Set the is_incoming of the message.

<a name="aea.protocols.base.Message.body"></a>
#### body

```python
 | @property
 | body() -> Dict
```

Get the body of the message (in dictionary form).

**Returns**:

the body

<a name="aea.protocols.base.Message.body"></a>
#### body

```python
 | @body.setter
 | body(body: Dict) -> None
```

Set the body of hte message.

**Arguments**:

- `body`: the body.

**Returns**:

None

<a name="aea.protocols.base.Message.dialogue_reference"></a>
#### dialogue`_`reference

```python
 | @property
 | dialogue_reference() -> Tuple[str, str]
```

Get the dialogue_reference of the message.

<a name="aea.protocols.base.Message.message_id"></a>
#### message`_`id

```python
 | @property
 | message_id() -> int
```

Get the message_id of the message.

<a name="aea.protocols.base.Message.performative"></a>
#### performative

```python
 | @property
 | performative() -> "Performative"
```

Get the performative of the message.

<a name="aea.protocols.base.Message.target"></a>
#### target

```python
 | @property
 | target() -> int
```

Get the target of the message.

<a name="aea.protocols.base.Message.set"></a>
#### set

```python
 | set(key: str, value: Any) -> None
```

Set key and value pair.

**Arguments**:

- `key`: the key.
- `value`: the value.

**Returns**:

None

<a name="aea.protocols.base.Message.get"></a>
#### get

```python
 | get(key: str) -> Optional[Any]
```

Get value for key.

<a name="aea.protocols.base.Message.unset"></a>
#### unset

```python
 | unset(key: str) -> None
```

Unset valye for key.

<a name="aea.protocols.base.Message.is_set"></a>
#### is`_`set

```python
 | is_set(key: str) -> bool
```

Check value is set for key.

<a name="aea.protocols.base.Message.__eq__"></a>
#### `__`eq`__`

```python
 | __eq__(other)
```

Compare with another object.

<a name="aea.protocols.base.Message.__str__"></a>
#### `__`str`__`

```python
 | __str__()
```

Get the string representation of the message.

<a name="aea.protocols.base.Message.encode"></a>
#### encode

```python
 | encode() -> bytes
```

Encode the message.

<a name="aea.protocols.base.Encoder"></a>
## Encoder Objects

```python
class Encoder(ABC)
```

Encoder interface.

<a name="aea.protocols.base.Encoder.encode"></a>
#### encode

```python
 | @staticmethod
 | @abstractmethod
 | encode(msg: Message) -> bytes
```

Encode a message.

**Arguments**:

- `msg`: the message to be encoded.

**Returns**:

the encoded message.

<a name="aea.protocols.base.Decoder"></a>
## Decoder Objects

```python
class Decoder(ABC)
```

Decoder interface.

<a name="aea.protocols.base.Decoder.decode"></a>
#### decode

```python
 | @staticmethod
 | @abstractmethod
 | decode(obj: bytes) -> Message
```

Decode a message.

**Arguments**:

- `obj`: the sequence of bytes to be decoded.

**Returns**:

the decoded message.

<a name="aea.protocols.base.Serializer"></a>
## Serializer Objects

```python
class Serializer(Encoder,  Decoder,  ABC)
```

The implementations of this class defines a serialization layer for a protocol.

<a name="aea.protocols.base.ProtobufSerializer"></a>
## ProtobufSerializer Objects

```python
class ProtobufSerializer(Serializer)
```

Default Protobuf serializer.

It assumes that the Message contains a JSON-serializable body.

<a name="aea.protocols.base.ProtobufSerializer.encode"></a>
#### encode

```python
 | @staticmethod
 | encode(msg: Message) -> bytes
```

Encode a message into bytes using Protobuf.

<a name="aea.protocols.base.ProtobufSerializer.decode"></a>
#### decode

```python
 | @staticmethod
 | decode(obj: bytes) -> Message
```

Decode bytes into a message using Protobuf.

<a name="aea.protocols.base.JSONSerializer"></a>
## JSONSerializer Objects

```python
class JSONSerializer(Serializer)
```

Default serialization in JSON for the Message object.

It assumes that the Message contains a JSON-serializable body.

<a name="aea.protocols.base.JSONSerializer.encode"></a>
#### encode

```python
 | @staticmethod
 | encode(msg: Message) -> bytes
```

Encode a message into bytes using JSON format.

**Arguments**:

- `msg`: the message to be encoded.

**Returns**:

the serialized message.

<a name="aea.protocols.base.JSONSerializer.decode"></a>
#### decode

```python
 | @staticmethod
 | decode(obj: bytes) -> Message
```

Decode bytes into a message using JSON.

**Arguments**:

- `obj`: the serialized message.

**Returns**:

the decoded message.

<a name="aea.protocols.base.Protocol"></a>
## Protocol Objects

```python
class Protocol(Component)
```

This class implements a specifications for a protocol.

It includes a serializer to encode/decode a message.

<a name="aea.protocols.base.Protocol.__init__"></a>
#### `__`init`__`

```python
 | __init__(configuration: ProtocolConfig, message_class: Type[Message], **kwargs)
```

Initialize the protocol manager.

**Arguments**:

- `configuration`: the protocol configurations.
- `message_class`: the message class.

<a name="aea.protocols.base.Protocol.serializer"></a>
#### serializer

```python
 | @property
 | serializer() -> Type[Serializer]
```

Get the serializer.

<a name="aea.protocols.base.Protocol.from_dir"></a>
#### from`_`dir

```python
 | @classmethod
 | from_dir(cls, directory: str, **kwargs) -> "Protocol"
```

Load the protocol from a directory.

**Arguments**:

- `directory`: the directory to the skill package.

**Returns**:

the protocol object.

<a name="aea.protocols.base.Protocol.from_config"></a>
#### from`_`config

```python
 | @classmethod
 | from_config(cls, configuration: ProtocolConfig, **kwargs) -> "Protocol"
```

Load the protocol from configuration.

**Arguments**:

- `configuration`: the protocol configuration.

**Returns**:

the protocol object.

