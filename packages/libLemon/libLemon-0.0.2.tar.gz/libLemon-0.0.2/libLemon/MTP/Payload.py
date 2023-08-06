#!/usr/bin/env python3

import json
from time import time
import libLemon.Utils.Logger as Logger
from libLemon.Utils.Const import ERROR_TYPE
from libLemon.Error.Error import NoTypeFoundError, SerializeError, DeserializeError


class Payload:
    def __init__(self, **entries):
        if '__annotations__' in type(self).__dict__:
            annotations = type(self).__dict__['__annotations__']
            for k, v in entries.items():
                if not k in annotations:
                    raise SerializeError('unknown attr name `%s` for class `%s`' % (k, self.__class__.__name__))
                
                if not isinstance(v, annotations[k]):
                    raise SerializeError('bad attr type `%s` (got %s, but %s expected) for class `%s`' % (k, type(v), annotations[k], self.__class__.__name__))
        self.__dict__.update(entries)


def serialize(payload: Payload) -> bytes:
    typee = ERROR_TYPE
    try:
        assert(isinstance(payload, Payload))
        typee = payload.__class__.__name__
        return json.dumps({ 
            'type': payload.__class__.__name__,
            'time': time(),
            'payload': payload.__dict__ 
        }).encode()
    except:
        raise SerializeError('failed to serialize object of type `%s`' % typee)

def deserialize(body: bytes, expected_types: list[type]) -> Payload:
    typee = ERROR_TYPE
    obj = json.loads(body.decode())
    try:
        for typee in expected_types:
            Logger.info('check ' + typee.__name__)
            if typee.__name__ == obj['type']:
                entries = obj['payload']
                payload = typee(**entries)
                assert(isinstance(payload, Payload))
                return payload
        raise NoTypeFoundError('no known type to deserialize for name `%s`' % obj['type'])
    except NoTypeFoundError:
        raise
    except:
        raise DeserializeError('failed to deserialize object of type `%s`' % typee)