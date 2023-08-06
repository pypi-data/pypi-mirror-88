from abc import ABC

from mux_demux_ws.utils import group_send_mux_demux


class MuxDemuxConsumerException(Exception):
    pass

class SecondaryBaseConsumer(ABC):

    def __init__(self, primary_consumer, key, id):
        self.primary_consumer = primary_consumer
        self.user = primary_consumer.user
        self.channel_layer = primary_consumer.channel_layer
        self.channel_name = primary_consumer.channel_name
        self.key = key
        self.id = id
        self.groups = set()

    @property
    def is_authenticated(self):
        return self.primary_consumer.is_authenticated

    async def send_message(self, message):
        await self.primary_consumer.send_message({
            'data': message,
            'id': self.id,
        })

    async def connect(self, data):
        return True

    async def disconnect(self, close_code=None):
        del self.primary_consumer.connections[self.id]
        return True

    async def receive(self, data):
        await self.commands[data['command']](self, data)

    commands = {
        'disconnect': disconnect,
        'send_message': send_message,
    }

    async def group_add(self, group_name):
        if group_name not in self.groups:
            self.groups.add(group_name)
            if group_name not in self.primary_consumer.groups:
                self.primary_consumer.groups[group_name] = {}
                await self.channel_layer.group_add(
                    group_name,
                    self.channel_name
                )
            self.primary_consumer.groups[group_name][self.id] = self

    async def group_discard(self, group_name):
        if group_name in self.groups:
            self.groups.remove(group_name)
            del self.primary_consumer.groups[group_name][self.id]
            if len(self.primary_consumer.groups[group_name].keys()) == 0:
                await self.channel_layer.group_discard(
                    group_name,
                    self.channel_name
                )

    async def group_send(self, group_name, data):
        return await group_send_mux_demux(group_name, data, channel_layer=self.channel_layer)

class SecondaryDefaultConsumer(SecondaryBaseConsumer):
    default_group_name = None

    async def connect(self, data):
        if not self.is_authenticated:
            raise MuxDemuxConsumerException("No user authenticated")
        if self.default_group_name:
            await self.group_add(self.default_group_name)
        return super().connect(data)

    async def disconnect(self, close_code=None):
        ret = super().disconnect(close_code)
        if self.default_group_name:
            await self.group_discard(self.default_group_name)
        return ret