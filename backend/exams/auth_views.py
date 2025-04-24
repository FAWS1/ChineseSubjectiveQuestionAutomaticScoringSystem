#auth_views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .auth_serializers import LoginSerializer, UserSerializer
from django.contrib.auth import authenticate
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import Group

def generate_token(user_id, username, role):
    """生成JWT token"""
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

@api_view(['POST'])
def register(request):
    """用户注册视图"""
    role = request.data.get('role')
    if role not in ['teacher', 'student']:
        return Response({'error': '无效的用户角色'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        user.is_staff = (role == 'teacher')
        # 将用户添加到对应组
        try:
            group = Group.objects.get(name=role)
        except Group.DoesNotExist:
            group = Group.objects.create(name=role)
        user.groups.add(group)
        token = generate_token(user.id, user.username, role)
        return Response({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'is_teacher': user.groups.filter(name='teacher').exists()
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    """用户登录视图"""
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    try:
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            role = 'teacher' if user.groups.filter(name='teacher').exists() else 'student'
            token = generate_token(user.id, user.username, role)
            return Response({
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'is_teacher': user.groups.filter(name='teacher').exists()
                }
            })
        return Response({'error': '密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
    except ObjectDoesNotExist:
        return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

        #12345