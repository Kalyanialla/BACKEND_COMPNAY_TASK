from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings


class UserProfile(models.Model):
    """Extended user profile with online status"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"{self.user.username}'s profile"


class ChatRoom(models.Model):
    """Chat room for 1-to-1 or group conversations"""
    ROOM_TYPE_CHOICES = [
        ('ONE_TO_ONE', 'One to One'),
        ('GROUP', 'Group'),
    ]
    
    name = models.CharField(max_length=255, blank=True, null=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='ONE_TO_ONE')
    members = models.ManyToManyField(User, related_name='chat_rooms')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chat_rooms'
        ordering = ['-updated_at']
    
    def __str__(self):
        if self.name:
            return self.name
        return f"Room {self.id}"


class Message(models.Model):
    """Encrypted message model"""
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    encrypted_content = models.TextField()  # Encrypted message content
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'messages'
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['room', '-timestamp']),
            models.Index(fields=['sender', '-timestamp']),
        ]
    
    def encrypt_message(self, content):
        """Encrypt message before saving to database (Server-side encryption)"""
        try:
            cipher = Fernet(settings.ENCRYPTION_KEY.encode())
            self.encrypted_content = cipher.encrypt(content.encode()).decode()
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")
    
    def decrypt_message(self):
        """Decrypt message when retrieving from database"""
        try:
            if not self.encrypted_content:
                return "[No content to decrypt]"
            
            # Validate encryption key format
            encryption_key = settings.ENCRYPTION_KEY
            if not encryption_key:
                return "[Encryption key not configured]"
            
            try:
                cipher = Fernet(encryption_key.encode())
                decrypted = cipher.decrypt(self.encrypted_content.encode()).decode()
                return decrypted
            except Exception as e:
                # Log the error for debugging
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Decryption error for message {self.id}: {str(e)}")
                return f"[Decryption failed: {str(e)}]"
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Unexpected error in decrypt_message: {str(e)}")
            return "[Decryption failed]"
    
    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"