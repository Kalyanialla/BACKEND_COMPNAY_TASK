from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated  
from django.contrib.auth.models import User


# SIGNUP
@api_view(['POST'])
def Signup(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created"}, status=status.HTTP_201_CREATED)

    return Response({"message": "Not created", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# login 
@api_view(['POST'])
def Login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    # Validate input
    if not username or not password:
        return Response(
            {"message": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Authenticate user
    user = authenticate(username=username, password=password)

    if user is not None:
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "Login successful",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            },
            status=status.HTTP_200_OK
        )

    # Invalid credentials
    return Response(
        {"message": "Invalid username or password"},
        status=status.HTTP_401_UNAUTHORIZED
    )

# logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Logout(request):
    refresh_token = request.data.get('refresh')  # refresh token from client
    if not refresh_token:
        return Response({"message": "Refresh token is required"}, status=400)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful"}, status=200)
    except:
        return Response({"message": "Invalid token"}, status=400)



# get the uses
@api_view(['GET'])
def get_user(request):
    data=User.objects.all()
    serializer=RegisterSerializer(data,many=True)
    return Response(serializer.data)
    