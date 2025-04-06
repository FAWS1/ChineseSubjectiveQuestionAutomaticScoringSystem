from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamViewSet, StudentAnswerViewSet

router = DefaultRouter()
router.register('exams', ExamViewSet)
router.register('student-answers', StudentAnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]