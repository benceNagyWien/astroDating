<template>
  <div class="p-8">
    <h1 class="text-3xl font-bold">Willkommen zu Hause!</h1>
    <p class="mt-4">Sie sind erfolgreich angemeldet.</p>
    <button @click="handleLogout"
            class="px-4 py-2 mt-6 font-medium text-white bg-red-600 border border-transparent rounded-md group hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
      Abmelden
    </button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.removeToken()
  router.push('/')
}
</script>
