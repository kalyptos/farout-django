import type { Ref } from 'vue'

interface User {
  id: number
  discord_id?: string
  username: string
  email?: string
  role: string
  must_change_password: boolean
  avatar?: string
  discriminator?: string
}

export const useAuth = () => {
  const { fetchApi } = useApi()
  const user = useState<User | null>('auth-user', () => null)
  const isAuthenticated = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  // Initialize auth state on mount
  const initAuth = async () => {
    try {
      const response = await fetchApi<User>('/auth/me')
      user.value = response
    } catch (error) {
      user.value = null
    }
  }

  // Login with username/password (local admin)
  const login = async (username: string, password: string) => {
    try {
      const response = await fetchApi<{ access_token: string }>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
        headers: { 'Content-Type': 'application/json' }
      })
      
      // Token is in httpOnly cookie, but we also get it in response
      // Fetch user info
      await initAuth()
      
      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.message || 'Login failed' }
    }
  }

  // Login with Discord
  const loginWithDiscord = async () => {
    try {
      const response = await fetchApi<{ url: string }>('/auth/discord')
      // Redirect to Discord OAuth
      window.location.href = response.url
    } catch (error) {
      console.error('Discord login failed:', error)
    }
  }

  // Logout
  const logout = async () => {
    try {
      await fetchApi('/auth/logout', { method: 'POST' })
      user.value = null
      navigateTo('/login')
    } catch (error) {
      console.error('Logout failed:', error)
    }
  }

  // Change password
  const changePassword = async (oldPassword: string, newPassword: string) => {
    try {
      await fetchApi('/auth/change-password', {
        method: 'POST',
        body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }),
        headers: { 'Content-Type': 'application/json' }
      })
      
      // Update user state to reflect password changed
      if (user.value) {
        user.value.must_change_password = false
      }
      
      return { success: true }
    } catch (error: any) {
      return { success: false, error: error.message || 'Password change failed' }
    }
  }

  return {
    user,
    isAuthenticated,
    isAdmin,
    initAuth,
    login,
    loginWithDiscord,
    logout,
    changePassword
  }
}
