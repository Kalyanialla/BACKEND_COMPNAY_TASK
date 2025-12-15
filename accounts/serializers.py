# from rest_framework import serializers
# from django.contrib.auth.models import User

# class RegisterSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ["username", "email", "password", "password2"]
#         extra_kwargs = {
#             "password": {"write_only": True}
#         }

#     # Validate passwords and uniqueness
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields do not match"})
        
#         if User.objects.filter(username=attrs['username']).exists():
#             raise serializers.ValidationError({"username": "Username already exists"})
        
#         if User.objects.filter(email=attrs['email']).exists():
#             raise serializers.ValidationError({"email": "Email already exists"})
        
#         return attrs

#     # Create user
#     def create(self, validated_data):
#         # Remove password2 before creating user
#         validated_data.pop('password2')

#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password']  # Django hashes automatically
#         )
#         return user


from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        """Validate passwords match and check uniqueness"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields do not match"})
        
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists"})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
        
        return attrs

    def create(self, validated_data):
        """Create user and user profile"""
        validated_data.pop('password2')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # FIXED: Import here to avoid circular import
        from chat.models import UserProfile
        UserProfile.objects.get_or_create(user=user)
        
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for basic user details without profile"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']