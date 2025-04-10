<template>
  <div class="manage-exam-container">
    <h2>考试管理页面</h2>
    <el-alert type="info" show-icon>
      当前考试列表加载中...
    </el-alert>
  </div>
</template>

<script lang="ts">
export default {
  name: 'ManageExam'
}
</script>

<style>
.manage-exam-container {
  padding: 20px;
}
</style>