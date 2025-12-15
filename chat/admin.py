from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, ChatRoom, Message


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_online', 'last_seen', 'created_at']
    list_filter = ['is_online', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'last_seen']


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'room_type', 'created_by', 'created_at']
    list_filter = ['room_type', 'created_at']
    search_fields = ['name', 'created_by__username']
    filter_horizontal = ['members']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'room', 'timestamp', 'is_read']
    list_filter = ['is_read', 'timestamp']
    search_fields = ['sender__username', 'room__name']
    readonly_fields = ['encrypted_content', 'timestamp']
    
    def get_readonly_fields(self, request, obj=None):
        # Make all fields readonly for editing
        if obj:
            return ['encrypted_content', 'timestamp', 'sender', 'room']
        return ['encrypted_content', 'timestamp']