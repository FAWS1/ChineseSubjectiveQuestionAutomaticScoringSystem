<template>
  <div class="upload-answers">
    <el-card class="upload-form">
      <template #header>
        <div class="card-header">
          <h2>上传学生答案</h2>
        </div>
      </template>

      <el-form :model="uploadForm" :rules="rules" ref="uploadFormRef" label-width="100px">
        <el-form-item label="选择考试" prop="examId">
          <el-select v-model="uploadForm.examId" placeholder="请选择考试">
            <el-option
              v-for="exam in examList"
              :key="exam.id"
              :label="exam.name"
              :value="exam.id"
            ></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="答案文件" prop="file">
          <el-upload
            class="upload-demo"
            action="#"
            :auto-upload="false"
            :on-change="handleFileChange"
            :file-list="fileList"
          >
            <template #trigger>
              <el-button type="primary">选择文件</el-button>
            </template>
            <el-button
              class="ml-3"
              type="success"
              @click="submitUpload"
              :disabled="!uploadForm.file"
            >
              上传答案
            </el-button>
            <template #tip>
              <div class="el-upload__tip">
                请上传包含学生答案的Excel文件，文件应包含学生姓名和答案内容
              </div>
            </template>
          </el-upload>
        </el-form-item>
      </el-form>

      <div v-if="previewData.length" class="preview-section">
        <h3>文件预览</h3>
        <el-table :data="previewData" style="width: 100%">
          <el-table-column prop="studentName" label="学生姓名" width="180">
          </el-table-column>
          <el-table-column prop="answer" label="答案内容">
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const uploadFormRef = ref()
const fileList = ref([])
const previewData = ref([])

const uploadForm = reactive({
  examId: '',
  file: null
})

// 模拟考试列表数据
const examList = ref([
  { id: 1, name: '期中考试' },
  { id: 2, name: '期末考试' }
])

const rules = {
  examId: [{ required: true, message: '请选择考试', trigger: 'change' }],
  file: [{ required: true, message: '请上传答案文件', trigger: 'change' }]
}

const handleFileChange = (uploadFile) => {
  uploadForm.file = uploadFile.raw
  // TODO: 实现文件预览功能
  previewData.value = [
    { studentName: '张三', answer: '示例答案内容1' },
    { studentName: '李四', answer: '示例答案内容2' }
  ]
}

const submitUpload = async () => {
  if (!uploadForm.examId || !uploadForm.file) {
    ElMessage.warning('请选择考试并上传文件')
    return
  }
  // TODO: 调用后端API上传文件
  ElMessage.success('答案上传成功')
  fileList.value = []
  previewData.value = []
  uploadForm.file = null
}
</script>

<style scoped>
.upload-answers {
  padding: 20px;
}

.upload-form {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-section {
  margin-top: 20px;
}

.ml-3 {
  margin-left: 12px;
}
</style>