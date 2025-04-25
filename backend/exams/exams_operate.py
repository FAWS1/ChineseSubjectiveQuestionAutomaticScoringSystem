from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import Exam, StudentAnswer
import requests
import json


def create_exam(exam_data):
    """创建考试核心逻辑"""
    try:
        exam_name = exam_data.get("exam_name")
        exam_id = str(uuid.uuid4())
        
        from .models import ensure_exam_table
        ensure_exam_table(exam_id)
        
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO exam_%s (exam_name) VALUES (%%s)", 
                [exam_id, exam_name]
            )
        
        return {"status": "success", "exam_id": exam_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def submit_answer(answer_data):
    """提交答案核心逻辑"""
    try:
        exam_id = answer_data.get("exam_id")
        student_name = answer_data.get("student_name")
        answer = answer_data.get("answer")

        exam = Exam.objects.get(id=exam_id)

        # 调用评分服务
        response = requests.post("http://127.0.0.1:5000/score", json={
            "student_answer": answer
        })
        response.raise_for_status()
        score_data = response.json()

        # 保存答案
        StudentAnswer.objects.create(
            exam=exam,
            student_name=student_name,
            answer=answer,
            score=score_data.get("score"),
            similarity=score_data.get("similarity")
        )

        return {"status": "success", "score": score_data.get("score")}
    except Exam.DoesNotExist:
        return {"status": "error", "message": "考试不存在"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_scores(exam_id):
    """获取考试成绩核心逻辑"""
    try:
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
        return {"status": "success", "results": result, "exam_name": exam.exam_name}
    except Exam.DoesNotExist:
        return {"status": "error", "message": "考试不存在"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def update_answer(update_data):
    """更新答案核心逻辑"""
    try:
        exam_id = update_data.get("exam_id")
        student_name = update_data.get("student_name")
        new_answer = update_data.get("answer")

        exam = Exam.objects.get(id=exam_id)
        answer_obj = StudentAnswer.objects.get(exam=exam, student_name=student_name)

        response = requests.post("http://127.0.0.1:5000/score", json={
            "student_answer": new_answer
        })
        response.raise_for_status()
        score_data = response.json()

        answer_obj.answer = new_answer
        answer_obj.score = score_data.get("score")
        answer_obj.similarity = score_data.get("similarity")
        answer_obj.save()

        return {"status": "success", "new_score": answer_obj.score}
    except StudentAnswer.DoesNotExist:
        return {"status": "error", "message": "答案记录不存在"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
