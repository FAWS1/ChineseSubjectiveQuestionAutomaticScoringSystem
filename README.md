# 中文主观题自动评分系统

基于BERT的中文主观题自动评分系统，支持考试创建、学生管理、自动评分和成绩分析。

## 项目结构

```
├── frontend/          # Vue.js前端项目
├── backend/           # Django主后端
├── scoring_service/   # Flask评分服务
└── requirements.txt   # Python依赖
```

## 技术栈

- 前端：Vue.js + Element UI
- 后端：Django + Flask
- 数据库：MySQL
- 模型：BERT (bert-base-chinese)

## 主要功能

- 教师端
  - 创建考试
  - 上传答案
  - 自动评分
  - 成绩修改

- 学生端
  - 成绩查询

## 评分机制

- BERT语义相似度计算
- TF-IDF关键词匹配
- 余弦相似度计算