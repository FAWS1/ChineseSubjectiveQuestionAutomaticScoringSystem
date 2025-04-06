# 系统备份信息

## 项目结构
- frontend/: Vue.js前端项目
  - 使用Vue 3 + TypeScript
  - Element Plus UI组件库
  - Vite构建工具
  - 主要功能：学生查看成绩界面

- backend/: Django后端项目
  - Django 4.2.7
  - Django REST Framework
  - MySQL数据库
  - 主要模块：考试管理、成绩评估

## 依赖版本
### 后端主要依赖
- Django==4.2.7
- django-cors-headers==4.3.0
- mysqlclient==2.2.0
- django-rest-framework==3.14.0
- pandas==2.1.3
- numpy==1.26.2
- transformers==4.35.2
- torch==2.1.1
- scikit-learn==1.3.2

## 数据库信息
- 类型：MySQL
- 主要表：
  - exams: 存储考试信息
  - student_answers: 存储学生答案
  - scores: 存储评分结果

## 备份时间
备份创建时间：2024年1月8日

## 注意事项
1. 确保MySQL数据库定期备份
2. 前端构建前需要安装node_modules
3. 后端需要配置正确的数据库连接信息
4. 评分服务依赖于预训练模型