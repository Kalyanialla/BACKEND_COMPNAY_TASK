"""
Management command to delete all users from the database
Usage: python manage.py delete_all_users
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chat.models import ChatRoom, Message, UserProfile


class Command(BaseCommand):
    help = 'Delete all users, chat rooms, and messages from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion (required to actually delete)',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'This will delete ALL users, chat rooms, and messages!\n'
                    'To confirm, run: python manage.py delete_all_users --confirm'
                )
            )
            return

        # Count before deletion
        user_count = User.objects.count()
        room_count = ChatRoom.objects.count()
        message_count = Message.objects.count()
        profile_count = UserProfile.objects.count()

        self.stdout.write(f'Found:')
        self.stdout.write(f'  - {user_count} users')
        self.stdout.write(f'  - {room_count} chat rooms')
        self.stdout.write(f'  - {message_count} messages')
        self.stdout.write(f'  - {profile_count} user profiles')
        self.stdout.write('')

        # Delete in order (respecting foreign key constraints)
        self.stdout.write('Deleting messages...')
        Message.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('✓ Messages deleted'))

        self.stdout.write('Deleting chat rooms...')
        ChatRoom.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('✓ Chat rooms deleted'))

        self.stdout.write('Deleting user profiles...')
        UserProfile.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('✓ User profiles deleted'))

        self.stdout.write('Deleting users...')
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('✓ Users deleted'))

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully deleted all data!\n'
                f'  - {user_count} users\n'
                f'  - {room_count} chat rooms\n'
                f'  - {message_count} messages\n'
                f'  - {profile_count} user profiles'
            )
        )
        self.stdout.write('')
        self.stdout.write('Database is now clean. You can start fresh!')
