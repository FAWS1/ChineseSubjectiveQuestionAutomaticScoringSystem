<template>
  <div class="view-scores">
    <el-card class="query-form">
      <template #header>
        <div class="card-header">
          <h2>成绩查询</h2>
        </div>
      </template>

      <el-form :model="queryForm" :rules="rules" ref="queryFormRef" label-width="100px">
        <el-form-item label="选择考试" prop="examId">
          <el-select v-model="queryForm.examId" placeholder="请选择考试">
            <el-option
              v-for="exam in examList"
              :key="exam.id"
              :label="exam.name"
              :value="exam.id"
            ></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="学生姓名" prop="studentName">
          <el-input v-model="queryForm.studentName" placeholder="请输入姓名"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="queryScore" :loading="querying">
            查询成绩
          </el-button>
        </el-form-item>
      </el-form>

      <div v-if="scoreResult" class="score-result">
        <el-descriptions title="成绩信息" :column="1" border>
          <el-descriptions-item label="考试名称">
            {{ scoreResult.examName }}
          </el-descriptions-item>
          <el-descriptions-item label="学生姓名">
            {{ scoreResult.studentName }}
          </el-descriptions-item>
          <el-descriptions-item label="得分">
            <span class="score">{{ scoreResult.score }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="答案内容">
            {{ scoreResult.answer }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const queryFormRef = ref()
const querying = ref(false)
const scoreResult = ref(null)

const queryForm = reactive({
  examId: '',
  studentName: ''
})

// 模拟考试列表数据
const examList = ref([
  { id: 1, name: '期中考试' },
  { id: 2, name: '期末考试' }
])

const rules = {
  examId: [{ required: true, message: '请选择考试', trigger: 'change' }],
  studentName: [{ required: true, message: '请输入姓名', trigger: 'blur' }]
}

const queryScore = async () => {
  if (!queryForm.examId || !queryForm.studentName) {
    ElMessage.warning('请选择考试并输入姓名')
    return
  }

  querying.value = true
  try {
    // TODO: 调用后端API查询成绩
    // 模拟查询结果
    await new Promise(resolve => setTimeout(resolve, 1000))
    scoreResult.value = {
      examName: examList.value.find(exam => exam.id === queryForm.examId)?.name,
      studentName: queryForm.studentName,
      score: 85,
      answer: '这是学生的答案内容...'
    }
  } catch (error) {
    ElMessage.error('查询成绩失败')
    scoreResult.value = null
  } finally {
    querying.value = false
  }
}
</script>

<style scoped>
.view-scores {
  padding: 20px;
}

.query-form {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.score-result {
  margin-top: 20px;
}

.score {
  font-size: 24px;
  color: #409EFF;
  font-weight: bold;
}
</style>