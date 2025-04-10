<template>
  <div class="grade-query">
    <el-card class="grade-card">
      <template #header>
        <div class="card-header">
          <h2>成绩查询</h2>
          <el-input
            v-model="searchQuery"
            placeholder="搜索考试"
            class="search-input"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </template>

      <el-tabs v-model="activeTab" class="grade-tabs">
        <el-tab-pane label="考试列表" name="examList">
          <div class="exam-list">
            <el-card
              v-for="exam in filteredExams"
              :key="exam.id"
              class="exam-card"
              shadow="hover"
              @click="selectExam(exam)"
            >
              <div class="exam-info">
                <h3>{{ exam.name }}</h3>
                <div class="exam-meta">
                  <span><el-icon><Calendar /></el-icon>{{ exam.date }}</span>
                  <span><el-icon><Document /></el-icon>{{ exam.subject }}</span>
                </div>
                <div class="exam-score" :class="getScoreClass(exam.score)">
                  {{ exam.score }}分
                </div>
              </div>
            </el-card>
          </div>
        </el-tab-pane>

        <el-tab-pane label="成绩统计" name="statistics">
          <div class="statistics-container">
            <el-row :gutter="20">
              <el-col :span="8">
                <el-card class="stat-card">
                  <template #header>
                    <div class="stat-header">
                      <el-icon><Trophy /></el-icon>
                      <span>最高分</span>
                    </div>
                  </template>
                  <div class="stat-value">{{ statistics.highest }}分</div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card class="stat-card">
                  <template #header>
                    <div class="stat-header">
                      <el-icon><Histogram /></el-icon>
                      <span>平均分</span>
                    </div>
                  </template>
                  <div class="stat-value">{{ statistics.average }}分</div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card class="stat-card">
                  <template #header>
                    <div class="stat-header">
                      <el-icon><DataLine /></el-icon>
                      <span>考试数量</span>
                    </div>
                  </template>
                  <div class="stat-value">{{ statistics.total }}次</div>
                </el-card>
              </el-col>
            </el-row>

            <el-card class="chart-card">
              <div class="chart-container">
                <div class="score-chart" ref="chartRef"></div>
              </div>
            </el-card>

            <el-row :gutter="20" class="stat-row">
              <el-col :xs="24" :sm="12" :md="8">
                <el-card class="stat-card">
                  <h3>平均分</h3>
                  <div class="stat-value">{{ averageScore }}</div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card class="stat-card">
                  <template #header>
                    <div class="stat-header">
                      <el-icon><DataLine /></el-icon>
                      <span>考试数量</span>
                    </div>
                  </template>
                  <div class="stat-value">{{ statistics.total }}次</div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog
      v-model="examDetailVisible"
      title="考试详情"
      width="50%"
      class="exam-detail-dialog"
    >
      <template v-if="selectedExam">
        <div class="detail-content">
          <h3>{{ selectedExam.name }}</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="考试日期">{{ selectedExam.date }}</el-descriptions-item>
            <el-descriptions-item label="科目">{{ selectedExam.subject }}</el-descriptions-item>
            <el-descriptions-item label="得分">{{ selectedExam.score }}</el-descriptions-item>
            <el-descriptions-item label="满分">100</el-descriptions-item>
          </el-descriptions>
          
          <div class="answer-section">
            <h4>我的答案</h4>
            <el-input type="textarea" v-model="selectedExam.answer" readonly rows="4" />
            
            <h4>标准答案</h4>
            <el-input type="textarea" v-model="selectedExam.standardAnswer" readonly rows="4" />
            
            <h4>评分反馈</h4>
            <el-input type="textarea" v-model="selectedExam.feedback" readonly rows="3" />
          </div>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Search, Calendar, Document, Trophy, Histogram, DataLine } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

// 模拟数据
const examList = ref([
  {
    id: 1,
    name: '期中考试',
    date: '2023-10-15',
    subject: '语文',
    score: 85,
    answer: '这是学生的答案...',
    standardAnswer: '这是标准答案...',
    feedback: '答案结构完整，论述充分，但有些细节可以进一步完善。'
  },
  // 添加更多考试数据...
])

const searchQuery = ref('')
const activeTab = ref('examList')
const examDetailVisible = ref(false)
const selectedExam = ref(null)
const scoreChart = ref(null)

const statistics = ref({
  highest: 95,
  average: 82,
  total: 10
})

const filteredExams = computed(() => {
  return examList.value.filter(exam =>
    exam.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    exam.subject.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const getScoreClass = (score) => {
  if (score >= 90) return 'score-excellent'
  if (score >= 80) return 'score-good'
  if (score >= 60) return 'score-pass'
  return 'score-fail'
}

const selectExam = (exam) => {
  selectedExam.value = exam
  examDetailVisible.value = true
}

onMounted(() => {
  const chart = echarts.init(scoreChart.value)
  const option = {
    title: {
      text: '成绩趋势',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: examList.value.map(exam => exam.name)
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100
    },
    series: [{
      data: examList.value.map(exam => exam.score),
      type: 'line',
      smooth: true,
      markLine: {
        data: [{ type: 'average', name: '平均分' }]
      }
    }]
  }
  chart.setOption(option)

  window.addEventListener('resize', () => {
    chart.resize()
  })
})
</script>

<style >
.grade-query {
  padding: 20px;
}

.grade-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-input {
  width: 250px;
}

.exam-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.exam-card {
  cursor: pointer;
  transition: all 0.3s;
}

.exam-card:hover {
  transform: translateY(-5px);
}

.exam-info h3 {
  margin: 0 0 10px 0;
  color: #303133;
}

.exam-meta {
  display: flex;
  gap: 15px;
  color: #909399;
  font-size: 14px;
}

.exam-meta span {
  display: flex;
  align-items: center;
  gap: 5px;
}

.exam-score {
  margin-top: 15px;
  font-size: 24px;
  font-weight: bold;
  text-align: right;
}

.score-excellent { color: #67C23A; }
.score-good { color: #409EFF; }
.score-pass { color: #E6A23C; }
.score-fail { color: #F56C6C; }

.statistics-container {
  padding: 20px 0;
}

.stat-card {
  text-align: center;
}

.stat-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #409EFF;
}

.chart-container {
  margin-top: 30px;
}

.score-chart {
  width: 100%;
  height: 400px;
}

.detail-content {
  padding: 20px;
}

.answer-section {
  margin-top: 20px;
}

.answer-section h4 {
  margin: 15px 0 10px 0;
  color: #606266;
}

.stat-card {
  background: linear-gradient(145deg, #f0fff4, #e6fffa);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
}

.chart-card {
  margin-top: 30px;
  border-radius: 12px;
}

@media (max-width: 768px) {
  .stat-row {
    margin-top: 15px;
  }
  .chart-card {
    margin-top: 20px;
  }
}
</style>