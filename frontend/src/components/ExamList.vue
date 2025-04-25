<template>
  <div class="exam-list">
    <h2>考试列表</h2>
    <div class="exam-grid">
      <div v-for="exam in exams" :key="exam.id" class="exam-card">
        <h3>{{ exam.name }}</h3>
        <p class="question-preview">{{ exam.question.substring(0, 100) }}...</p>
        <div class="card-actions">
          <router-link :to="`/exam/${exam.id}`" class="btn-view">查看详情</router-link>
          <router-link :to="`/answer/${exam.id}`" class="btn-answer">开始答题</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface Exam {
  id: number
  name: string
  question: string
  created_at: string
}

const exams = ref<Exam[]>([])

const fetchExams = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/create-exams/')
    exams.value = response.data
  } catch (error) {
    console.error('获取考试列表失败：', error)
  }
}

onMounted(() => {
  fetchExams()
})
</script>

<style >
.exam-list {
  padding: 20px;
}

.exam-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.exam-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.exam-card h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.question-preview {
  color: #666;
  margin-bottom: 15px;
  line-height: 1.4;
}

.card-actions {
  display: flex;
  gap: 10px;
}

.btn-view,
.btn-answer {
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-view {
  background-color: #e0e0e0;
  color: #333;
}

.btn-answer {
  background-color: #1976d2;
  color: white;
}

.btn-view:hover {
  background-color: #d0d0d0;
}

.btn-answer:hover {
  background-color: #1565c0;
}
</style>