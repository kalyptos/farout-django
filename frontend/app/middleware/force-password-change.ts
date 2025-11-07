export default defineNuxtRouteMiddleware(async (to, from) => {
  const { user, initAuth } = useAuth()

  // Initialize auth if not already done
  if (!user.value) {
    await initAuth()
  }

  // If user must change password, redirect to change password page
  if (user.value?.must_change_password && to.path !== '/change-password') {
    return navigateTo('/change-password')
  }
})
