<template>
  <div class="teacher-home">
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="welcome-section">
          <h1>欢迎使用中文主观题自动评分系统</h1>
          <p>您已登录为教师账号</p>
        </div>
      </el-col>
    </el-row>
    
    <el-row :gutter="10" class="feature-cards">
      <el-col :xs="24" :sm="12" :md="9">
        <el-card class="feature-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><Document /></el-icon>
              <span>创建考试</span>
            </div>
          </template>
          <div class="card-content">
            <p>创建新的考试，设置考试题目和参数</p>
            <el-button type="primary" @click="router.push('/teacher/create-exam')">开始创建</el-button>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="9">
        <el-card class="feature-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><Upload /></el-icon>
              <span>上传答案</span>
            </div>
          </template>
          <div class="card-content">
            <p>上传标准答案和学生答案</p>
            <el-button type="primary" @click="router.push('/teacher/upload-answers')">去上传</el-button>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="9">
        <el-card class="feature-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><Check /></el-icon>
              <span>自动评分</span>
            </div>
          </template>
          <div class="card-content">
            <p>自动评分</p>
            <el-button type="primary" @click="router.push('/teacher/auto-scoring')">开始评分</el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="9">
        <el-card class="feature-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><Check /></el-icon>
              <span>查看成绩</span>
            </div>
          </template>
          <div class="card-content">
            <p>查看和分析学生考试成绩</p>
            
            <el-button type="primary" @click="router.push({ name: 'ViewGrades' })">查看成绩</el-button>

          </div>
        </el-card>
      </el-col>

      
    </el-row>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { Document, Upload, Check } from '@element-plus/icons-vue'

const router = useRouter()
</script>

<style>
.teacher-home {
  padding: 0;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  margin: 20px 0 40px;
  padding: 0 20px;
}

.welcome-section h1 {
  font-size: 24px;
  color: #303133;
  margin-bottom: 10px;
}

.welcome-section p {
  font-size: 16px;
  color: #606266;
}

.feature-cards {
  margin: 0;
  padding: 0 20px;
  display: flex;
  flex-wrap: wrap;
}

.feature-card {
  margin-bottom: 24px;
  transition: all 0.3s;
  height: 100%;
}

.card-header {
  display: flex;
  align-items: center;
  font-size: 18px;
}

.card-header .el-icon {
  margin-right: 12px;
  font-size: 20px;
}

.card-content {
  text-align: center;
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 150px;
}

.card-content p {
  margin: 0;
  color: #606266;
  font-size: 15px;
}
</style>