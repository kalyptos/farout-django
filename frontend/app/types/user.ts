export interface UserProfile {
  username: string
  discord_id: string | null
  email: string
  role: 'admin' | 'member'
  rank: string
  rank_image: string | null
  created_at: string
  last_login: string | null
  member_id: number | null
  member_data: {
    display_name: string
    bio: string | null
    avatar_url: string | null
    missions_completed: any[]
    trainings_completed: any[]
    stats: any
    member_since: string
  } | null
}

export interface AdminUser {
  id: number
  username: string
  discord_id: string | null
  email: string
  role: 'admin' | 'member'
  rank: string
  rank_image: string | null
  is_active: boolean
  created_at: string
  last_login: string | null
}

export interface UserListResponse {
  users: AdminUser[]
  total: number
  page: number
  limit: number
  pages: number
}
