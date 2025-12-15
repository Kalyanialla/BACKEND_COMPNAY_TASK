# # from django.shortcuts import render
# # from rest_framework_simplejwt.tokens import RefreshToken
# # from .serializers import RegisterSerializer
# # from rest_framework.decorators import api_view , permission_classes
# # from rest_framework.response import Response
# # from rest_framework import status
# # from django.contrib.auth import authenticate
# # from rest_framework.permissions import IsAuthenticated  
# # from django.contrib.auth.models import User


# # # SIGNUP
# # @api_view(['POST'])
# # def Signup(request):
# #     serializer = RegisterSerializer(data=request.data)

# #     if serializer.is_valid():
# #         serializer.save()
# #         return Response({"message": "User created"}, status=status.HTTP_201_CREATED)

# #     return Response({"message": "Not created", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# # # login 
# # @api_view(['POST'])
# # def Login(request):
# #     username = request.data.get("username")
# #     password = request.data.get("password")

# #     # Validate input
# #     if not username or not password:
# #         return Response(
# #             {"message": "Username and password are required"},
# #             status=status.HTTP_400_BAD_REQUEST
# #         )

# #     # Authenticate user
# #     user = authenticate(username=username, password=password)

# #     if user is not None:
# #         # Generate JWT tokens
# #         refresh = RefreshToken.for_user(user)
# #         return Response(
# #             {
# #                 "message": "Login successful",
# #                 "access_token": str(refresh.access_token),
# #                 "refresh_token": str(refresh)
# #             },
# #             status=status.HTTP_200_OK
# #         )

# #     # Invalid credentials
# #     return Response(
# #         {"message": "Invalid username or password"},
# #         status=status.HTTP_401_UNAUTHORIZED
# #     )

# # # logout
# # @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# # def Logout(request):
# #     refresh_token = request.data.get('refresh')  # refresh token from client
# #     if not refresh_token:
# #         return Response({"message": "Refresh token is required"}, status=400)
# #     try:
# #         token = RefreshToken(refresh_token)
# #         token.blacklist()
# #         return Response({"message": "Logout successful"}, status=200)
# #     except:
# #         return Response({"message": "Invalid token"}, status=400)



# # # get the uses
# # @api_view(['GET'])
# # def get_user(request):
# #     data=User.objects.all()
# #     serializer=RegisterSerializer(data,many=True)
# #     return Response(serializer.data)
    


# from django.shortcuts import render
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import RegisterSerializer
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from django.contrib.auth.models import User

# # SIGNUP
# @api_view(['POST'])
# @permission_classes([AllowAny])  # FIXED: Allow unauthenticated access
# def Signup(request):
#     serializer = RegisterSerializer(data=request.data)

#     if serializer.is_valid():
#         user = serializer.save()
#         # Generate tokens for immediate login after signup
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             "message": "User created successfully",
#             "user": {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email
#             },
#             "access_token": str(refresh.access_token),
#             "refresh_token": str(refresh)
#         }, status=status.HTTP_201_CREATED)

#     return Response({
#         "message": "Registration failed",
#         "errors": serializer.errors
#     }, status=status.HTTP_400_BAD_REQUEST)


# # LOGIN
# @api_view(['POST'])
# @permission_classes([AllowAny])  # FIXED: Allow unauthenticated access
# def Login(request):
#     username = request.data.get("username")
#     password = request.data.get("password")

#     # Validate input
#     if not username or not password:
#         return Response(
#             {"message": "Username and password are required"},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     # Authenticate user
#     user = authenticate(username=username, password=password)

#     if user is not None:
#         # Generate JWT tokens
#         refresh = RefreshToken.for_user(user)
#         return Response(
#             {
#                 "message": "Login successful",
#                 "user": {
#                     "id": user.id,
#                     "username": user.username,
#                     "email": user.email,
#                     "first_name": user.first_name,
#                     "last_name": user.last_name
#                 },
#                 "access_token": str(refresh.access_token),
#                 "refresh_token": str(refresh)
#             },
#             status=status.HTTP_200_OK
#         )

#     # Invalid credentials
#     return Response(
#         {"message": "Invalid username or password"},
#         status=status.HTTP_401_UNAUTHORIZED
#     )


# # LOGOUT
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def Logout(request):
#     try:
#         refresh_token = request.data.get('refresh_token')  # FIXED: Changed from 'refresh'
        
#         if not refresh_token:
#             return Response(
#                 {"message": "Refresh token is required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         token = RefreshToken(refresh_token)
#         token.blacklist()
        
#         return Response(
#             {"message": "Logout successful"},
#             status=status.HTTP_200_OK
#         )
#     except Exception as e:
#         return Response(
#             {"message": "Invalid or expired token", "error": str(e)},
#             status=status.HTTP_400_BAD_REQUEST
#         )


# # GET ALL USERS
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])  # FIXED: Require authentication
# def get_user(request):
#     """Get all users (for chat user selection)"""
#     # Exclude current user from the list
#     users = User.objects.exclude(id=request.user.id)
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)





# # get the uses
# @api_view(['GET'])
# def get_user(request):
#     data=User.objects.all()
#     serializer=RegisterSerializer(data,many=True)
#     return Response(serializer.data)


from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User


# SIGNUP
@api_view(['POST'])
@permission_classes([AllowAny])
def Signup(request):
    """Register a new user"""
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        # Generate tokens for immediate login after signup
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "User created successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            },
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_201_CREATED)

    return Response({
        "message": "Registration failed",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


# LOGIN
@api_view(['POST'])
@permission_classes([AllowAny])
def Login(request):
    """Login user and return JWT tokens"""
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"message": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            },
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_200_OK)

    return Response(
        {"message": "Invalid username or password"},
        status=status.HTTP_401_UNAUTHORIZED
    )


# LOGOUT
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Logout(request):
    """Logout user by blacklisting refresh token"""
    try:
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response(
                {"message": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"message": "Invalid or expired token", "error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


# GET ALL USERS (excluding current user)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    """Get all users except current user (for chat)"""
    users = User.objects.exclude(id=request.user.id)
    serializer = UserSerializer(users, many=True)
    return Response({
        "message": "Users retrieved successfully",
        "users": serializer.data
    }, status=status.HTTP_200_OK)


# GET CURRENT USER
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """Get currently logged in user details"""
    serializer = UserSerializer(request.user)
    return Response({
        "message": "Current user retrieved successfully",
        "user": serializer.data
    }, status=status.HTTP_200_OK)