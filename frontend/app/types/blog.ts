// Blog Post Types
export interface BlogPost {
  id: number
  heading: string
  content: string
  author: string
  feature_image: string
  created_at: string
  updated_at: string
  slug: string
  published: boolean
}

export interface BlogPostCreate {
  heading: string
  content: string
  author: string
  feature_image: string
  published?: boolean
}

export interface BlogPostUpdate {
  heading?: string
  content?: string
  author?: string
  feature_image?: string
  published?: boolean
}

export interface BlogPostListResponse {
  posts: BlogPost[]
  total: number
  page: number
  limit: number
  total_pages: number
}

export interface BlogAuthor {
  name: string
  avatar: string
}
