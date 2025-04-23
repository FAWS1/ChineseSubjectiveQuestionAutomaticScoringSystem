#auth_serializers.py
from rest_framework import serializers
from .auth_models import TeacherAuth, StudentAuth
from django.contrib.auth.models import User

class TeacherAuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = TeacherAuth
        fields = ['id', 'username', 'password', 'email', 'phone']
    
    def create(self, validated_data):
        teacher = TeacherAuth(**validated_data)
        teacher.set_password(validated_data['password'])
        teacher.save()
        return teacher

class StudentAuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = StudentAuth
        fields = ['id', 'username', 'password', 'email', 'phone']
    
    def create(self, validated_data):
        student = StudentAuth(**validated_data)
        student.set_password(validated_data['password'])
        student.save()
        return student

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone']
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    role = serializers.ChoiceField(choices=['teacher', 'student'])