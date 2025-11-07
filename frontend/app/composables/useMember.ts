interface Member {
  id: number
  discord_id: string
  display_name: string
  bio?: string
  avatar_url?: string
  rank: string
  missions_completed: any[]
  trainings_completed: any[]
  stats: Record<string, any>
  created_at: string
  updated_at: string
}

export const useMember = () => {
  const { fetchApi } = useApi()

  const getMembers = async () => {
    try {
      return await fetchApi<Member[]>('/members')
    } catch (error) {
      console.error('Failed to fetch members:', error)
      return []
    }
  }

  const getMember = async (discordId: string) => {
    try {
      return await fetchApi<Member>(`/members/${discordId}`)
    } catch (error) {
      console.error('Failed to fetch member:', error)
      return null
    }
  }

  const updateMember = async (discordId: string, data: Partial<Member>) => {
    try {
      return await fetchApi<Member>(`/members/${discordId}`, {
        method: 'PUT',
        body: JSON.stringify(data),
        headers: { 'Content-Type': 'application/json' }
      })
    } catch (error) {
      console.error('Failed to update member:', error)
      throw error
    }
  }

  return {
    getMembers,
    getMember,
    updateMember
  }
}
