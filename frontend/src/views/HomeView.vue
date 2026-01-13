<template>
  <div class="p-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">AstroDate</h1>
      <div class="flex gap-4">
        <router-link to="/matches"
                    class="px-4 py-2 font-medium text-indigo-600 bg-white border border-indigo-600 rounded-md hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
          Matches
        </router-link>
        <button @click="handleLogout"
                class="px-4 py-2 font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
          Abmelden
        </button>
      </div>
    </div>

    <!-- Kompatibler Benutzer Anzeige -->
    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-600">Lade kompatiblen Benutzer...</p>
    </div>

    <div v-else-if="error" class="text-center py-12">
      <p class="text-red-600">{{ error }}</p>
      <button @click="loadCompatibleUser" 
              class="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
        Erneut versuchen
      </button>
    </div>

    <div v-else-if="currentUser" class="max-w-md mx-auto">
      <!-- Benutzer Karte -->
      <div class="bg-white rounded-lg shadow-lg overflow-hidden">
        <!-- Profilbild -->
        <div class="w-full h-96 bg-gray-200 flex items-center justify-center">
          <img v-if="currentUser.image_filename" 
               :src="getImageUrl(currentUser.image_filename)" 
               :alt="`Profilbild von ${currentUser.email}`"
               class="w-full h-full object-cover">
          <div v-else class="text-gray-400 text-4xl">
            👤
          </div>
        </div>

        <!-- Benutzer Informationen -->
        <div class="p-6">
          <h2 class="text-2xl font-bold mb-2">{{ currentUser.email }}</h2>
          <p v-if="currentUser.bio" class="text-gray-600 mb-4">{{ currentUser.bio }}</p>
          <p v-if="currentUser.zodiac_sign_name" class="text-sm text-gray-500">
            Sternzeichen: <span class="font-semibold">{{ currentUser.zodiac_sign_name }}</span>
          </p>
        </div>

        <!-- Like/Dislike Buttons -->
        <div class="p-6 flex gap-4">
          <button @click="handleDislike"
                  class="flex-1 px-6 py-3 font-bold text-white bg-red-600 rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 flex items-center justify-center gap-2">
            <span class="text-2xl">✕</span>
            <span>Dislike</span>
          </button>
          <button @click="handleLike"
                  class="flex-1 px-6 py-3 font-semibold text-white bg-green-600 rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500">
            ❤️ Like
          </button>
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

const currentUser = ref<UserRead | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

/**
 * Lädt einen kompatiblen Benutzer vom Backend
 */
const loadCompatibleUser = async () => {
  loading.value = true
  error.value = null
  
  try {
    const user = await userService.discoverCompatibleUser()
    currentUser.value = user
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Fehler beim Laden des kompatiblen Benutzers'
    console.error(err)
  } finally {
    loading.value = false
  }
}

/**
 * Behandelt den Like-Button Klick
 * Speichert den Like in der Datenbank und lädt einen neuen kompatiblen Benutzer
 */
const handleLike = async () => {
  if (currentUser.value) {
    try {
      const response = await userService.swipeUser(currentUser.value.id, true);
      console.log(response.message); // Optional: Log success or mutual match message
      // Lade einen neuen kompatiblen Benutzer nach dem Like
      await loadCompatibleUser();
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Fehler beim Liken des Benutzers';
      console.error(err);
    }
  }
};

/**
 * Behandelt den Dislike-Button Klick
 * Speichert den Dislike und lädt einen neuen kompatiblen Benutzer
 */
const handleDislike = async () => {
  if (currentUser.value) {
    try {
      await userService.swipeUser(currentUser.value.id, false);
      // Lade einen neuen kompatiblen Benutzer nach dem Dislike
      await loadCompatibleUser();
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Fehler beim Disliken des Benutzers';
      console.error(err);
    }
  }
};

/**
 * Gibt die URL für das Profilbild zurück
 */
const getImageUrl = (filename: string): string => {
  return `http://localhost:8000/userImages/${filename}`
}

/**
 * Formatiert das Geburtsdatum für die Anzeige
 */
const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleDateString('de-DE')
}

/**
 * Behandelt die Abmeldung
 */
const handleLogout = () => {
  authStore.removeToken()
  router.push('/')
}

// Lade einen kompatiblen Benutzer beim Mounten der Komponente
onMounted(() => {
  loadCompatibleUser()
})
</script>
