<template>
  <div class="answer-upload">
    <el-card class="upload-card" :body-style="{ padding: '20px' }">
      <template #header>
        <div class="card-header">
          <h2>上传学生答案</h2>
        </div>
      </template>

      <el-form :model="form" label-width="120px" class="upload-form">
        <el-form-item label="选择考试">
          <el-select v-model="form.examId" placeholder="请选择考试" class="w-full">
            <el-option
              v-for="exam in examList"
              :key="exam.exam_name"
              :label="exam.exam_name"
              :value="exam.exam_name"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="学生答案文件">
          <el-upload
            ref="uploadRef"
            class="uploader"
            drag
            :auto-upload="false"
            :multiple="false"
            :limit="1"
            :file-list="fileList"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
          >
            <el-icon class="upload-icon"><upload-filled /></el-icon>
            <div class="upload-text">
              <em>点击上传文件或将文件拖拽到此处</em>
              <p class="upload-tip">支持 .xlsx, .xls 格式的文件</p>
              <p class="upload-tip important-tip">Excel文件必须包含以下列名：学生姓名、学号、答案</p>
            </div>
          </el-upload>

          <div class="mt-4">
            <el-alert
              type="warning"
              title="重要提示"
              description="选择文件后，请点击下方【上传文件】按钮，否则文件不会被上传到服务器！"
              show-icon
              :closable="false"
              class="mb-4"
            />
            <el-button
              type="primary"
              size="large"
              @click="submitUpload"
              :loading="uploading"
              :disabled="uploading"
              class="upload-btn"
            >
              <el-icon><upload-filled /></el-icon> 上传文件
            </el-button>
          </div>
        </el-form-item>

        <div v-if="uploadStatus.show" class="upload-status">
          <el-alert
            :title="uploadStatus.message"
            :type="uploadStatus.type"
            :closable="false"
            show-icon
            :effect="uploadStatus.type === 'error' ? 'dark' : 'light'"
            class="upload-status-alert"
          />
          <div v-if="uploadStatus.details" class="error-details mt-2">
            <pre>{{ uploadStatus.details }}</pre>
          </div>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import api from '@/api'

const uploadRef = ref(null)
const fileList = ref([])
const uploading = ref(false)

const form = ref({
  examId: '',
})

const examList = ref([])
const examListCache = ref(null)
const uploadStatus = ref({
  show: false,
  message: '',
  type: 'info',
  details: '',
})

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

// 加载考试列表
onMounted(async () => {
  if (examListCache.value) {
    examList.value = examListCache.value
    return
  }
  try {
    const response = await api.get('/create-exams/')
    examList.value = response.data || []
    examListCache.value = examList.value
  } catch (error) {
    console.error('获取考试列表失败', error)
    ElMessage.error('获取考试列表失败')
  }
})

// 文件变更处理
const handleFileChange = (file, fileListNew) => {
  if (file && file.raw) {
    const isExcel = file.raw.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      || file.raw.type === 'application/vnd.ms-excel'
    if (!isExcel) {
      ElMessage.error('只能上传Excel文件！')
      uploadRef.value.clearFiles()
      return
    }
    if (!form.value.examId) {
      ElMessage.error('请先选择考试！')
      uploadRef.value.clearFiles()
      return
    }
    fileList.value = fileListNew
  }
}

// 移除文件
const handleFileRemove = () => {
  fileList.value = []
}

// 提交上传
const submitUpload = async () => {
  if (!form.value.examId) {
    ElMessage.error('请先选择考试！')
    return
  }
  if (fileList.value.length === 0) {
    ElMessage.error('请选择要上传的文件！')
    return
  }

  try {
    uploading.value = true
    const formData = new FormData()
    formData.append('file', fileList.value[0].raw)
    formData.append('examId', form.value.examId)
    // 添加列名映射信息，告知后端如何处理Excel文件中的列名
    formData.append('column_mapping', JSON.stringify({
      'student_id': '学号',
      'student_name': '学生姓名',
      'student_answer': '答案'
    }))

    await api.post('/upload-answers/upload_batch/', formData, {
      headers: {
        ...authHeaders.value,
        'Content-Type': 'multipart/form-data'
      }
    })

    uploadStatus.value = {
      show: true,
      message: '答案上传成功！',
      type: 'success'
    }
    fileList.value = []
  } catch (error) {
    console.error('上传文件失败', error)
    let message = '答案上传失败，请重试'
    let details = ''
    
    if (error.response) {
      // 详细展示服务器返回的错误信息
      const errorData = error.response.data
      if (errorData) {
        if (errorData.detail) {
          message = `服务器错误: ${errorData.detail}`
        } else if (errorData.error) {
          message = `服务器错误: ${errorData.error}`
        } else if (typeof errorData === 'string') {
          message = `服务器错误: ${errorData}`
        } else {
          message = `服务器返回错误 (状态码: ${error.response.status})`
          // 保存完整错误信息用于显示
          try {
            details = JSON.stringify(errorData, null, 2)
          } catch (e) {
            details = '无法解析错误详情'
          }
          console.error('完整错误响应:', details)
        }
      } else {
        message = `服务器返回错误 (状态码: ${error.response.status})`
      }
    } else if (error.request) {
      message = '服务器无响应，请检查网络'
      details = '请检查网络连接或服务器是否正常运行'
    } else {
      message = `请求错误: ${error.message}`
      details = error.stack || ''
    }
    
    uploadStatus.value = {
      show: true,
      message,
      type: 'error',
      details
    }
  } finally {
    setTimeout(() => {
      uploading.value = false
    }, 2000)  // 上传结束后缓冲2秒再解锁按钮
    
    // 根据上传状态类型设置不同的显示时间
    const displayTime = uploadStatus.value.type === 'error' ? 10000 : 4000
    setTimeout(() => {
      uploadStatus.value.show = false
    }, displayTime) // 错误信息显示更长时间，成功信息保持原来的时间
  }
}
</script>

<style scoped>
.answer-upload {
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: calc(100vh - 60px);
}
.upload-card {
  max-width: 800px;
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
.upload-form {
  margin-top: 20px;
}
.uploader {
  border: 2px dashed #409EFF;
  border-radius: 8px;
  background: #f8fafc;
  transition: all 0.3s;
}
.uploader:hover {
  border-color: #79bbff;
  background: #f1f6ff;
}
.upload-icon {
  font-size: 48px;
  color: #409EFF;
  margin-bottom: 10px;
}
.upload-text {
  color: #606266;
  font-size: 14px;
}
.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}
.important-tip {
  color: #E6A23C;
  font-weight: bold;
}
.upload-status {
  margin-top: 20px;
}
.upload-status-alert {
  font-weight: 500;
}
.error-details {
  background-color: #fef0f0;
  border: 1px solid #fde2e2;
  border-radius: 4px;
  padding: 8px;
  max-height: 200px;
  overflow-y: auto;
  font-family: monospace;
  font-size: 12px;
  white-space: pre-wrap;
  word-break: break-all;
}
.mt-4 {
  margin-top: 16px;
}
.mb-4 {
  margin-bottom: 16px;
}
.upload-btn {
  margin-top: 15px;
  width: 100%;
  height: 50px;
  font-size: 16px;
  font-weight: bold;
  background-color: #409EFF;
  border-color: #409EFF;
}
.w-full {
  width: 100%;
}
</style>
