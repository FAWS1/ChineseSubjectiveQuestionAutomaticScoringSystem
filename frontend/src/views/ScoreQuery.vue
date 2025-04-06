<template>
  <div class="score-query">
    <div class="query-container">
      <h2>成绩查询</h2>
      <div class="form-group">
        <label for="examId">考试编号：</label>
        <input
          v-model="examId"
          type="number"
          id="examId"
          placeholder="请输入考试编号"
        >
      </div>
      <div class="form-group">
        <label for="studentName">学生姓名：</label>
        <input
          v-model="studentName"
          type="text"
          id="studentName"
          placeholder="请输入你的姓名"
        >
      </div>
      <button @click="queryScore" :disabled="querying" class="query-btn">
        {{ querying ? '查询中...' : '查询成绩' }}
      </button>

      <div v-if="scoreResult" class="score-result">
        <h3>查询结果</h3>
        <div class="result-content">
          <div class="result-item">
            <span class="label">得分：</span>
            <span class="value">{{ scoreResult.score }}</span>
          </div>
          <div class="result-item">
            <span class="label">答案相似度：</span>
            <span class="value">{{ (scoreResult.similarity * 100).toFixed(2) }}%</span>
          </div>
        </div>
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const examId = ref('')
const studentName = ref('')
const querying = ref(false)
const scoreResult = ref(null)
const error = ref('')

const queryScore = async () => {
  if (!examId.value || !studentName.value) {
    error.value = '请填写完整的考试编号和学生姓名'
    return
  }

  error.value = ''
  scoreResult.value = null
  querying.value = true

  try {
    const response = await axios.post('http://localhost:8000/api/student-answers/query_score/', {
      exam_id: examId.value,
      student_name: studentName.value
    })
    scoreResult.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.error || '查询失败，请稍后重试'
  } finally {
    querying.value = false
  }
}
</script>

<style scoped>
.score-query {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.query-container {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.query-btn {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
  width: 100%;
}

.query-btn:hover {
  background-color: #1565c0;
}

.query-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.score-result {
  margin-top: 30px;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 4px;
}

.result-content {
  margin-top: 15px;
}

.result-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #ddd;
}

.result-item:last-child {
  border-bottom: none;
}

.label {
  color: #666;
}

.value {
  font-weight: 500;
  color: #333;
}

.error-message {
  margin-top: 20px;
  padding: 12px;
  background-color: #ffebee;
  color: #c62828;
  border-radius: 4px;
  text-align: center;
}
</style>