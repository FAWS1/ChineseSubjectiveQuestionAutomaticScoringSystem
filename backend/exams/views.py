from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Exam, StudentAnswer
from .serializers import ExamSerializer, StudentAnswerSerializer, ScoreQuerySerializer
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from difflib import SequenceMatcher

class ExamViewSet(viewsets.ModelViewSet):
    """考试视图集"""
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class StudentAnswerViewSet(viewsets.ModelViewSet):
    """学生答案视图集"""
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer

    def create(self, request, *args, **kwargs):
        try:
            # 获取考试实例
            exam = get_object_or_404(Exam, pk=request.data.get('exam'))
            
            # 计算答案相似度
            similarity = SequenceMatcher(None, exam.standard_answer, request.data.get('answer')).ratio()
            
            # 根据相似度计算分数（假设满分100分）
            score = round(similarity * 100, 2)
            
            # 添加相似度和分数到请求数据
            request.data['similarity'] = similarity
            request.data['score'] = score
            
            return super().create(request, *args, **kwargs)
            
        except IntegrityError:
            return Response(
                {"error": "该学生已经提交过这门考试的答案"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def query_score(self, request):
        """查询成绩接口"""
        serializer = ScoreQuerySerializer(data=request.data)
        if serializer.is_valid():
            exam_id = serializer.validated_data['exam_id']
            student_name = serializer.validated_data['student_name']
            
            try:
                student_answer = StudentAnswer.objects.get(
                    exam_id=exam_id,
                    student_name=student_name
                )
                return Response({
                    'score': student_answer.score,
                    'similarity': student_answer.similarity
                })
            except StudentAnswer.DoesNotExist:
                return Response(
                    {"error": "未找到该学生的考试记录"},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)