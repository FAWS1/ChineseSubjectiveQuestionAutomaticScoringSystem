<template>
  <div class="student-home">
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="welcome-section">
          <h1>欢迎使用中文主观题自动评分系统</h1>
          <p>您已登录为学生账号</p>
        </div>
      </el-col>
    </el-row>
    
    <el-row :gutter="24" class="feature-cards">
      <el-col :xs="24" :sm="12" :md="8" :lg="8">
        <el-card class="feature-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><Document /></el-icon>
              <span>成绩查询</span>
            </div>
          </template>
          <div class="card-content">
            <p>查看您的考试成绩和评分</p>
            <div class="button-wrapper">
              <el-button type="primary" @click="router.push('/student/view-scores')">查看成绩</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="8" :lg="8">
        <el-card class="feature-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><Search /></el-icon>
              <span>成绩分析</span>
            </div>
          </template>
          <div class="card-content">
            <p>查看成绩统计和分析报告</p>
            <div class="button-wrapper">
              <el-button type="primary" @click="router.push('/student/score-analysis')">查看分析</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { Document, Search } from '@element-plus/icons-vue'

const router = useRouter()
</script>

<style >
.student-home {
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
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 120px;
}

.card-content p {
  margin-bottom: 16px;
  flex-grow: 1;
}

.button-wrapper {
  display: flex;
  justify-content: center;
  margin-top: auto;
}

.button-wrapper .el-button {
  min-width: 120px;
}

.card-content {
  text-align: center;
  padding: 20px 0;
}

.card-content p {
  margin: 16px 0 24px;
  color: #606266;
  font-size: 15px;
}
</style>