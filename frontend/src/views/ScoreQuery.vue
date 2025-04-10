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

<style >
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
  margin-bottom: var(--spacing-lg);
}

label {
  display: block;
  margin-bottom: var(--spacing-sm);
  font-weight: 600;
  color: var(--text-primary);
  font-size: 1rem;
}

input {
  width: 100%;
  padding: var(--spacing-md);
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius-md);
  font-size: 1rem;
  transition: all var(--transition-fast);
  background: var(--bg-secondary);
}

input:focus {
  outline: none;
  border-color: var(--primary-color);
  background: var(--bg-primary);
  box-shadow: 0 0 0 3px var(--primary-light);
}

.query-btn {
  width: 100%;
  padding: var(--spacing-md);
  background: linear-gradient(45deg, var(--primary-color), var(--primary-dark));
  color: white;
  border: none;
  border-radius: var(--border-radius-md);
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.query-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--box-shadow);
}

.query-btn:disabled {
  background: var(--border-light);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.score-result {
  margin-top: var(--spacing-xl);
  padding: var(--spacing-lg);
  background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
  border-radius: var(--border-radius-lg);
  border: 2px solid var(--border-lighter);
  animation: fadeIn var(--transition-normal);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.result-content {
  margin-top: var(--spacing-md);
}

.result-item {
  margin-bottom: var(--spacing-md);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-md);
  background: var(--bg-primary);
  border-radius: var(--border-radius-md);
  box-shadow: var(--box-shadow-light);
}

.label {
  font-weight: 600;
  color: var(--text-secondary);
}

.value {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--success-color);
  background: linear-gradient(45deg, var(--success-color), var(--primary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
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