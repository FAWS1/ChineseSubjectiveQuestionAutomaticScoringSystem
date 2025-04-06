<template>
  <div class="student-dashboard">
    <el-container>
      <el-aside width="200px">
        <el-menu
          :router="true"
          class="el-menu-vertical"
          default-active="/student/view-scores"
        >
          <el-menu-item index="/student/view-scores">
            <el-icon><Document /></el-icon>
            <span>查看成绩</span>
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
import { Document } from '@element-plus/icons-vue'
</script>

<style scoped>
.student-dashboard {
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