#CreateExam.vue
<template>
  <div class="create-exam">
    <el-card class="exam-form">
      <template #header>
        <div class="card-header">
          <h2>创建考试</h2>
        </div>
      </template>
      
      <el-form :model="examForm" :rules="rules" ref="examFormRef" label-width="100px">
        <el-form-item label="考试名称" prop="name">
          <el-input v-model="examForm.name" placeholder="请输入考试名称"></el-input>
        </el-form-item>
        
        <el-form-item label="考试题目" prop="question">
          <el-input
            v-model="examForm.question"
            type="textarea"
            :rows="4"
            placeholder="请输入考试题目"
          ></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm(examFormRef)">
            创建考试
          </el-button>
          <el-button @click="resetForm(examFormRef)">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useExamStore } from '@/stores/exam'

const examStore = useExamStore()

const examFormRef = ref()
const examForm = reactive({
  name: '',
  question: ''
})

const rules = {
  name: [
    { required: true, message: '请输入考试名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  question: [
    { required: true, message: '请输入考试题目', trigger: 'blur' },
    { min: 5, max: 500, message: '长度在 5 到 500 个字符', trigger: 'blur' }
  ]
}

const submitForm = async (formEl) => {
  if (!formEl) return
  await formEl.validate(async (valid) => {
    if (valid) {
      await examStore.createExam(examForm)  // 调用 store 创建考试
      ElMessage.success('考试创建成功')
      formEl.resetFields()
    }
  })
}

const resetForm = (formEl) => {
  if (!formEl) return
  formEl.resetFields()
}
</script>


<style >
.create-exam {
  padding: 20px;
}

.exam-form {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>