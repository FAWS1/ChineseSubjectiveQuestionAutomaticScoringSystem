from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class TeacherAuth(models.Model):
    """教师认证模型"""
    username = models.CharField('用户名', max_length=50, unique=True)
    password = models.CharField('密码', max_length=128)
    email = models.EmailField('邮箱', max_length=254, blank=True)
    phone = models.CharField('手机号', max_length=11, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '教师认证'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class StudentAuth(models.Model):
    """学生认证模型"""
    username = models.CharField('用户名', max_length=50, unique=True)
    password = models.CharField('密码', max_length=128)
    email = models.EmailField('邮箱', max_length=254, blank=True)
    phone = models.CharField('手机号', max_length=11, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '学生认证'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)