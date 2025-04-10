<template>
  <div class="teacher-dashboard">
    <el-container>
      <el-aside width="240px">
        <div class="dashboard-logo">
          <img src="/logo.svg" alt="Logo" class="logo-img" />
          <span class="logo-text">教师管理系统</span>
        </div>
        <el-menu
          :router="true"
          class="el-menu-vertical"
          default-active="/teacher"
          background-color="#1e1e2d"
          text-color="#a2a3b7"
          active-text-color="#ffffff"
        >
          <div class="menu-content">
          <el-menu-item index="/teacher">
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/teacher/create-exam">
            <el-icon><Document /></el-icon>
            <span>创建考试</span>
          </el-menu-item>
          <el-menu-item index="/teacher/upload-answers">
            <el-icon><Upload /></el-icon>
            <span>上传答案</span>
          </el-menu-item>
          <el-menu-item index="/teacher/auto-scoring">
            <el-icon><Check /></el-icon>
            <span>自动评分</span>
          </el-menu-item>
          </div>
          <div class="logout-button-container">
            <el-menu-item @click="handleLogout">
              <el-icon><SwitchButton /></el-icon>
              <span>退出登录</span>
            </el-menu-item>
          </div>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header height="60px" class="dashboard-header">
          <div class="header-left">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/teacher' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item>{{ currentRoute }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          <div class="header-right">
            <el-dropdown trigger="click">
              <span class="user-profile">
                <el-avatar :size="32" icon="UserFilled" />
                <span class="user-name">{{ userName }}</span>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        <el-main class="dashboard-main">
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Document, Upload, Check, UserFilled, SwitchButton, HomeFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useStore } from '@/stores'


const router = useRouter()
const route = useRoute()
const store = useStore()

const userName = computed(() => store.user?.username || '教师')

const currentRoute = computed(() => {
  const routeMap = {
    '/teacher/create-exam': '创建考试',
    '/teacher/upload-answers': '上传答案',
    '/teacher/auto-scoring': '自动评分'
  }
  return routeMap[route.path] || '首页'
})

const handleLogout = () => {
  store.logout()
  ElMessage.success('已退出登录')
  router.push('/')
}
</script>

<style >
.teacher-dashboard {
  height: 100vh;
}

.el-container {
  height: 100%;
}

.el-aside {
  background-color: #1e1e2d;
  color: #fff;
  transition: width 0.3s;
}

.dashboard-logo {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  background-color: #1b1b28;
}

.logo-img {
  width: 32px;
  height: 32px;
  margin-right: 8px;
}

.logo-text {
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
}

.el-menu {
  border-right: none;
}

.el-menu-vertical {
  height: calc(100% - 60px);
  display: flex;
  flex-direction: column;
}

.menu-content {
  flex: 1;
}

.logout-button-container {
  border-top: 1px solid #2d2d3f;
}

.dashboard-header {
  background-color: #ffffff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.user-name {
  margin-left: 8px;
  font-size: 14px;
  color: #606266;
}

.dashboard-main {
  background-color: #f6f6f6;
  padding: 20px;
  height: calc(100vh - 60px);
  overflow-y: auto;
}

.el-menu-item {
  &:hover {
    background-color: #2d2d3f !important;
  }
  &.is-active {
    background-color: #2d2d3f !important;
  }
}
</style>