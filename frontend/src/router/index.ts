import type { RouteRecordRaw } from 'vue-router'
import { createRouter, createWebHistory } from 'vue-router'
import TeacherLayout from '@/layouts/TeacherLayout.vue'
import StudentLayout from '@/layouts/StudentLayout.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
  },
  {
    path: '/teacher',
    name: 'TeacherRoot',
    component: TeacherLayout,
    // 移除重定向，让教师登录后停留在教师主页
    children: [
      { path: '', name: 'TeacherHome', component: () => import('@/views/teacher/TeacherHome.vue') },
      { path: 'create-exam', name: 'CreateExam', component: () => import('@/views/teacher/CreateExam.vue') },
      { path: 'upload-answers', name: 'UploadAnswers', component: () => import('@/views/teacher/UploadAnswers.vue') },
      { path: 'auto-scoring', name: 'AutoScoring', component: () => import('@/views/teacher/AutoScoring.vue') },
      { path: 'manage-exam', name: 'ManageExam', component: () => import('@/views/teacher/ManageExam.vue') },
      { path: 'view-grades', name: 'ViewGrades', component: () => import('@/views/teacher/ViewGrades.vue') },
      
    ],
  },
  
  {
    path: '/student',
    name: 'StudentRoot',
    component: StudentLayout,
    // 移除重定向，让学生登录后停留在学生主页
    children: [
      { path: '', name: 'StudentHome', component: () => import('@/views/student/StudentHome.vue') },
      { path: 'view-scores', name: 'ViewScores', component: () => import('@/views/student/ViewScores.vue') },
      { path: 'grade-query', name: 'GradeQuery', component: () => import('@/views/student/GradeQuery.vue') },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
