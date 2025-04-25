# jwt_auth.py
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth.models import User
import jwt

class JWTAuthentication(authentication.BaseAuthentication):
    """
    自定义JWT认证类
    从请求头中获取JWT令牌并验证用户身份
    """
    def authenticate(self, request):
        # 从请求头中获取Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None
        
        # 提取令牌
        token = auth_header.split(' ')[1]
        
        try:
            # 解码令牌
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            username = payload.get('username')
            
            # 获取用户
            user = User.objects.get(id=user_id, username=username)
            
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('令牌已过期')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('无效的令牌')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('用户不存在')