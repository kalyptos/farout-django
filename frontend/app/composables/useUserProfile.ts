import type { UserProfile } from '~/types/user'

export const useUserProfile = () => {
  const { fetchApi } = useApi()
  const profile = ref<UserProfile | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchProfile = async () => {
    loading.value = true
    error.value = null
    try {
      const data = await fetchApi<UserProfile>('/auth/user/me')
      profile.value = data
    } catch (e: any) {
      error.value = e.message || 'Failed to load profile'
      // If 401, redirect to login
      if (e.statusCode === 401 || e.status === 401) {
        await navigateTo('/login')
      }
    } finally {
      loading.value = false
    }
  }

  return {
    profile,
    loading,
    error,
    fetchProfile
  }
}
