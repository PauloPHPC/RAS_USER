from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import GetUserSerializer
from .serializers import CreateUserSerializer
from .serializers import UpdateUserSerializer
from django.contrib.auth.hashers import make_password
import secrets
import string
import requests


@api_view(['POST'])
@permission_classes([])
def create_user(request):
    if request.method == 'POST':
        password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))

        first_password = password

        request.data["password"] = make_password(password)

        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        
            try:
                notification_url = f'http://localhost:8000/notifications/credentials/{User.id}/'

                notification_data = {
                    "username": User.email,
                    "password": first_password,
                    }

                send_email = requests.post(notification_url, json=notification_data)
            except Exception:
                print('impossible to send email to user')
            print(first_password)    
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([])
def get_user_by_id(request, id):
    try:
        user = User.objects.get(id=id)
        serializer = GetUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([])
def get_user_by_email(request, email):
    try:
        user = User.objects.get(email=email)
        serializer = GetUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    user = request.user

    serializer = UpdateUserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Update successful'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    # Implement your to get the current user information
    user = request.user  # Assuming you have authentication middleware enabled
    serializer = GetUserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['POST'])
# @permission_classes([])
# def user_login(request):
#     serializer = LoginSerializer(data=request.data)
#     if serializer.is_valid():
#         # Implement your authentication logic here
#         # For simplicity, let's assume a successful login for any valid request
#         access_token = "your_access_token"
#         refresh_token = "your_refresh_token"
#         return Response({'access': access_token, 'refresh': refresh_token}, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def user_logout(request):
#     # Implement your logout logic here
#     return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def refresh_access_token(request):
#     serializer = RefreshTokenSerializer(data=request.data)
#     if serializer.is_valid():
#         # Implement your logic to refresh the access token
#         new_access_token = "your_new_access_token"
#         return Response({'token': new_access_token}, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)