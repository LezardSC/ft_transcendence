from channels.generic.websocket import AsyncWebsocketConsumer
from users.models import CustomUser
import json


class FriendsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = 'friend_request'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, exit_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'friend_request':
            from_user = data.get('from_user')
            to_user = data.get('to')
            await self.channel_layer.group_send(
                self.group_name,
                {'type': 'send_friend_request_notification',
                'from_user': from_user,
                'to': to_user})
            
    async def send_friend_request_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'friend_request',
            'from_user': event['from_user'],
            'to': event['to'],
            }))

    async def authenticate_user_with_username(self, username):
        try:
            user = await CustomUser.objects.aget(username=username)
            return user
        except CustomUser.DoesNotExist:
            return None
        
    async def authenticate_user(self, text_data_json):
        username = text_data_json['username']
        user = await self.authenticate_user_with_username(username)
        if user is not None:
            self.scope['user'] = user
            await self.send(text_data=json.dumps({ "type": "auth", "status": "success"}))
        else:
            await self.send(text_data=json.dumps({ "type": "auth", "status": "failed"}))