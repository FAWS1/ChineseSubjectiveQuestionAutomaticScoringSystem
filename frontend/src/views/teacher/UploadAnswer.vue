<template>
  <div class="upload-answer">
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
              :key="exam.id"
              :label="exam.name"
              :value="exam.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="学生答案文件">
          <el-upload
            class="upload-area"
            drag
            action="/api/upload-answers"
            :headers="{
              'X-Requested-With': 'XMLHttpRequest',
            }"
            :data="{ examId: form.examId }"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
            :before-upload="beforeUpload"
          >
            <el-icon class="upload-icon"><upload-filled /></el-icon>
            <div class="upload-text">
              <em>点击上传文件或将文件拖拽到此处</em>
              <p class="upload-tip">支持 .xlsx, .xls 格式的文件</p>
            </div>
          </el-upload>
        </el-form-item>

        <div class="upload-status" v-if="uploadStatus.show">
          <el-alert
            :title="uploadStatus.message"
            :type="uploadStatus.type"
            :closable="false"
            show-icon
          />
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const form = ref({
  examId: '',
})

const examList = ref([])
const uploadStatus = ref({
  show: false,
  message: '',
  type: 'info'
})

onMounted(async () => {
  try {
    const response = await fetch('/api/exams')
    const data = await response.json()
    examList.value = data
  } catch (error) {
    ElMessage.error('获取考试列表失败')
  }
})

const beforeUpload = (file) => {
  const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
                 file.type === 'application/vnd.ms-excel'
  if (!isExcel) {
    ElMessage.error('只能上传Excel文件！')
    return false
  }
  if (!form.value.examId) {
    ElMessage.error('请先选择考试！')
    return false
  }
  return true
}

const handleUploadSuccess = (response) => {
  uploadStatus.value = {
    show: true,
    message: '答案上传成功！',
    type: 'success'
  }
  setTimeout(() => {
    uploadStatus.value.show = false
  }, 3000)
}

const handleUploadError = () => {
  uploadStatus.value = {
    show: true,
    message: '答案上传失败，请重试',
    type: 'error'
  }
}
</script>

<style >
.upload-answer {
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

.upload-area {
  border: 2px dashed #409EFF;
  border-radius: 8px;
  background: #f8fafc;
  transition: all 0.3s;
}

.upload-area:hover {
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

.upload-status {
  margin-top: 20px;
}

.w-full {
  width: 100%;
}
</style>