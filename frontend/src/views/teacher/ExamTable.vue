<template>
  <div class="exam-table-view">
    <el-card class="exam-table-container">
      <template #header>
        <div class="card-header">
          <h2>考试表单</h2>
        </div>
      </template>

      <div class="content-wrapper">
        <!-- 数据表格 -->
        <el-table
          v-loading="loading"
          :data="examList"
          style="width: 100%"
          border
          stripe
          :default-sort="{prop: 'exam_name', order: 'ascending'}">
          <el-table-column prop="exam_name" label="考试名称" sortable width="180" />
          <el-table-column prop="average_score" label="平均分" sortable>
            <template #default="scope">
              {{ scope.row.average_score !== null ? scope.row.average_score : '(暂无数据)' }}
            </template>
          </el-table-column>
          <el-table-column prop="min_score" label="最低分" sortable>
            <template #default="scope">
              {{ scope.row.min_score !== null ? scope.row.min_score : '(暂无数据)' }}
            </template>
          </el-table-column>
          <el-table-column prop="max_score" label="最高分" sortable>
            <template #default="scope">
              {{ scope.row.max_score !== null ? scope.row.max_score : '(暂无数据)' }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180">
            <template #default="scope">
              <el-button
                type="primary"
                size="small"
                @click="viewExamDetails(scope.row)">
                查看详情
              </el-button>
              <el-button
                type="success"
                size="small"
                @click="refreshExamStats(scope.row)">
                刷新统计
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 空数据显示 -->
        <el-empty v-if="examList.length === 0 && !loading" description="暂无考试数据" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/api'

const examList = ref([])
const loading = ref(true)

// 认证头
const authHeaders = computed(() => {
  let token = ''
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      const user = JSON.parse(userStr)
      token = user.token || ''
    } catch (e) {
      console.error('解析用户信息失败', e)
    }
  }
  return {
    'X-Requested-With': 'XMLHttpRequest',
    'Authorization': token ? `Bearer ${token}` : ''
  }
})

// 获取考试统计数据
const fetchExamStats = async () => {
  loading.value = true
  try {
    const response = await api.get('/create-exams/', {
      headers: authHeaders.value
    })
    examList.value = response.data || []
  } catch (error) {
    console.error('获取考试统计数据失败:', error)
    ElMessage.error('获取考试统计数据失败')
  } finally {
    loading.value = false
  }
}

// 查看考试详情
const viewExamDetails = (exam) => {
  ElMessage.info(`查看${exam.exam_name}的详细信息`)
  // 可以添加导航到详情页面的逻辑
}

// 刷新单个考试的统计数据
const refreshExamStats = async (exam) => {
  try {
    ElMessage.info(`正在刷新${exam.exam_name}的统计数据...`)
    // 这里可以添加调用后端更新统计数据的API
    await fetchExamStats() // 刷新后重新获取数据
    ElMessage.success(`已更新${exam.exam_name}的统计数据`)
  } catch (error) {
    console.error('刷新考试统计数据失败:', error)
    ElMessage.error('刷新考试统计数据失败')
  }
}

onMounted(() => {
  fetchExamStats()
})
</script>

<style>
.exam-table-view {
  padding: 20px;
  min-height: calc(100vh - 60px);
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  display: flex;
  justify-content: center;
  align-items: flex-start;
  width: 100%;
  box-sizing: border-box;
}

.exam-table-container {
  width: 100%;
  max-width: 1280px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.95);
  margin: 0 auto;
}

.content-wrapper {
  padding: 0 15px 20px;
}

.card-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #2c3e50;
}

@media (max-width: 768px) {
  .exam-table-container {
    width: 95%;
  }
  
  .content-wrapper {
    padding: 0 10px 10px;
  }
  
  .el-table {
    font-size: 14px;
  }
}
</style> 