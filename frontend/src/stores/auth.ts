import { defineStore } from 'pinia'

interface User {
  username: string
  token: string
  role: 'teacher' | 'student'
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.user,
    getUsername: (state) => state.user?.username || '',
  },
  actions: {
    login(username: string, token: string, role: 'teacher' | 'student') {
      this.user = { username, token, role }
      localStorage.setItem('user', JSON.stringify(this.user))
    },
    logout() {
      this.user = null
      localStorage.removeItem('user')
    },
    loadFromLocalStorage() {
      const data = localStorage.getItem('user')
      if (data) {
        this.user = JSON.parse(data)
      }
    },
  },
})
