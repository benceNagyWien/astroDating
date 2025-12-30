import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null) // We can store user info here later

  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  function removeToken() {
    token.value = null
    localStorage.removeItem('token')
  }
  
  const isAuthenticated = ref(!!token.value)

  function setAuthenticated(authStatus: boolean) {
    isAuthenticated.value = authStatus
  }


  return { token, user, isAuthenticated, setToken, removeToken, setAuthenticated }
})
