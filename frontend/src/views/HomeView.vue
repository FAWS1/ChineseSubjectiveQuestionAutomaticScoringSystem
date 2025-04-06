<template>
  <div class="home">
    <el-card class="home-card">
      <h1 class="system-title">中文主观题自动评分系统</h1>
      <div class="login-options">
        <el-button
          type="primary"
          size="large"
          @click="$router.push('/teacher')"
          :icon="User"
        >
          教师登录
        </el-button>
        <el-button
          type="success"
          size="large"
          @click="$router.push('/student')"
          :icon="Notebook"
        >
          学生登录
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { User, Notebook } from '@element-plus/icons-vue'
</script>

<style scoped>
.home {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
}

.home-card {
  width: 90%;
  max-width: 600px;
  text-align: center;
  padding: 2rem;
}

.system-title {
  font-size: 2rem;
  color: #303133;
  margin-bottom: 3rem;
}

.login-options {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.el-button {
  width: 160px;
  height: 50px;
  font-size: 1.1rem;
}
</style>
