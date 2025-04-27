<template>
  <div class="auto-scoring">
    <el-card class="scoring-form">
      <template #header>
        <div class="card-header">
          <h2>自动评分</h2>
        </div>
      </template>

      <el-form :model="scoringForm" :rules="rules" ref="scoringFormRef" label-width="100px">
        <el-form-item label="选择考试" prop="examId">
          <el-select v-model="scoringForm.examId" placeholder="请选择考试" @change="handleExamChange" class="w-full">
            <el-option
              v-for="exam in examList"
              :key="exam.exam_name"
              :label="exam.exam_name"
              :value="exam.exam_name"
            ></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="标准答案" prop="standardAnswer">
          <el-input
            v-model="scoringForm.standardAnswer"
            type="textarea"
            :rows="4"
            placeholder="请输入标准答案"
          ></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="startScoring" :loading="scoring">
            开始评分
          </el-button>
        </el-form-item>
      </el-form>

      <div v-if="scoringResults.length" class="results-section">
        <h3>评分结果</h3>
        <el-table :data="scoringResults" style="width: 100%">
          <el-table-column prop="studentName" label="学生姓名" width="120">
          </el-table-column>
          <el-table-column prop="answer" label="学生答案" show-overflow-tooltip>
          </el-table-column>
          <el-table-column prop="score" label="得分" width="120">
            <template #default="{ row }">
              <el-input-number
                v-model="row.score"
                :min="0"
                :max="100"
                size="small"
                @change="handleScoreChange(row)"
              ></el-input-number>
            </template>
          </el-table-column>
          <el-table-column prop="similarity" label="相似度" width="120">
            <template #default="{ row }">
              {{ (row.similarity * 100).toFixed(2) }}%
            </template>
          </el-table-column>
        </el-table>

        <div class="actions">
          <el-button type="success" @click="saveScores" :disabled="!scoringResults.length">
            保存评分结果
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/api'

const scoringFormRef = ref()
const scoring = ref(false)
const scoringResults = ref([])

const scoringForm = reactive({
  examId: '',
  standardAnswer: ''
})

const examList = ref([])

const rules = {
  examId: [{ required: true, message: '请选择考试', trigger: 'change' }],
  standardAnswer: [{ required: true, message: '请输入标准答案', trigger: 'blur' }]
}

// 获取认证令牌，并创建请求头对象
const authHeaders = computed(() => {
  let token = ''
  try {
    const userStr = localStorage.getItem('user')
    if (userStr) {
      const user = JSON.parse(userStr)
      token = user.token || ''
    }
  } catch (e) {
    console.error('获取用户令牌失败', e)
  }
  return {
    'X-Requested-With': 'XMLHttpRequest',
    'Authorization': token ? `Bearer ${token}` : ''
  }
})

onMounted(async () => {
  try {
    const response = await api.get('/create-exams/')
    examList.value = response.data || []
  } catch (error) {
    console.error('获取考试列表失败', error)
    ElMessage.error('获取考试列表失败')
  }
})

const handleExamChange = (examId) => {
  // TODO: 获取考试信息和已上传的答案
  scoringResults.value = []
}

const startScoring = async () => {
  if (!scoringForm.examId || !scoringForm.standardAnswer) {
    ElMessage.warning('请选择考试并输入标准答案')
    return
  }

  scoring.value = true
  try {
    // 调用后端API进行自动评分
    const response = await api.post('/auto-scoring/', {
      examId: scoringForm.examId,
      standardAnswer: scoringForm.standardAnswer
    }, {
      headers: authHeaders.value
    })
    
    scoringResults.value = response.data || []
    ElMessage.success('评分完成')
  } catch (error) {
    console.error('评分过程出现错误', error)
    ElMessage.error('评分过程出现错误')
  } finally {
    scoring.value = false
  }
}

const handleScoreChange = (row) => {
  // TODO: 更新单个学生的分数
  console.log('分数已修改:', row)
}

const saveScores = async () => {
  try {
    // 调用后端API保存评分结果
    await api.post('/save-scores/', {
      examId: scoringForm.examId,
      scores: scoringResults.value
    }, {
      headers: authHeaders.value
    })
    
    ElMessage.success('评分结果已保存')
  } catch (error) {
    console.error('保存评分结果失败', error)
    ElMessage.error('保存评分结果失败')
  }
}
</script>


<style>
.auto-scoring {
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: calc(100vh - 60px);
}

.scoring-form {
  max-width: 1000px;
  margin: 0 auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.9);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #2c3e50;
}

.results-section {
  margin-top: 20px;
}

.actions {
  margin-top: 20px;
  text-align: right;
}

.w-full {
  width: 100%;
}
</style>