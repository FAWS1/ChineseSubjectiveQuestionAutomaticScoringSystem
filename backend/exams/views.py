#views.py:
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
from django.db.models import Avg, Max, Min
from django.db import transaction




            
# --- UploadAnswers 视图 ---
class ExamViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def create_exam(self, request):
        result = exams_operate.create_exam(request.data)
        return Response(result, status=201 if result['status'] == 'success' else 400)

    @action(detail=False, methods=['post'])
    def submit_answer(self, request):
        result = exams_operate.submit_answer(request.data)
        return Response(result, status=200 if result['status'] == 'success' else 400)

    @action(detail=False, methods=['get'])
    def get_scores(self, request):
        exam_id = request.query_params.get('exam_id')
        result = exams_operate.get_scores(exam_id)
        return Response(result, status=200 if result['status'] == 'success' else 400)

    @action(detail=False, methods=['post'])
    def update_answer(self, request):
        result = exams_operate.update_answer(request.data)
        return Response(result, status=200 if result['status'] == 'success' else 400)

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
                # 获取考试信息
                exam = get_object_or_404(Exam, exam_name=exam_id)
                
                # 构造动态表名
                table_name = f"exam_{exam.exam_name.strip().replace(' ', '_')}_answers"
                print(f"使用的表名: {table_name}")  # 添加日志以便调试
                
                # 读取Excel文件
                df = pd.read_excel(file_obj)
                
                # 检查是否有列名映射信息
                column_mapping_str = request.POST.get('column_mapping')
                if column_mapping_str:
                    try:
                        import json
                        column_mapping = json.loads(column_mapping_str)
                        # 重命名列以匹配后端期望的格式
                        df = df.rename(columns=column_mapping)
                    except Exception as e:
                        print(f"列名映射解析错误: {str(e)}")
                
                # 检查必要的列是否存在
                required_columns = ['学生姓名', '学号', '答案']
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    return Response({
                        'error': f'文件格式错误，缺少必要的列: {", ".join(missing_columns)}。请确保Excel文件包含以下列：学生姓名、学号、答案'
                    }, status=400)
                
                # 使用事务确保数据一致性
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        # 对每一行数据进行处理
                        for _, row in df.iterrows():
                            # 构建插入动态表的SQL语句
                            sql = f"""
                            INSERT INTO `{table_name}` 
                            (student_id, student_name, student_answer, created_at) 
                            VALUES (%s, %s, %s, NOW())
                            """
                            
                            # 执行SQL插入数据
                            cursor.execute(sql, [
                                row['学号'],
                                row['学生姓名'],
                                row['答案']
                            ])
                            
                return Response({'message': '批量上传成功'})
            except Exception as e:
                return Response({'error': str(e)}, status=500)

        # GET 请求的处理
        else:
            return Response({
                'message': 'GET 请求时返回批量上传表单。',
            })

# --- CreateExams 视图 ---
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction, connection
from .models import Exam
from .serializers import ExamSerializer

class CreateExams(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        """获取所有考试列表"""
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"获取考试列表错误: {str(e)}")
            return Response({"error": f"获取考试列表失败: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        print("收到的请求数据：", request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("验证错误详情:", serializer.errors)
            return Response({"error": "数据验证失败", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        exam_name = serializer.validated_data.get('exam_name')

        if not exam_name:
            return Response({"error": "考试名称不能为空"}, status=status.HTTP_400_BAD_REQUEST)

        # 构造表名，确保命名合法（不含空格等非法字符）
        table_name = f"exam_{exam_name.strip().replace(' ', '_')}_answers"

        try:
            with transaction.atomic():
                # 创建考试记录
                exam = serializer.save()

                # 创建对应答案表
                self.create_answer_table(table_name)

                return Response({
                    "message": "考试创建成功，答案表已建立",
                    "exam_id": exam.id,
                    "table_name": table_name
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"创建失败: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create_answer_table(self, table_name):
        """创建学生答案表"""
        sql = f'''
            CREATE TABLE IF NOT EXISTS `{table_name}` (
                student_id VARCHAR(50) NOT NULL,
            student_name VARCHAR(100) NOT NULL,
            student_answer TEXT NOT NULL,
            keywords_score FLOAT DEFAULT 0,
            similarity_score FLOAT DEFAULT 0,
            final_score FLOAT DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        '''
        print(f"SQL to be executed: {sql}")  # 打印出 SQL 查询

        with connection.cursor() as cursor:
            cursor.execute(sql)  # 执行 SQL 语句


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