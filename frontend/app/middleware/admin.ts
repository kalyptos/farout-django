export default defineNuxtRouteMiddleware(async (to, from) => {
  // Skip middleware during server-side rendering
  // Auth will be checked on client-side after hydration
  if (process.server) {
    return
  }

  const { user, initAuth, isAdmin } = useAuth()

  // Initialize auth if not already done
  if (!user.value) {
    await initAuth()
  }

  // If no user, redirect to login
  if (!user.value) {
    return navigateTo('/login')
  }

  // If not admin, redirect to user dashboard
  if (!isAdmin.value) {
    return navigateTo('/user')
  }
})
