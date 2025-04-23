import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';

export const useExamStore = defineStore('exam', () => {
  const examList = ref<any[]>([]);

  const fetchExams = async () => {
    try {
      const response = await axios.get('/api/exams/');
      examList.value = response.data;
    } catch (error) {
      console.error('获取考试列表失败', error);
    }
  };

  const createExam = async (examData: any) => {
    try {
      const response = await axios.post('/api/exams/', examData);
      examList.value.push(response.data);  // 将新创建的考试添加到考试列表
    } catch (error) {
      console.error('创建考试失败', error);
    }
  };

  return {
    examList,
    fetchExams,
    createExam
  };
});
