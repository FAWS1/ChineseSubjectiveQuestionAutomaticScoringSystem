#models.py

from django.db import models


class Exam(models.Model):
    """考试模型"""
    name = models.CharField('考试名称', max_length=100)
    question = models.TextField('考试题目')
    standard_answer = models.TextField('标准答案', blank=True)
    keywords = models.TextField('关键词', blank=True, help_text='多个关键词用逗号分隔')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '考试'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class StudentAnswer(models.Model):
    """学生答案模型"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name='考试')
    student_name = models.CharField('学生姓名', max_length=50)
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
        return f'{self.exam.name} - {self.student_name}'