from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateExams, UploadAnswers, AutoScoring, ViewScores, AnalysisScores
from . import auth_views

# 初始化路由
router = DefaultRouter()
router.register('create-exams', CreateExams, basename='create-exams')
router.register('upload-answers', UploadAnswers, basename='upload-answers')
router.register('auto-scoring', AutoScoring, basename='auto-scoring')
router.register('view-scores', ViewScores, basename='view-scores')
router.register('analysis-scores', AnalysisScores, basename='analysis-scores')

# 合并所有路由
urlpatterns = [
    path('auth/register/', auth_views.register, name='register'),
    path('auth/login/', auth_views.login, name='login'),
    path('', include(router.urls)),  # 这必须放最后，避免覆盖其他路由
]
