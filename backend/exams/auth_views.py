from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .auth_models import TeacherAuth, StudentAuth
from .auth_serializers import TeacherAuthSerializer, StudentAuthSerializer, LoginSerializer
import jwt
from datetime import datetime, timedelta
from django.conf import settings

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
    
    serializer = TeacherAuthSerializer if role == 'teacher' else StudentAuthSerializer
    serializer = serializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        token = generate_token(user.id, user.username, role)
        return Response({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'role': role
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
    auth_model = TeacherAuth if data['role'] == 'teacher' else StudentAuth
    
    try:
        user = auth_model.objects.get(username=data['username'])
        if user.check_password(data['password']):
            token = generate_token(user.id, user.username, data['role'])
            return Response({
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'role': data['role']
                }
            })
        return Response({'error': '密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
    except ObjectDoesNotExist:
        return Response({'error': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)