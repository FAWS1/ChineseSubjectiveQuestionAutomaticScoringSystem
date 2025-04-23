from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import Exam, StudentAnswer
import requests
import json


@csrf_exempt
@require_http_methods(["POST"])
def create_exam(request):
    """教师创建考试"""
    try:
        data = json.loads(request.body)
        name = data.get("name")
        question = data.get("question")
        standard_answer = data.get("standard_answer", "")

        exam = Exam.objects.create(
            name=name,
            question=question,
            standard_answer=standard_answer
        )
        return JsonResponse({"message": "考试创建成功", "exam_id": exam.id}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def submit_answer(request):
    """学生提交答案并自动评分"""
    try:
        data = json.loads(request.body)
        exam_id = data.get("exam_id")
        student_name = data.get("student_name")
        answer = data.get("answer")

        exam = Exam.objects.get(id=exam_id)

        # 调用 Flask 自动评分 API
        response = requests.post("http://127.0.0.1:5000/score", json={
            "standard_answer": exam.standard_answer,
            "student_answer": answer
        })
        response.raise_for_status()
        score_data = response.json()

        # 保存学生答案与分数
        StudentAnswer.objects.create(
            exam=exam,
            student_name=student_name,
            answer=answer,
            score=score_data.get("score"),
            similarity=score_data.get("similarity")
        )

        return JsonResponse({"message": "提交成功", "score": score_data.get("score")}, status=200)
    except Exam.DoesNotExist:
        return JsonResponse({"error": "考试不存在"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@require_http_methods(["GET"])
def get_scores(request):
    """教师查看某场考试的全部成绩"""
    try:
        exam_id = request.GET.get("exam_id")
        exam = Exam.objects.get(id=exam_id)
        answers = StudentAnswer.objects.filter(exam=exam)

        result = [
            {
                "student_name": a.student_name,
                "score": a.score,
                "similarity": a.similarity,
                "answer": a.answer
            }
            for a in answers
        ]
        return JsonResponse({"exam": exam.name, "results": result}, status=200)
    except Exam.DoesNotExist:
        return JsonResponse({"error": "考试不存在"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def update_answer(request):
    """学生更新答案（重新评分）"""
    try:
        data = json.loads(request.body)
        exam_id = data.get("exam_id")
        student_name = data.get("student_name")
        new_answer = data.get("answer")

        exam = Exam.objects.get(id=exam_id)
        answer_obj = StudentAnswer.objects.get(exam=exam, student_name=student_name)

        # 调用 Flask 自动评分 API
        response = requests.post("http://127.0.0.1:5000/score", json={
            "standard_answer": exam.standard_answer,
            "student_answer": new_answer
        })
        response.raise_for_status()
        score_data = response.json()

        # 更新数据
        answer_obj.answer = new_answer
        answer_obj.score = score_data.get("score")
        answer_obj.similarity = score_data.get("similarity")
        answer_obj.save()

        return JsonResponse({"message": "答案更新成功", "new_score": answer_obj.score}, status=200)
    except StudentAnswer.DoesNotExist:
        return JsonResponse({"error": "答案记录不存在"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
