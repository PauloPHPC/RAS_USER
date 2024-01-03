from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import GetUserSerializer
from .serializers import CreateUserSerializer
from .serializers import UpdateUserSerializer
from .serializers import CurrentUserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
import secrets
import string
import requests


@api_view(['POST'])
@permission_classes([])
def create_user(request):
    if request.method == 'POST':
        users_data = request.data  # Assumindo que request.data é uma lista de usuários

        if not isinstance(users_data, list):
            users_data = [users_data]

        created_users = []
        response = []
        for user_data in users_data:
            password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
            first_password = password

            user_data["password"] = make_password(password)

            user_data.setdefault("role", "student")

            serializer = CreateUserSerializer(data=user_data)
            if serializer.is_valid():
                serializer.save()
                created_users = [serializer.instance]
                try:
                    notification_url = f' http://nginx/notifications/credentials/{serializer.instance.id}/'

                    notification_data = {
                        "username": serializer.instance.email,
                        "password": first_password,
                    }

                    send_email = requests.post(notification_url, json=notification_data)
                except Exception:
                    print('impossible to send email to user')
                print(first_password)
            response.append(user_data)
        if created_users:          
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response("Failed to create user(s)", status=status.HTTP_400_BAD_REQUEST)


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
def update_user(request, id):
    if not request.user.is_authenticated:
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UpdateUserSerializer(user, data=request.data)
    if serializer.is_valid():
        password = serializer.validated_data.get('password')
        if password:
            serializer.validated_data['password'] = make_password(password)
        serializer.save()
        return Response({'message': 'Update successful'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user

    serializer = CurrentUserSerializer(user)
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