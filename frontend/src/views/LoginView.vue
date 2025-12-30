<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-50">
    <div class="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-md">
      <div class="text-center">
        <img class="w-auto h-24 mx-auto" src="../assets/logo.jpeg" alt="AstroDate Logo">
        <h2 class="mt-6 text-3xl font-extrabold text-center text-gray-900">
          Willkommen bei AstroDate
        </h2>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email-address" class="sr-only">E-Mail-Adresse</label>
            <input id="email-address" name="email" type="email" autocomplete="email" required
                   class="relative block w-full px-3 py-2 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-none appearance-none rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                   placeholder="E-Mail-Adresse" v-model="email">
          </div>
          <div>
            <label for="password" class="sr-only">Passwort</label>
            <input id="password" name="password" type="password" autocomplete="current-password" required
                   class="relative block w-full px-3 py-2 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-none appearance-none rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                   placeholder="Passwort" v-model="password">
          </div>
        </div>

        <div class="flex items-center justify-between">
          <p v-if="errorMsg" class="text-sm text-red-600">{{ errorMsg }}</p>
        </div>

        <div>
          <button type="submit" @click.prevent="handleLogin"
                  class="relative flex justify-center w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md group hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            Anmelden
          </button>
        </div>
        <div>
          <button @click.prevent="handleRegister"
                  class="relative flex justify-center w-full px-4 py-2 text-sm font-medium text-indigo-600 bg-white border border-indigo-600 rounded-md group hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            Registrierung
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const email = ref('')
const password = ref('')
const errorMsg = ref('')
const router = useRouter()
const authStore = useAuthStore()

const handleLogin = async () => {
  // TODO: Call the auth service
  console.log('Login attempt with:', email.value)
  // Placeholder logic
  if (email.value && password.value) {
    authStore.setToken('fake-token-for-now')
    await router.push('/home')
  } else {
    errorMsg.value = 'Bitte geben Sie E-Mail und Passwort ein.'
  }
}

const handleRegister = async () => {
  // TODO: Call the auth service
  console.log('Register attempt with:', email.value)
  errorMsg.value = 'Registrierung ist noch nicht implementiert.'
}
</script>
