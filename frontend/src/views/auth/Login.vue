<template>
  <div class="login-page">
    <el-card class="login-card">
      <h2>{{ role === 'teacher' ? '教师登录' : '学生登录' }}</h2>
      <el-form @submit.prevent="handleLogin" :label-width="80" style="width: 100%">
        <el-form-item label="用户名" style="margin-bottom: 20px">
          <el-input v-model="username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" style="margin-bottom: 20px">
          <el-input type="password" v-model="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item style="margin-bottom: 0; text-align: center">
          <el-button type="primary" @click="handleLogin" style="width: 100%">登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const username = ref('')
const password = ref('')
const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 从路由的查询参数获取角色，默认为教师
const role = computed(() => {
  const path = route.query.role
  return path === 'student' ? 'student' : 'teacher'
})

// 登录请求
const handleLogin = async () => {
  if (username.value && password.value) {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/auth/login/', {  // 后端登录接口
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username.value,
          password: password.value,
          role: role.value,  // 角色信息
        }),
      });
      
      if (response.ok) {
        const data = await response.json();
        // 登录成功，存储 token 和用户信息
        authStore.login(username.value, role.value === 'teacher', data.token);
        ElMessage.success('登录成功');
        router.push(role.value === 'teacher' ? '/teacher' : '/student'); // 跳转到不同的页面
      } else {
        ElMessage.error('用户名或密码错误');
      }
    } catch (error) {
      ElMessage.error('登录失败，请重试');
    }
  } else {
    ElMessage.error('请输入用户名和密码');
  }
}
</script>

<style scoped>
.login-page {
  width: 100vw;
  height: 100vh;
  background: linear-gradient(to bottom right, #f0f4ff, #ffffff);
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  background: #fff;
  padding: 40px 60px;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  text-align: center;
  min-width: 320px;
  max-width: 420px;
  width: 100%;
}

.title {
  font-size: 24px;
  font-weight: 600;
  color: #409EFF;
  margin-bottom: 32px;
}
</style>
