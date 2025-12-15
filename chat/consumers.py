# import json
# import logging
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from django.contrib.auth.models import User
# from .models import ChatRoom, Message, UserProfile
# from rest_framework_simplejwt.tokens import AccessToken
# from rest_framework_simplejwt.exceptions import TokenError

# logger = logging.getLogger(__name__)


# class ChatConsumer(AsyncWebsocketConsumer):
#     """WebSocket consumer for real-time chat"""
    
#     async def connect(self):
#         """Handle WebSocket connection"""
#         try:
#             # Get JWT token from query string
#             query_string = self.scope['query_string'].decode()
#             token = None
            
#             if query_string:
#                 params = dict(x.split('=') for x in query_string.split('&') if '=' in x)
#                 token = params.get('token', '')
            
#             logger.info(f"WebSocket connection attempt - Room: {self.scope['url_route']['kwargs'].get('room_id')}, Token present: {bool(token)}")
            
#             # Authenticate user using JWT
#             self.user = await self.authenticate_user(token)
            
#             if not self.user:
#                 logger.warning("WebSocket connection rejected: Invalid or missing token")
#                 await self.close(code=4001)  # Unauthorized
#                 return
            
#             # Get room_id and convert to int if needed
#             room_id_str = self.scope['url_route']['kwargs']['room_id']
#             try:
#                 self.room_id = int(room_id_str)
#             except ValueError:
#                 logger.error(f"Invalid room_id format: {room_id_str}")
#                 await self.close(code=4004)  # Bad request
#                 return
            
#             self.room_group_name = f'chat_{self.room_id}'
            
#             # Verify user is member of the room
#             is_member = await self.verify_room_membership()
#             if not is_member:
#                 logger.warning(f"WebSocket connection rejected: User {self.user.id} is not a member of room {self.room_id}")
#                 await self.close(code=4003)  # Forbidden
#                 return
            
#             # Join room group
#             try:
#                 await self.channel_layer.group_add(
#                     self.room_group_name,
#                     self.channel_name
#                 )
#             except Exception as e:
#                 logger.error(f"Failed to join channel layer group: {e}")
#                 await self.close(code=4004)  # Internal error
#                 return
            
#             await self.accept()
#             await self.set_user_online(True)
            
#             logger.info(f"WebSocket connected: User {self.user.id} to room {self.room_id}")
            
#             # Notify others user joined
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'user_status',
#                     'user_id': self.user.id,
#                     'username': self.user.username,
#                     'status': 'online'
#                 }
#             )
#         except Exception as e:
#             logger.error(f"Error in WebSocket connect: {e}", exc_info=True)
#             await self.close(code=4004)  # Internal error
    
#     async def disconnect(self, close_code):
#         """Handle WebSocket disconnection"""
#         if hasattr(self, 'user') and self.user:
#             await self.set_user_online(False)
            
#             if hasattr(self, 'room_group_name'):
#                 await self.channel_layer.group_send(
#                     self.room_group_name,
#                     {
#                         'type': 'user_status',
#                         'user_id': self.user.id,
#                         'username': self.user.username,
#                         'status': 'offline'
#                     }
#                 )
        
#         if hasattr(self, 'room_group_name'):
#             await self.channel_layer.group_discard(
#                 self.room_group_name,
#                 self.channel_name
#             )
    
#     async def receive(self, text_data):
#         """Receive message from WebSocket"""
#         try:
#             data = json.loads(text_data)
#             message_type = data.get('type', 'message')
            
#             if message_type == 'message':
#                 content = data.get('content', '').strip()
                
#                 if not content:
#                     return
                
#                 # Save encrypted message to database
#                 message = await self.save_message(content)
                
#                 # Use original content for WebSocket (already decrypted)
#                 # Decryption is only needed when retrieving from database via API
#                 message_payload = {
#                     'type': 'chat_message',
#                     'message': {
#                         'id': message.id,
#                         'content': content,  # Use original content (already plaintext)
#                         'sender': {
#                             'id': self.user.id,
#                             'username': self.user.username,
#                             'first_name': self.user.first_name,
#                             'last_name': self.user.last_name
#                         },
#                         'timestamp': message.timestamp.isoformat(),
#                         'is_read': False
#                     }
#                 }
                
#                 logger.info(
#                     f"Broadcasting message {message.id} from user {self.user.id} "
#                     f"to group {self.room_group_name} (room {self.room_id})"
#                 )
                
#                 # Broadcast to ALL users in the room (including sender)
#                 await self.channel_layer.group_send(
#                     self.room_group_name,
#                     message_payload
#                 )
                
#                 logger.info(
#                     f"Message {message.id} successfully broadcast to group {self.room_group_name}. "
#                     f"All connected users in room {self.room_id} should receive it."
#                 )
            
#             elif message_type == 'typing':
#                 # Broadcast typing indicator
#                 await self.channel_layer.group_send(
#                     self.room_group_name,
#                     {
#                         'type': 'typing_indicator',
#                         'user_id': self.user.id,
#                         'username': self.user.username,
#                         'is_typing': data.get('is_typing', False)
#                     }
#                 )
                
#         except json.JSONDecodeError as e:
#             logger.error(f"JSON decode error: {e}")
#             await self.send(text_data=json.dumps({
#                 'type': 'error',
#                 'message': 'Invalid JSON format'
#             }))
#         except Exception as e:
#             logger.error(f"Error in receive: {e}", exc_info=True)
#             await self.send(text_data=json.dumps({
#                 'type': 'error',
#                 'message': 'An error occurred processing your message'
#             }))
    
#     async def chat_message(self, event):
#         """Send message to WebSocket - This is called for ALL users in the room"""
#         try:
#             message_data = event.get('message', {})
#             sender_id = message_data.get('sender', {}).get('id')
#             current_user_id = self.user.id if hasattr(self, 'user') and self.user else None
            
#             logger.info(
#                 f"Broadcasting message {message_data.get('id')} to user {current_user_id} "
#                 f"(sender: {sender_id}) in room {getattr(self, 'room_id', 'unknown')}"
#             )
            
#             # Send message to this WebSocket connection (all users in room receive this)
#             await self.send(text_data=json.dumps({
#                 'type': 'message',
#                 'message': message_data
#             }))
            
#             logger.info(f"Message {message_data.get('id')} successfully sent to user {current_user_id}")
#         except Exception as e:
#             logger.error(f"Error sending message to WebSocket for user {getattr(self, 'user', {}).id}: {e}", exc_info=True)
    
#     async def user_status(self, event):
#         """Send user status to WebSocket"""
#         await self.send(text_data=json.dumps({
#             'type': 'user_status',
#             'user_id': event['user_id'],
#             'username': event['username'],
#             'status': event['status']
#         }))
    
#     async def typing_indicator(self, event):
#         """Send typing indicator to WebSocket (exclude sender)"""
#         if event['user_id'] != self.user.id:
#             await self.send(text_data=json.dumps({
#                 'type': 'typing',
#                 'user_id': event['user_id'],
#                 'username': event['username'],
#                 'is_typing': event['is_typing']
#             }))
    
#     @database_sync_to_async
#     def authenticate_user(self, token):
#         """Authenticate user using JWT token"""
#         if not token:
#             return None
#         try:
#             access_token = AccessToken(token)
#             user_id = access_token['user_id']
#             return User.objects.get(id=user_id)
#         except (TokenError, User.DoesNotExist, KeyError):
#             return None
    
#     @database_sync_to_async
#     def verify_room_membership(self):
#         """Verify user is a member of the chat room"""
#         try:
#             room = ChatRoom.objects.get(id=self.room_id)
#             return room.members.filter(id=self.user.id).exists()
#         except ChatRoom.DoesNotExist:
#             return False
    
#     @database_sync_to_async
#     def save_message(self, content):
#         """Save encrypted message to database"""
#         room = ChatRoom.objects.get(id=self.room_id)
#         message = Message.objects.create(
#             room=room,
#             sender=self.user
#         )
#         message.encrypt_message(content)  # Encrypt on server-side
#         message.save()
#         return message
    
#     @database_sync_to_async
#     def set_user_online(self, is_online):
#         """Update user online status"""
#         profile, created = UserProfile.objects.get_or_create(user=self.user)
#         profile.is_online = is_online
#         profile.save()
    







import json
import logging
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import ChatRoom, Message, UserProfile

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            query = parse_qs(self.scope["query_string"].decode())
            token = query.get("token", [None])[0]

            self.user = await self.authenticate_user(token)
            if not self.user:
                await self.close(code=4001)
                return

            self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
            self.room_group_name = f"chat_{self.room_id}"

            is_member = await self.verify_room_membership()
            if not is_member:
                await self.close(code=4003)
                return

            await self.accept()

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.set_user_online(True)

        except Exception:
            logger.error("WebSocket connect error", exc_info=True)
            await self.close(code=4004)

    async def disconnect(self, close_code):
        try:
            if hasattr(self, "user") and self.user:
                await self.set_user_online(False)

            if hasattr(self, "room_group_name"):
                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                )
        except Exception:
            logger.error("WebSocket disconnect error", exc_info=True)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            content = data.get("content", "").strip()
            if not content:
                return

            message = await self.save_message(content)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": {
                        "id": message.id,
                        "content": content,
                        "sender": {
                            "id": self.user.id,
                            "username": self.user.username,
                        },
                        "timestamp": message.timestamp.isoformat(),
                    }
                }
            )

        except Exception:
            logger.error("WebSocket receive error", exc_info=True)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "message",
            "message": event["message"]
        }))

    # ================= DB HELPERS =================

    @database_sync_to_async
    def authenticate_user(self, token):
        try:
            access = AccessToken(token)
            return User.objects.get(id=access["user_id"])
        except Exception:
            return None

    @database_sync_to_async
    def verify_room_membership(self):
        try:
            room = ChatRoom.objects.get(id=self.room_id)
            return room.members.filter(id=self.user.id).exists()
        except ChatRoom.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, content):
        room = ChatRoom.objects.get(id=self.room_id)
        message = Message.objects.create(room=room, sender=self.user)
        message.encrypt_message(content)
        message.save()
        return message

    @database_sync_to_async
    def set_user_online(self, is_online):
        profile, _ = UserProfile.objects.get_or_create(user=self.user)
        profile.is_online = is_online
        profile.save()
