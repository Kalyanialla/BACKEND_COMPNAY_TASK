# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import ChatRoom, Message, UserProfile


# class UserProfileSerializer(serializers.ModelSerializer):
#     """Serializer for user profile"""
#     class Meta:
#         model = UserProfile
#         fields = ['is_online', 'last_seen']


# class UserSerializer(serializers.ModelSerializer):
#     """Serializer for user details"""
#     profile = UserProfileSerializer(read_only=True)
    
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']


# class MessageSerializer(serializers.ModelSerializer):
#     """Serializer for messages with decryption"""
#     sender = UserSerializer(read_only=True)
#     content = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Message
#         fields = ['id', 'sender', 'content', 'timestamp', 'is_read']
    
#     def get_content(self, obj):
#         return obj.decrypt_message()


# class ChatRoomSerializer(serializers.ModelSerializer):
#     """Serializer for chat rooms"""
#     members = UserSerializer(many=True, read_only=True)
#     member_ids = serializers.ListField(
#         child=serializers.IntegerField(),
#         write_only=True,
#         required=False
#     )
#     last_message = serializers.SerializerMethodField()
#     unread_count = serializers.SerializerMethodField()
    
#     class Meta:
#         model = ChatRoom
#         fields = ['id', 'name', 'room_type', 'members', 'member_ids', 
#                   'created_at', 'updated_at', 'last_message', 'unread_count']
    
#     def get_last_message(self, obj):
#         last_msg = obj.messages.last()
#         if last_msg:
#             return {
#                 'id': last_msg.id,
#                 'content': last_msg.decrypt_message(),
#                 'sender': last_msg.sender.username,
#                 'timestamp': last_msg.timestamp.isoformat()
#             }
#         return None
    
#     def get_unread_count(self, obj):
#         request = self.context.get('request')
#         if request and request.user and request.user.is_authenticated:
#             return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
#         return 0



from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ChatRoom, Message, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    class Meta:
        model = UserProfile
        fields = ['is_online', 'last_seen']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details with profile"""
    profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']
    
    def get_profile(self, obj):
        """Get or create profile for user"""
        profile, created = UserProfile.objects.get_or_create(user=obj)
        return UserProfileSerializer(profile).data


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for messages with decryption"""
    sender = UserSerializer(read_only=True)
    content = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'is_read']
    
    def get_content(self, obj):
        return obj.decrypt_message()


class ChatRoomSerializer(serializers.ModelSerializer):
    """Serializer for chat rooms"""
    members = UserSerializer(many=True, read_only=True)
    member_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'room_type', 'members', 'member_ids', 
                  'created_at', 'updated_at', 'last_message', 'unread_count']
    
    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return {
                'id': last_msg.id,
                'content': last_msg.decrypt_message(),
                'sender': last_msg.sender.username,
                'timestamp': last_msg.timestamp.isoformat()
            }
        return None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0
   