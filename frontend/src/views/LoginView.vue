<template>
  <!-- Hauptcontainer mit Gradient-Hintergrund -->
  <div class="flex items-center justify-center min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
    <div class="w-full max-w-md px-6 py-8">
      <!-- Logo und Titel-Bereich -->
      <div class="text-center mb-8">
        <div class="inline-block p-3 mb-4 bg-white rounded-2xl shadow-lg">
          <img class="w-16 h-16 rounded-full" src="../assets/logo.jpeg" alt="AstroDate Logo">
        </div>
        <h1 class="text-5xl font-extrabold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-2">
          AstroDate
        </h1>
        <p class="text-gray-600 text-base font-medium">Finde deine astrologische Liebe</p>
      </div>

      <!-- Anmelde-/Registrierungsformular -->
      <div class="bg-white/80 backdrop-blur-sm rounded-3xl shadow-2xl p-8 border border-white/20 transition-all duration-300">
        <form @submit.prevent="isRegisterMode ? handleRegister() : handleLogin()" class="space-y-6">
          <!-- E-Mail Eingabefeld -->
          <div class="space-y-2">
            <label for="email-address" class="block text-sm font-semibold text-gray-700">
              E-Mail-Adresse
            </label>
            <div class="relative">
              <input 
                id="email-address" 
                name="email" 
                type="email" 
                autocomplete="email" 
                required
                class="w-full px-4 py-3.5 text-gray-900 placeholder-gray-400 bg-gray-50 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 hover:border-gray-300"
                placeholder="max.mustermann@email.de" 
                v-model="email">
            </div>
          </div>

          <!-- Passwort Eingabefeld -->
          <div class="space-y-2">
            <label for="password" class="block text-sm font-semibold text-gray-700">
              Passwort
            </label>
            <div class="relative">
              <input 
                id="password" 
                name="password" 
                type="password" 
                autocomplete="current-password" 
                required
                class="w-full px-4 py-3.5 text-gray-900 placeholder-gray-400 bg-gray-50 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 hover:border-gray-300"
                placeholder="Dein Passwort" 
                v-model="password">
            </div>
          </div>

          <!-- Geburtsdatum Eingabefeld (nur bei Registrierung) -->
          <div v-if="isRegisterMode" class="space-y-2 transition-all duration-300 ease-in-out animate-fadeIn">
            <label for="birth-date" class="block text-sm font-semibold text-gray-700">
              Geburtsdatum
            </label>
            <div class="relative">
              <input 
                id="birth-date" 
                name="birth-date" 
                type="date" 
                required
                class="w-full px-4 py-3.5 text-gray-900 bg-gray-50 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 hover:border-gray-300"
                v-model="birthDate">
            </div>
          </div>

          <!-- Fehler-/Erfolgsmeldungen -->
          <div class="min-h-[28px] flex items-center justify-center">
            <p v-if="errorMsg" class="text-sm text-red-600 font-medium text-center px-4 py-2 bg-red-50 rounded-lg animate-pulse">
              {{ errorMsg }}
            </p>
            <p v-if="successMsg" class="text-sm text-green-600 font-medium text-center px-4 py-2 bg-green-50 rounded-lg">
              {{ successMsg }}
            </p>
          </div>

          <!-- Hauptaktion-Button (Anmelden/Registrieren) -->
          <button 
            type="submit"
            @click.prevent="isRegisterMode ? handleRegister() : handleLogin()"
            class="w-full py-4 px-6 bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 text-white font-bold text-base rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 focus:outline-none focus:ring-4 focus:ring-indigo-300">
            {{ isRegisterMode ? 'Konto erstellen' : 'Anmelden' }}
          </button>

          <!-- Wechsel-Button (Registrierung/Anmeldung) -->
          <div class="pt-2">
            <button 
              v-if="!isRegisterMode"
              @click.prevent="isRegisterMode = true"
              type="button"
              class="w-full py-3.5 px-4 text-indigo-600 font-semibold rounded-xl border-2 border-indigo-200 bg-indigo-50/50 hover:bg-indigo-100 hover:border-indigo-300 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500">
              Noch kein Konto? Jetzt registrieren
            </button>
            <button 
              v-else
              @click.prevent="isRegisterMode = false"
              type="button"
              class="w-full py-3.5 px-4 text-gray-600 font-semibold rounded-xl border-2 border-gray-200 bg-gray-50/50 hover:bg-gray-100 hover:border-gray-300 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-gray-400">
              Bereits ein Konto? Zur Anmeldung
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import authService from '../services/authService'

// Reaktive Variablen für Formularfelder
const email = ref('')
const password = ref('')
const birthDate = ref('')
const isRegisterMode = ref(false)
const errorMsg = ref('')
const successMsg = ref('')
const router = useRouter()
const authStore = useAuthStore()

/**
 * Behandelt den Anmeldevorgang
 * Validiert die Eingaben und sendet die Anmeldedaten an den Backend-Service
 */
const handleLogin = async () => {
  errorMsg.value = ''
  successMsg.value = ''
  
  // Validierung der Eingabefelder
  if (!email.value || !password.value) {
    errorMsg.value = 'Bitte geben Sie E-Mail und Passwort ein.'
    return
  }

  try {
    // Anmeldung über den Auth-Service
    const data = await authService.login(email.value, password.value)
    authStore.setToken(data.access_token)
    authStore.setAuthenticated(true)
    
    // Weiterleitung zur Home-Seite nach erfolgreicher Anmeldung
    await router.push('/home')
  } catch (error: any) {
    authStore.setAuthenticated(false)
    errorMsg.value = 'Anmeldung fehlgeschlagen. Überprüfen Sie Ihre Anmeldedaten.'
    console.error(error)
  }
}

/**
 * Behandelt den Registrierungsvorgang
 * Validiert alle Eingaben inklusive Geburtsdatum und erstellt einen neuen Benutzer
 */
const handleRegister = async () => {
  errorMsg.value = ''
  successMsg.value = ''
  
  // Validierung aller erforderlichen Felder
  if (!email.value || !password.value || !birthDate.value) {
    errorMsg.value = 'Bitte geben Sie E-Mail, Passwort und Geburtsdatum für die Registrierung ein.'
    return
  }

  try {
    // Benutzerdaten für die Registrierung vorbereiten
    // HTML5 date input gibt bereits das Format YYYY-MM-DD zurück
    const userData = {
      email: email.value,
      password: password.value,
      birth_date: birthDate.value,
    }
    
    // Registrierung über den Auth-Service
    await authService.register(userData)
    successMsg.value = 'Registrierung erfolgreich! Sie können sich jetzt anmelden.'
    
    // Formular zurücksetzen und zurück zum Anmeldemodus wechseln
    email.value = ''
    password.value = ''
    birthDate.value = ''
    isRegisterMode.value = false
  } catch (error: any) {
    // Backend-Fehlermeldungen anzeigen, falls verfügbar
    if (error.response?.data?.detail) {
      errorMsg.value = error.response.data.detail
    } else {
      errorMsg.value = 'Registrierung fehlgeschlagen. Die E-Mail könnte bereits vergeben sein.'
    }
    console.error(error)
  }
}
</script>

<style scoped>
/* Fade-In Animation für das Geburtsdatum-Feld */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-in-out;
}
</style>
