<template>
  <div class="exam-detail">
    <div v-if="exam" class="exam-container">
      <h2>{{ exam.name }}</h2>
      <div class="exam-info">
        <h3>考试题目：</h3>
        <div class="question-content">{{ exam.question }}</div>
      </div>
      
      <div class="answer-section">
        <h3>提交答案</h3>
        <div class="form-group">
          <label for="studentName">学生姓名：</label>
          <input
            v-model="studentName"
            type="text"
            id="studentName"
            placeholder="请输入你的姓名"
          >
        </div>
        <div class="form-group">
          <label for="answer">答案：</label>
          <textarea
            v-model="answer"
            id="answer"
            rows="6"
            placeholder="请输入你的答案"
          ></textarea>
        </div>
        <button @click="submitAnswer" :disabled="submitting" class="submit-btn">
          {{ submitting ? '提交中...' : '提交答案' }}
        </button>
      </div>

      <div v-if="submitResult" :class="['result-message', submitResult.success ? 'success' : 'error']">
        {{ submitResult.message }}
      </div>
    </div>
    <div v-else class="loading">加载中...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

interface Exam {
  id: number
  name: string
  question: string
}

const exam = ref<Exam | null>(null)
const studentName = ref('')
const answer = ref('')
const submitting = ref(false)
const submitResult = ref<{ success: boolean; message: string } | null>(null)

const fetchExam = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/create-exams/${route.params.id}/`)
    exam.value = response.data
  } catch (error) {
    console.error('获取考试详情失败：', error)
  }
}

const submitAnswer = async () => {
  if (!studentName.value || !answer.value) {
    submitResult.value = {
      success: false,
      message: '请填写完整的学生姓名和答案'
    }
    return
  }

  submitting.value = true
  try {
    await axios.post('http://localhost:8000/api/student-answers/', {
      exam: exam.value?.id,
      student_name: studentName.value,
      answer: answer.value
    })
    
    submitResult.value = {
      success: true,
      message: '答案提交成功！'
    }
    
    // 提交成功后清空表单
    studentName.value = ''
    answer.value = ''
    
    // 延迟跳转到成绩查询页面
    setTimeout(() => {
      router.push('/query-score')
    }, 2000)
  } catch (error: any) {
    submitResult.value = {
      success: false,
      message: error.response?.data?.error || '提交答案失败，请稍后重试'
    }
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchExam()
})
</script>

<style >
.exam-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.exam-container {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.exam-info {
  margin-bottom: 30px;
}

.question-content {
  white-space: pre-wrap;
  line-height: 1.6;
  color: #333;
  background: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
  margin-top: 10px;
}

.answer-section {
  margin-top: 30px;
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

input,
textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

textarea {
  resize: vertical;
}

.submit-btn {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-btn:hover {
  background-color: #1565c0;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.result-message {
  margin-top: 20px;
  padding: 12px;
  border-radius: 4px;
  text-align: center;
}

.success {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.error {
  background-color: #ffebee;
  color: #c62828;
}

.loading {
  text-align: center;
  color: #666;
  margin-top: 40px;
}
</style>