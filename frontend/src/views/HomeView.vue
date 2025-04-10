<template>
  <div class="login-page">
    <div class="login-card">
      <h1 class="title">中文主观题自动评分系统</h1>
      <div class="button-group">
        <el-button type="primary" icon="User" @click="loginAsTeacher">教师登录</el-button>
        <el-button type="success" icon="Notebook" @click="loginAsStudent">学生登录</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const loginAsTeacher = () => {
  router.push('/login?role=teacher')
}
const loginAsStudent = () => {
  router.push('/login?role=student')
}
</script>

<style >
.login-page {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: linear-gradient(to bottom right, #f0f4ff, #ffffff);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 20px;
  box-sizing: border-box;
}

.login-card {
  width: 100%;
  max-width: 480px;
  background: #fff;
  padding: 48px 40px;
  border-radius: 16px;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.title {
  font-size: 28px;
  font-weight: 600;
  color: #409EFF;
  margin-bottom: 32px;
}

.button-group {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}


</style>
