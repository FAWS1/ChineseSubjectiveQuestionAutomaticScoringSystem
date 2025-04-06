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
          <el-select v-model="scoringForm.examId" placeholder="请选择考试" @change="handleExamChange">
            <el-option
              v-for="exam in examList"
              :key="exam.id"
              :label="exam.name"
              :value="exam.id"
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
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const scoringFormRef = ref()
const scoring = ref(false)
const scoringResults = ref([])

const scoringForm = reactive({
  examId: '',
  standardAnswer: ''
})

// 模拟考试列表数据
const examList = ref([
  { id: 1, name: '期中考试' },
  { id: 2, name: '期末考试' }
])

const rules = {
  examId: [{ required: true, message: '请选择考试', trigger: 'change' }],
  standardAnswer: [{ required: true, message: '请输入标准答案', trigger: 'blur' }]
}

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
    // TODO: 调用后端API进行自动评分
    // 模拟评分结果
    await new Promise(resolve => setTimeout(resolve, 1500))
    scoringResults.value = [
      {
        studentName: '张三',
        answer: '这是张三的答案内容...',
        score: 85,
        similarity: 0.85
      },
      {
        studentName: '李四',
        answer: '这是李四的答案内容...',
        score: 75,
        similarity: 0.75
      }
    ]
    ElMessage.success('评分完成')
  } catch (error) {
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
    // TODO: 调用后端API保存评分结果
    ElMessage.success('评分结果已保存')
  } catch (error) {
    ElMessage.error('保存评分结果失败')
  }
}
</script>

<style scoped>
.auto-scoring {
  padding: 20px;
}

.scoring-form {
  max-width: 1000px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.results-section {
  margin-top: 20px;
}

.actions {
  margin-top: 20px;
  text-align: right;
}
</style>