import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/teacher',
      name: 'teacher',
      component: () => import('../views/teacher/TeacherDashboard.vue'),
      children: [
        {
          path: 'create-exam',
          name: 'createExam',
          component: () => import('../views/teacher/CreateExam.vue')
        },
        {
          path: 'upload-answers',
          name: 'uploadAnswers',
          component: () => import('../views/teacher/UploadAnswers.vue')
        },
        {
          path: 'auto-scoring',
          name: 'autoScoring',
          component: () => import('../views/teacher/AutoScoring.vue')
        }
      ]
    },
    {
      path: '/student',
      name: 'student',
      component: () => import('../views/student/StudentDashboard.vue'),
      children: [
        {
          path: 'view-scores',
          name: 'viewScores',
          component: () => import('../views/student/ViewScores.vue')
        }
      ]
    }
  ]
})

export default router