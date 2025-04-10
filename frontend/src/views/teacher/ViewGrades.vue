<template>
  <div class="view-grades">
    <el-card class="grades-container">
      <template #header>
        <div class="card-header">
          <h2>成绩查看</h2>
        </div>
      </template>

      <el-table :data="gradesData" style="width: 100%">
        <el-table-column prop="studentName" label="学生姓名" width="120" />
        <el-table-column prop="examName" label="考试名称" width="180" />
        <el-table-column prop="score" label="分数" width="120" />
        <el-table-column prop="submissionTime" label="提交时间" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const gradesData = ref([
  {
    studentName: '张三',
    examName: '期中考试',
    score: 85,
    submissionTime: '2024-03-15 14:30'
  },
  {
    studentName: '李四',
    examName: '期末考试',
    score: 92,
    submissionTime: '2024-06-20 09:45'
  }
])
</script>

<style >
.view-grades {
  padding: 20px;
  min-height: calc(100vh - 60px);
}

.grades-container {
  max-width: 1000px;
  margin: 0 auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.card-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #2c3e50;
}
</style>