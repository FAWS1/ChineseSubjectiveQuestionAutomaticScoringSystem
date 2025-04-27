<template>
  <div class="teacher-dashboard">
    <el-container>
      <el-aside width="240px" class="aside">
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
            <el-menu-item index="/teacher/view-grades">
              <el-icon><TrendCharts /></el-icon>
              <span>查看成绩</span>
            </el-menu-item>
            <el-menu-item index="/teacher/exam-table">
              <el-icon><Document /></el-icon>
              <span>考试表单</span>
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
          <div class="router-view-wrapper">
            <router-view />
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Document, Upload, Check, UserFilled, SwitchButton, HomeFilled, TrendCharts } from '@element-plus/icons-vue'
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
    '/teacher/auto-scoring': '自动评分',
    '/teacher/view-grades': '查看成绩',
    '/teacher/exam-table': '考试表单'
  }
  return routeMap[route.path] || '首页'
})

const handleLogout = () => {
  store.logout()
  ElMessage.success('已退出登录')
  router.push('/')
}
</script>

<style scoped>
.teacher-dashboard {
  height: 100vh;
  overflow: hidden;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  --primary-color: #409EFF;
  --side-width: 240px;
}

.el-container {
  height: 100%;
}

.aside {
  background-color: #001529;
  color: #fff;
  transition: width 0.3s;
  width: var(--side-width) !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  z-index: 1000;
}

.dashboard-logo {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  background-color: #001529;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-img {
  width: 32px;
  height: 32px;
  margin-right: 12px;
  filter: drop-shadow(0 0 2px rgba(255, 255, 255, 0.2));
}

.logo-text {
  color: #ffffff;
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 1px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.el-menu {
  border-right: none;
}

.el-menu-vertical {
  height: calc(100% - 60px);
  display: flex;
  flex-direction: column;
  background-color: #001529 !important;
}

.menu-content {
  flex: 1;
}

.logout-button-container {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: auto;
}

.dashboard-header {
  background-color: #ffffff;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  position: relative;
  z-index: 900;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-profile:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.user-name {
  margin-left: 8px;
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.dashboard-main {
  background-color: #f4f6f9;
  padding: 20px;
  height: calc(100vh - 60px);
  overflow: hidden;
  position: relative;
}

.router-view-wrapper {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  background-color: transparent;
  padding: 0;
  box-sizing: border-box;
  scroll-behavior: smooth;
}

.el-menu-item {
  height: 52px;
  line-height: 52px;
  margin: 4px 0;
  border-radius: 4px;
  margin-left: 8px;
  margin-right: 8px;
  padding-left: 16px !important;
}

.el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

.el-menu-item.is-active {
  background-color: var(--primary-color) !important;
  color: white !important;
  font-weight: 500;
}

.el-menu-item .el-icon {
  margin-right: 10px;
  font-size: 18px;
}

.el-breadcrumb {
  font-size: 14px;
}

@media (max-width: 768px) {
  .aside {
    position: fixed;
    height: 100%;
    transform: translateX(-100%);
    transition: transform 0.3s;
    z-index: 1001;
  }
  
  .aside.is-open {
    transform: translateX(0);
  }
  
  .dashboard-header {
    padding: 0 10px;
  }
  
  .dashboard-main {
    padding: 10px;
  }
}
</style>
