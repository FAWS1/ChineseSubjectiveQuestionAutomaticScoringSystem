#ManageExam.vue
<template>
  <div class="manage-exam-container">
    <h2>考试管理页面</h2>
    <el-alert v-if="examStore.examList.length === 0" type="info" show-icon>
      当前考试列表加载中...
    </el-alert>
    <el-table :data="examStore.examList" style="width: 100%">
      <el-table-column prop="name" label="考试名称" width="180" />
      <el-table-column prop="question" label="考试题目" width="300" />
      <el-table-column prop="created_at" label="创建时间" />
    </el-table>
  </div>
</template>

<script lang="ts">
import { onMounted } from 'vue'
import { useExamStore } from '@/stores/exam'

export default {
  name: 'ManageExam',
  setup() {
    const examStore = useExamStore()

    onMounted(() => {
      examStore.fetchExams()  // 组件加载时获取考试列表
    })

    return {
      examStore
    }
  }
}
</script>

<style>
.manage-exam-container {
  padding: 20px;
}
</style>
