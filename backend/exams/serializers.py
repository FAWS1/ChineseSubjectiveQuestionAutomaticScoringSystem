#serializers.py
from rest_framework import serializers
from .models import Exam, StudentAnswer

class ExamSerializer(serializers.ModelSerializer):
    """考试序列化器"""
    class Meta:
        model = Exam
        fields = ['exam_name']

class StudentAnswerSerializer(serializers.ModelSerializer):
    """学生答案序列化器"""
    exam_name = serializers.CharField(source='exam.exam_name', read_only=True)

    class Meta:
        model = StudentAnswer
        fields = ['id', 'exam', 'exam_name', 'student_name', 'answer', 'score', 'similarity', 'created_at']

class ScoreQuerySerializer(serializers.Serializer):
    """成绩查询序列化器"""
    exam_id = serializers.IntegerField()
    student_name = serializers.CharField(max_length=50)