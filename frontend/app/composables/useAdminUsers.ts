import type { AdminUser, UserListResponse } from '~/types/user'

export const useAdminUsers = () => {
  const { fetchApi } = useApi()
  
  const users = ref<AdminUser[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const total = ref(0)
  const page = ref(1)
  const limit = ref(20)
  const pages = ref(0)
  const search = ref('')
  const roleFilter = ref<'' | 'admin' | 'member'>('')
  
  const fetchUsers = async () => {
    loading.value = true
    error.value = null
    try {
      const params = new URLSearchParams({
        page: page.value.toString(),
        limit: limit.value.toString(),
      })
      if (search.value) params.append('search', search.value)
      if (roleFilter.value) params.append('role', roleFilter.value)
      
      const data = await fetchApi<UserListResponse>(`/admin/users?${params}`)
      users.value = data.users
      total.value = data.total
      pages.value = data.pages
    } catch (e: any) {
      error.value = e.message || 'Failed to load users'
      if (e.statusCode === 403 || e.status === 403) {
        // Not admin, redirect to user dashboard
        await navigateTo('/user')
      }
    } finally {
      loading.value = false
    }
  }
  
  const changeRole = async (userId: number, newRole: 'admin' | 'member') => {
    try {
      await fetchApi(`/admin/users/${userId}/role`, {
        method: 'PUT',
        body: JSON.stringify({ role: newRole }),
        headers: { 'Content-Type': 'application/json' }
      })
      await fetchUsers() // Refresh list
      return { success: true, message: 'Role updated successfully' }
    } catch (e: any) {
      return { success: false, error: e.message || 'Failed to update role' }
    }
  }
  
  const changeRank = async (userId: number, rank: string, rankImage: string | null) => {
    try {
      await fetchApi(`/admin/users/${userId}/rank`, {
        method: 'PUT',
        body: JSON.stringify({ rank, rank_image: rankImage }),
        headers: { 'Content-Type': 'application/json' }
      })
      await fetchUsers() // Refresh list
      return { success: true, message: 'Rank updated successfully' }
    } catch (e: any) {
      return { success: false, error: e.message || 'Failed to update rank' }
    }
  }
  
  const deleteUser = async (userId: number) => {
    try {
      await fetchApi(`/admin/users/${userId}`, {
        method: 'DELETE'
      })
      await fetchUsers() // Refresh list
      return { success: true, message: 'User deleted successfully' }
    } catch (e: any) {
      return { success: false, error: e.message || 'Failed to delete user' }
    }
  }
  
  const nextPage = () => {
    if (page.value < pages.value) {
      page.value++
      fetchUsers()
    }
  }
  
  const prevPage = () => {
    if (page.value > 1) {
      page.value--
      fetchUsers()
    }
  }
  
  const goToPage = (pageNum: number) => {
    if (pageNum >= 1 && pageNum <= pages.value) {
      page.value = pageNum
      fetchUsers()
    }
  }
  
  const resetFilters = () => {
    search.value = ''
    roleFilter.value = ''
    page.value = 1
    fetchUsers()
  }
  
  return {
    users,
    loading,
    error,
    total,
    page,
    limit,
    pages,
    search,
    roleFilter,
    fetchUsers,
    changeRole,
    changeRank,
    deleteUser,
    nextPage,
    prevPage,
    goToPage,
    resetFilters
  }
}
