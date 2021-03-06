# Gym Protocol

**Name:** gym

**Author**: fetchai

**Version**: 0.4.0

**Short Description**: A protocol for interacting with a gym connection.

**License**: Apache-2.0

## Description

This is a protocol for interacting with a gym connection.

## Specification

```yaml
---
name: gym
author: fetchai
version: 0.4.0
description: A protocol for interacting with a gym connection.
license: Apache-2.0
aea_version: '>=0.5.0, <0.6.0'
speech_acts:
  act:
    action: ct:AnyObject
    step_id: pt:int
  percept:
    step_id: pt:int
    observation: ct:AnyObject
    reward: pt:float
    done: pt:bool
    info: ct:AnyObject
  status:
    content: pt:dict[pt:str, pt:str]
  reset: {}
  close: {}
...
---
ct:AnyObject: |
  bytes any = 1;
...
---
initiation: [reset]
reply:
  reset: [status]
  status: [act, close, reset]
  act: [percept]
  percept: [act, close, reset]
  close: []
termination: [close]
roles: {agent, environment}
end_states: [successful]
...
```

## Links

* <a href="https://gym.openai.com" target=_blank>OpenAI Gym</a>