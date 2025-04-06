import { createRouter, createWebHistory } from 'vue-router'
import ExamList from '../components/ExamList.vue'
import ExamDetail from '../views/ExamDetail.vue'
import ScoreQuery from '../views/ScoreQuery.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: ExamList
    },
    {
      path: '/exam/:id',
      name: 'exam-detail',
      component: ExamDetail
    },
    {
      path: '/query-score',
      name: 'score-query',
      component: ScoreQuery
    },
  ],
})

export default router
