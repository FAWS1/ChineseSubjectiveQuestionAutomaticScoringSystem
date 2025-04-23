#vews.py:
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Exam, StudentAnswer
from .serializers import ExamSerializer, StudentAnswerSerializer, ScoreQuerySerializer
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from difflib import SequenceMatcher
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
import pandas as pd
import logging

class CreateExams(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            exam = serializer.save(teacher=self.request.user)  # 保存考试并关联教师
            # 如果创建成功，返回成功响应
            return Response(
                {"message": "考试创建成功", "exam_id": exam.id},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            # 如果出现错误，返回失败响应
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

            
# --- UploadAnswers 视图 ---
class UploadAnswers(viewsets.ModelViewSet):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def perform_create(self, serializer):
        try:
            exam_id = self.request.data.get('exam_id')
            exam = get_object_or_404(Exam, id=exam_id)
            answer = serializer.save(
                student=self.request.user,
                exam=exam
            )
            return Response({"message": "答案提交成功"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'post'])
    def upload_batch(self, request):
        """批量上传学生答案"""
        if request.method == 'POST':
            exam_id = request.POST.get('examId')
            file_obj = request.FILES.get('file')

            if not exam_id or not file_obj:
                return Response({'error': '缺少参数'}, status=400)

            try:
                exam = get_object_or_404(Exam, id=exam_id)
                df = pd.read_excel(file_obj)

                for _, row in df.iterrows():
                    StudentAnswer.objects.create(
                        exam=exam,
                        student_name=row['学生姓名'],
                        student_id=row['学号'],
                        answer=row['答案']
                    )
                return Response({'message': '批量上传成功'})
            except Exception as e:
                return Response({'error': str(e)}, status=500)

        # GET 请求的处理
        else:
            return Response({
                'message': 'GET 请求时返回批量上传表单。',
            })

# --- CreateExams 视图 ---
class CreateExams(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            exam = serializer.save(teacher=self.request.user)
            return Response({"message": "考试创建成功", "exam_id": exam.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'post'])
    def create_exam_form(self, request):
        """显示考试创建表单"""
        if request.method == 'POST':
            # 处理考试创建逻辑
            return Response({'message': '考试创建成功'})

        # GET 请求时显示一个表单
        return Response({
            'message': 'GET 请求时返回创建考试表单。',
        })


class ViewScores(viewsets.ReadOnlyModelViewSet):
    serializer_class = StudentAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """根据用户角色返回成绩列表"""
        if hasattr(self.request.user, 'is_teacher') and self.request.user.is_teacher:
            return StudentAnswer.objects.all().select_related('exam', 'student')
        return StudentAnswer.objects.filter(student=self.request.user).select_related('exam')

    @action(detail=False, methods=['get', 'post'])
    def query_score(self, request):
        """查询成绩接口，同时支持 GET 和 POST 请求"""
        if request.method == 'GET':
            # GET 请求方式，用户直接传递 query 参数查询成绩
            exam_id = request.query_params.get('exam_id')
            student_name = request.query_params.get('student_name')
            if not exam_id or not student_name:
                return Response({'error': '缺少必要的参数 (exam_id, student_name)'}, status=status.HTTP_400_BAD_REQUEST)
            
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

        elif request.method == 'POST':
            # POST 请求方式，使用序列化器来验证请求数据
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

class AnalysisScores(viewsets.ReadOnlyModelViewSet):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get', 'post'])
    def statistics(self, request):
        if request.method == 'GET':
            return self.get_statistics(request)
        elif request.method == 'POST':
            return self.post_statistics(request)

    def get_statistics(self, request):
        """处理 GET 请求，基于查询参数获取统计信息"""
        exam_id = request.query_params.get('exam_id')
        if not exam_id:
            return Response({'error': '需要提供考试ID'}, status=status.HTTP_400_BAD_REQUEST)

        answers = StudentAnswer.objects.filter(exam_id=exam_id)
        total = answers.count()

        if total == 0:
            return Response({
                'total_students': total,
                'average_score': None,
                'highest_score': None,
                'lowest_score': None,
                'average_bert_score': None,
                'average_keyword_score': None,
                'score_distribution': {},
                'pass_rate': 0,
                'excellent_rate': 0
            })

        stats = answers.aggregate(
            avg_score=Avg('final_score'),
            max_score=Max('final_score'),
            min_score=Min('final_score'),
            avg_bert_score=Avg('bert_score'),
            avg_keyword_score=Avg('keyword_score')
        )

        score_ranges = {
            '优秀(90-100)': answers.filter(final_score__gte=90).count(),
            '良好(80-89)': answers.filter(final_score__gte=80, final_score__lt=90).count(),
            '中等(70-79)': answers.filter(final_score__gte=70, final_score__lt=80).count(),
            '及格(60-69)': answers.filter(final_score__gte=60, final_score__lt=70).count(),
            '不及格(<60)': answers.filter(final_score__lt=60).count()
        }

        pass_rate = (answers.filter(final_score__gte=60).count() / total) * 100 if total > 0 else 0
        excellent_rate = (answers.filter(final_score__gte=90).count() / total) * 100 if total > 0 else 0

        return Response({
            'total_students': total,
            'average_score': stats['avg_score'],
            'highest_score': stats['max_score'],
            'lowest_score': stats['min_score'],
            'average_bert_score': stats['avg_bert_score'],
            'average_keyword_score': stats['avg_keyword_score'],
            'score_distribution': score_ranges,
            'pass_rate': pass_rate,
            'excellent_rate': excellent_rate
        })

    def post_statistics(self, request):
        """处理 POST 请求，基于请求体数据获取统计信息"""
        exam_id = request.data.get('exam_id')
        if not exam_id:
            return Response({'error': '需要提供考试ID'}, status=status.HTTP_400_BAD_REQUEST)

        answers = StudentAnswer.objects.filter(exam_id=exam_id)
        total = answers.count()

        if total == 0:
            return Response({
                'total_students': total,
                'average_score': None,
                'highest_score': None,
                'lowest_score': None,
                'average_bert_score': None,
                'average_keyword_score': None,
                'score_distribution': {},
                'pass_rate': 0,
                'excellent_rate': 0
            })

        stats = answers.aggregate(
            avg_score=Avg('final_score'),
            max_score=Max('final_score'),
            min_score=Min('final_score'),
            avg_bert_score=Avg('bert_score'),
            avg_keyword_score=Avg('keyword_score')
        )

        score_ranges = {
            '优秀(90-100)': answers.filter(final_score__gte=90).count(),
            '良好(80-89)': answers.filter(final_score__gte=80, final_score__lt=90).count(),
            '中等(70-79)': answers.filter(final_score__gte=70, final_score__lt=80).count(),
            '及格(60-69)': answers.filter(final_score__gte=60, final_score__lt=70).count(),
            '不及格(<60)': answers.filter(final_score__lt=60).count()
        }

        pass_rate = (answers.filter(final_score__gte=60).count() / total) * 100 if total > 0 else 0
        excellent_rate = (answers.filter(final_score__gte=90).count() / total) * 100 if total > 0 else 0

        return Response({
            'total_students': total,
            'average_score': stats['avg_score'],
            'highest_score': stats['max_score'],
            'lowest_score': stats['min_score'],
            'average_bert_score': stats['avg_bert_score'],
            'average_keyword_score': stats['avg_keyword_score'],
            'score_distribution': score_ranges,
            'pass_rate': pass_rate,
            'excellent_rate': excellent_rate
        })


class AutoScoring(viewsets.ModelViewSet):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get', 'post'])
    def score_bert(self, request, pk=None):
        """使用BERT模型进行评分"""
        if request.method == 'POST':
            try:
                logger.info("Received request for BERT scoring: %s", request.data)
                answer = self.get_object()
                response = requests.post("http://127.0.0.1:5000/bert_score", json={
                    "standard_answer": answer.exam.standard_answer,
                    "student_answer": answer.answer
                })
                response.raise_for_status()
                score_data = response.json()

                answer.bert_similarity = score_data.get("similarity")
                answer.bert_score = score_data.get("score")
                answer.save()

                logger.info("BERT scoring completed: %s", score_data)
                return Response({
                    'bert_score': answer.bert_score,
                    'bert_similarity': answer.bert_similarity
                })
            except Exception as e:
                logger.error("Error during BERT scoring: %s", str(e))
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # GET 请求的处理
        else:
            return Response({
                'message': 'GET 请求时显示BERT评分的相关信息或表单。',
            })

    @action(detail=True, methods=['get', 'post'])
    def score_keywords(self, request, pk=None):
        """使用关键词匹配进行评分"""
        if request.method == 'POST':
            try:
                logger.info("Received request for keyword scoring: %s", request.data)
                answer = self.get_object()
                response = requests.post("http://127.0.0.1:5000/keyword_score", json={
                    "standard_answer": answer.exam.standard_answer,
                    "student_answer": answer.answer,
                    "keywords": answer.exam.keywords
                })
                response.raise_for_status()
                score_data = response.json()

                answer.keyword_match = score_data.get("keyword_match")
                answer.keyword_score = score_data.get("score")
                answer.save()

                logger.info("Keyword scoring completed: %s", score_data)
                return Response({
                    'keyword_score': answer.keyword_score,
                    'keyword_match': answer.keyword_match
                })
            except Exception as e:
                logger.error("Error during keyword scoring: %s", str(e))
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # GET 请求的处理
        else:
            return Response({
                'message': 'GET 请求时显示关键词评分的相关信息或表单。',
            })

    @action(detail=True, methods=['get', 'post'])
    def score_combined(self, request, pk=None):
        """综合BERT和关键词评分"""
        if request.method == 'POST':
            try:
                logger.info("Received request for combined scoring: %s", request.data)
                answer = self.get_object()
                # 获取BERT评分
                bert_response = requests.post("http://127.0.0.1:5000/bert_score", json={
                    "standard_answer": answer.exam.standard_answer,
                    "student_answer": answer.answer
                })
                bert_data = bert_response.json()

                # 获取关键词评分
                keyword_response = requests.post("http://127.0.0.1:5000/keyword_score", json={
                    "standard_answer": answer.exam.standard_answer,
                    "student_answer": answer.answer,
                    "keywords": answer.exam.keywords
                })
                keyword_data = keyword_response.json()

                # 计算综合得分（可以根据需要调整权重）
                bert_weight = 0.7
                keyword_weight = 0.3

                answer.final_score = (
                    bert_weight * bert_data.get("score") +
                    keyword_weight * keyword_data.get("score")
                )
                answer.save()

                logger.info("Combined scoring completed: BERT %s, Keyword %s", bert_data, keyword_data)
                return Response({
                    'final_score': answer.final_score,
                    'bert_score': bert_data.get("score"),
                    'keyword_score': keyword_data.get("score")
                })
            except Exception as e:
                logger.error("Error during combined scoring: %s", str(e))
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # GET 请求的处理
        else:
            return Response({
                'message': 'GET 请求时显示综合评分的相关信息或表单。',
            })

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