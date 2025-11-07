export default defineNuxtRouteMiddleware(async (to, from) => {
  // Skip auth check during server-side rendering
  // Auth will be checked on client-side after hydration
  if (process.server) {
    return
  }

  const { user, initAuth } = useAuth()

  // Initialize auth if not already done
  if (!user.value) {
    await initAuth()
  }

  // If still no user, redirect to login
  if (!user.value) {
    return navigateTo('/login')
  }
})
