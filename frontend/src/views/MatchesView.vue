<template>
  <div class="p-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">AstroDate</h1>
      <div class="flex gap-4">
        <router-link to="/home"
                    class="px-4 py-2 font-medium text-indigo-600 bg-white border border-indigo-600 rounded-md hover:bg-indigo-50">
          Zurück zur Suche
        </router-link>
        <button @click="handleLogout"
                class="px-4 py-2 font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700">
          Abmelden
        </button>
      </div>
    </div>

    <!-- Tabs für verschiedene Ansichten -->
    <div class="mb-6 border-b border-gray-200">
      <nav class="flex gap-4">
        <button @click="activeTab = 'likedMe'"
                :class="[
                  'px-4 py-2 font-medium border-b-2 transition-colors',
                  activeTab === 'likedMe' 
                    ? 'border-indigo-600 text-indigo-600' 
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                ]">
          Wer hat mich geliked ({{ usersWhoLikedMe.length }})
        </button>
        <button @click="activeTab = 'iLiked'"
                :class="[
                  'px-4 py-2 font-medium border-b-2 transition-colors',
                  activeTab === 'iLiked' 
                    ? 'border-indigo-600 text-indigo-600' 
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                ]">
          Wen habe ich geliked ({{ myLikes.length }})
        </button>
      </nav>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Lade Daten...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <p class="text-red-600">{{ error }}</p>
      <button @click="loadData" 
              class="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
        Erneut versuchen
      </button>
    </div>

    <!-- Users List -->
    <div v-else>
      <!-- Wer hat mich geliked -->
      <div v-if="activeTab === 'likedMe'">
        <div v-if="usersWhoLikedMe.length === 0" class="text-center py-12">
          <p class="text-gray-600">Noch hat dich niemand geliked.</p>
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="user in usersWhoLikedMe" 
               :key="user.id"
               class="bg-white rounded-lg shadow-md overflow-hidden">
            <div class="w-full h-64 bg-gray-200 flex items-center justify-center">
              <img v-if="user.image_filename" 
                   :src="getImageUrl(user.image_filename)" 
                   :alt="`Profilbild von ${user.email}`"
                   class="w-full h-full object-cover">
              <div v-else class="text-gray-400 text-4xl">
                👤
              </div>
            </div>
            <div class="p-4">
              <h3 class="text-lg font-semibold mb-2">{{ user.email }}</h3>
              <p v-if="user.bio" class="text-sm text-gray-600 mb-2">{{ user.bio }}</p>
              <p v-if="user.zodiac_sign_name" class="text-xs text-gray-500">
                Sternzeichen: <span class="font-semibold">{{ user.zodiac_sign_name }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Wen habe ich geliked -->
      <div v-if="activeTab === 'iLiked'">
        <div v-if="myLikes.length === 0" class="text-center py-12">
          <p class="text-gray-600">Du hast noch niemanden geliked.</p>
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="user in myLikes" 
               :key="user.id"
               class="bg-white rounded-lg shadow-md overflow-hidden">
            <div class="w-full h-64 bg-gray-200 flex items-center justify-center">
              <img v-if="user.image_filename" 
                   :src="getImageUrl(user.image_filename)" 
                   :alt="`Profilbild von ${user.email}`"
                   class="w-full h-full object-cover">
              <div v-else class="text-gray-400 text-4xl">
                👤
              </div>
            </div>
            <div class="p-4">
              <h3 class="text-lg font-semibold mb-2">{{ user.email }}</h3>
              <p v-if="user.bio" class="text-sm text-gray-600 mb-2">{{ user.bio }}</p>
              <p v-if="user.zodiac_sign_name" class="text-xs text-gray-500">
                Sternzeichen: <span class="font-semibold">{{ user.zodiac_sign_name }}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import userService from '../services/userService'
import type { UserRead } from '../services/types'

const router = useRouter()
const authStore = useAuthStore()

const activeTab = ref<'likedMe' | 'iLiked'>('likedMe')
const usersWhoLikedMe = ref<UserRead[]>([])
const myLikes = ref<UserRead[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

/**
 * Lädt alle Like-Daten vom Backend
 */
const loadData = async () => {
  loading.value = true
  error.value = null
  
  try {
    const [whoLikedMe, iLiked] = await Promise.all([
      userService.getUsersWhoLikedMe(),
      userService.getMyLikes()
    ])
    usersWhoLikedMe.value = whoLikedMe
    myLikes.value = iLiked
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Fehler beim Laden der Daten'
    console.error(err)
  } finally {
    loading.value = false
  }
}

/**
 * Gibt die URL für das Profilbild zurück
 */
const getImageUrl = (filename: string): string => {
  return `http://localhost:8000/userImages/${filename}`
}

/**
 * Behandelt die Abmeldung
 */
const handleLogout = () => {
  authStore.removeToken()
  router.push('/')
}

// Lade Daten beim Mounten der Komponente
onMounted(() => {
  loadData()
})
</script>

