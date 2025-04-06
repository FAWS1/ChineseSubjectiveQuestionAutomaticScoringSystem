<template>
  <div class="teacher-dashboard">
    <el-container>
      <el-aside width="200px">
        <el-menu
          :router="true"
          class="el-menu-vertical"
          default-active="/teacher/create-exam"
        >
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
        </el-menu>
      </el-aside>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { Document, Upload, Check } from '@element-plus/icons-vue'
</script>

<style scoped>
.teacher-dashboard {
  height: 100vh;
}

.el-container {
  height: 100%;
}

.el-aside {
  background-color: #304156;
  color: #fff;
}

.el-menu {
  border-right: none;
}

.el-menu-vertical {
  height: 100%;
}

.el-main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>