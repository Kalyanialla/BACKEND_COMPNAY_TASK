from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Q
from .models import ChatRoom 
from .serializers import ChatRoomSerializer, MessageSerializer  # FIXED: seializers -> serializers


class ChatRoomViewSet(viewsets.ModelViewSet):
    """ViewSet for managing chat rooms"""
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get only rooms where user is a member"""
        return ChatRoom.objects.filter(members=self.request.user).distinct()
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def create(self, request):
        """Create a new chat room (1-to-1 or group)"""
        room_type = request.data.get('room_type', 'ONE_TO_ONE')
        member_ids = request.data.get('member_ids', [])
        name = request.data.get('name', '')
        
        if not member_ids:
            return Response(
                {'error': 'member_ids is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # For 1-to-1 chat, check if room already exists
        if room_type == 'ONE_TO_ONE' and len(member_ids) == 1:
            existing_room = ChatRoom.objects.filter(
                room_type='ONE_TO_ONE',
                members=request.user
            ).filter(members__id=member_ids[0]).distinct()
            
            if existing_room.exists():
                room = existing_room.first()
                return Response(
                    ChatRoomSerializer(room, context={'request': request}).data,
                    status=status.HTTP_200_OK
                )
        
        # Create new room
        room = ChatRoom.objects.create(
            name=name if name else None,
            room_type=room_type,
            created_by=request.user
        )
        room.members.add(request.user)
        
        # Add other members
        for member_id in member_ids:
            try:
                user = User.objects.get(id=member_id)
                room.members.add(user)
            except User.DoesNotExist:
                pass
        
        return Response(
            ChatRoomSerializer(room, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages in a room"""
        room = self.get_object()
        messages = room.messages.all()
        
        # Mark messages as read
        messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark all messages in room as read"""
        room = self.get_object()
        room.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
        return Response({'status': 'messages marked as read'})