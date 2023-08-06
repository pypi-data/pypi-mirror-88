from channels.layers import get_channel_layer

async def group_send_mux_demux(group_name, data, channel_layer=None):
    channel_layer = channel_layer or get_channel_layer()
    action = data.pop('type')
    await channel_layer.group_send(
        group_name,
        {
            **data,
            'group': group_name,
            'type': 'forward',
            'action': action,
        }
    )