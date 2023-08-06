import json
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer


# from mux_demux_ws.secondary_consumers import AlertConsumer
# consumers = {
#     "shopper_chat": ChatShopperConsumer,
#     "customer_chat": ChatCustomerConsumer,
#     "alerts": AlertConsumer,
# }


from django.conf import settings
consumers = getattr(settings, 'MUX_DEMUX_CONSUMERS', {})


class PrimaryConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connections = {}
        self.groups = {}

    @property
    def is_authenticated(self):
        return self.user and not self.user.is_anonymous




    def get_query_params(self):
        return parse_qs(self.scope['query_string'].decode())

    async def forward(self, event):
        group = event["group"]
        action = event["action"]
        if group in self.groups:
            for consumer in self.groups[group].values():
                await getattr(consumer, action)(event)


    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = 'muxdemux_{}'.format(self.user.id)
        self.query_params = self.get_query_params()

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        await self.send_sys_message({
            "type": "connected",
            "text": "Connection successful."
        })

    async def disconnect(self, close_code):
        # leave group room
        for connection in self.connections.values():
            try:
                await connection.disconnect(close_code)
            except:
                continue
        try:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        except Exception:
            pass

    async def disconnect(self, close_code):
        pass

    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    async def send_sys_message(self, message):
        await self.send_message({
            'data': message,
            'id': "sys",
        })

    async def secondary_connect(self, data):
        if data['key'] not in self.consumers:
            available_consumers = ", ".join([k for k in self.consumers.keys()])
            await self.send_sys_message({
                'key': data['key'],
                'id': data['id'],
                'type': "error",
                'text': f"Invalid key {data['key']} options are {available_consumers}"
            })
        else:
            if data['id'] in self.connections:
                try:
                    await self.connections[data['id']].disconnect()
                except Exception:
                    pass
            new_consumer = self.consumers[data['key']](self, data['key'], data['id'])
            try:
                connected = await new_consumer.connect(data)
            except Exception as e:
                print(e)
                connected = False
            if connected:
                self.connections[data['id']] = new_consumer
                await self.send_sys_message({
                    'key': data['key'],
                    'id': data['id'],
                    'type': "sys",
                    'text': f"Connection to {data['key']} successful"
                })
            else:
                await self.send_sys_message({
                    'key': data['key'],
                    'id': data['id'],
                    'type': "error",
                    'text': f"Error connecting to {data['key']}"
                })


    async def receive(self, text_data):
        data = json.loads(text_data)
        if 'command' not in data:
            await self.send_sys_message({
                'type': "error",
                'text': 'No command specified'
            })
        elif data['command'] == "connect":
            if not 'key' in data:
                await self.send_sys_message({
                    'type': "error",
                    'text': "No key specified for 'connect' command"
                })
            elif not 'id' in data:
                await self.send_sys_message({
                    'type': "error",
                    'text': "No 'id' specified for 'connect' command"
                })
            else:
                await self.secondary_connect(data)
        elif 'id' not in data:
            if data['command'] not in self.commands:
                await self.send_sys_message({
                    'type': "error",
                    'text': f"Invalid command '{data['command']}' for primary consumer"
                })
            else:
                await self.commands[data['command']](self)
        elif data['id'] not in self.connections:
            await self.send_sys_message({
                'id': data['id'],
                'type': "error",
                'text': f"No connection for id '{data['id']}'"
            })
        else:
            connection = self.connections[data['id']]
            try:
                await connection.receive(data)
            except Exception as e:
                print(e)
                await self.send_sys_message({
                    'id': data['id'],
                    'type': "error",
                    'text': str(e)
                })


    async def ping(self):
        await self.send_sys_message({
            'type': "pong",
        })

    commands = {
        'ping': ping
    }



