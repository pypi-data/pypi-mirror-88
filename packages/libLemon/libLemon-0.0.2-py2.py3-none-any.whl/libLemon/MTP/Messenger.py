#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from libLemon.Error.Error import NoTypeFoundError
import libLemon.Utils.Logger as Logger
from libLemon.MTP import EMQ
from libLemon.Utils.Const import FROM_TO_CONNECTOR, UNKNOWN_TYPE
from libLemon.MTP.Payload import Payload, deserialize, serialize

class Messenger:

    _client: mqtt.Client

    _send_topic: str
    _recv_topic: str

    _register_payload: dict

    _known_types = set()

    def __init__(self, local: str, remote: str, keep_alive: int = 600):
        host, port = EMQ.get_addr()

        self._send_topic = FROM_TO_CONNECTOR.join([local, remote])
        self._recv_topic = FROM_TO_CONNECTOR.join([remote, local])
        self._register_payload = dict()

        self._client = mqtt.Client()
        self._client.on_message = self._on_message
        self._client.connect(host, port, keep_alive)
        Logger.info('connected to mqtt message center')
        self._client.subscribe(self._recv_topic)
        Logger.info('subscribed topic `%s`' % self._recv_topic)
        self._client.loop_start()
        Logger.info('loop start~')

    def _on_message(self, client: mqtt.Client, _, msg):
        Logger.info('gotta message on client `%s`' % client)
        Logger.info('message content: %s' % msg.payload.decode())
        try:
            payload = deserialize(msg.payload, list(self._known_types))
        except NoTypeFoundError:
            Logger.warning('no handler installed for type `%s`' % UNKNOWN_TYPE)
            return
        typee = type(payload)
        if typee in self._register_payload:
            Logger.info('sent payload to installed handler `%s`' % self._register_payload[typee])
            self._register_payload[typee](payload)
        else:
            Logger.warning('no handler installed for type `%s`' % typee)

    def install_callback(self, typee: type, callback = None):
        if not issubclass(typee, Payload):
            raise TypeError('must provide type as a subclass of Payload')

        if callback:
            self._register_payload.update({typee: callback})
            self._known_types.add(typee)
        elif typee in self._register_payload:
            del self._register_payload[typee]

    def uninstall_callback(self, typee: type):
        self.install_callback(typee)


    def publish(self, payload: Payload):
        self._client.publish(self._send_topic, payload=serialize(payload))