<template>
  <div class="callback-page">
    <div class="container">
      <div class="callback-container">
        <div class="spinner-wrapper">
          <div class="spinner"></div>
        </div>
        <h2>{{ message }}</h2>
        <p v-if="!error">Please wait while we complete your authentication...</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

useHead({
  title: 'Discord Authentication - FarOut Organization'
})

const route = useRoute()
const { initAuth } = useAuth()
const message = ref('Completing Discord authentication...')
const error = ref(false)

onMounted(async () => {
  const code = route.query.code as string

  if (!code) {
    message.value = 'Authentication failed - no code provided'
    error.value = true
    setTimeout(() => navigateTo('/login'), 2000)
    return
  }

  try {
    // The backend handles the callback and sets the cookie
    // We just need to initialize auth and redirect
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase
    
    // Call backend callback endpoint (this will set the cookie)
    const response = await fetch(`${apiBase}/api/auth/discord/callback?code=${code}`, {
      credentials: 'include'
    })

    if (response.ok) {
      // Initialize auth state
      await initAuth()
      
      message.value = 'Success! Redirecting...'
      
      // Check user role and redirect appropriately
      const { user } = useAuth()
      if (user.value?.role === 'admin') {
        setTimeout(() => navigateTo('/admin'), 1000)
      } else {
        setTimeout(() => navigateTo('/user'), 1000)
      }
    } else {
      throw new Error('Authentication failed')
    }
  } catch (err) {
    console.error('Discord callback error:', err)
    message.value = 'Authentication failed. Redirecting to login...'
    error.value = true
    setTimeout(() => navigateTo('/login'), 2000)
  }
})
</script>

<style scoped lang="scss">
.callback-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.callback-container {
  text-align: center;
  background: var(--bg-card);
  border-radius: 12px;
  padding: 3rem;
  border: 1px solid var(--border-color);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  max-width: 500px;
  width: 100%;
}

.spinner-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(17, 171, 233, 0.2);
  border-top-color: var(--color-accent-1);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

h2 {
  color: var(--text-primary);
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

p {
  color: var(--text-secondary);
  font-size: 1rem;
  margin: 0;
}
</style>
