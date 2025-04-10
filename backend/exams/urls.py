from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamViewSet, StudentAnswerViewSet
from . import auth_views

router = DefaultRouter()

# 认证相关路由
urlpatterns = [
    path('auth/register/', auth_views.register, name='register'),
    path('auth/login/', auth_views.login, name='login'),
]

# API路由
router.register('exams', ExamViewSet)
router.register('student-answers', StudentAnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]