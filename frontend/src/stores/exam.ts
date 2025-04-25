import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/api';  // 使用统一配置的api实例替代直接导入axios

export const useExamStore = defineStore('exam', () => {
  const examList = ref<any[]>([]);

  const fetchExams = async () => {
    try {
      const response = await api.get('/create-exams/');
      examList.value = response.data;
    } catch (error) {
      console.error('获取考试列表失败', error);
    }
  };

  const createExam = async (examData: any) => {
    try {
      console.log('创建考试请求数据：', examData);
      const response = await api.post('/create-exams/', examData);  // 使用正确的相对路径
      examList.value.push(response.data);
    } catch (error) {
      console.error('创建考试失败', error);
      if ((error as any).response) {
        console.error('后端返回错误：', (error as any).response?.data);
      } else {
        console.error('非 API 错误', error);
      }
    }
  };
  
  

  return {
    examList,
    fetchExams,
    createExam
  };
});
