#models.py

from django.db import models
import sqlite3
from django.db import connection


class Exam(models.Model):
    """考试模型"""
    exam_name = models.CharField('考试名称', max_length=100, primary_key=True)
    #question = models.TextField('考试题目')

    #created_at = models.DateTimeField('创建时间', auto_now_add=True)
    #updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '考试'
        verbose_name_plural = verbose_name
        db_table = 'exams_exam'
       # ordering = ['-created_at']

    def __str__(self):
        return self.exam_name

class StudentAnswer(models.Model):
    """学生答案模型"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='考试')
    student_name = models.CharField('学生姓名', max_length=50)
    student_id = models.CharField('学号', max_length=50, blank=True, null=True)
    answer = models.TextField('答案内容')
    score = models.DecimalField('得分', max_digits=5, decimal_places=2, null=True, blank=True)
    similarity = models.FloatField('相似度', null=True, blank=True)
    created_at = models.DateTimeField('提交时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '学生答案'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        unique_together = ['exam', 'student_name']  # 同一考试每个学生只能有一个答案

    def __str__(self):
        return f'{self.exam.exam_name} - {self.student_name}'


def ensure_exam_table(exam_id):
    with connection.cursor() as cursor:
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS exam_{exam_id} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_name TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

# def ensure_answer_table(exam_id):
#     with connection.cursor() as cursor:
#         cursor.execute(f'''
#             CREATE TABLE IF NOT EXISTS student_answer_{exam_id} (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 student_name TEXT NOT NULL,
#                 answer TEXT NOT NULL,
#                 score DECIMAL(5,2),
#                 similarity FLOAT,
#                 created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
#                 UNIQUE(exam_id, student_name)
#             )
#         ''')