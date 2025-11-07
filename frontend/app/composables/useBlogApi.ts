import type {
  BlogPost,
  BlogPostCreate,
  BlogPostUpdate,
  BlogPostListResponse
} from '~/types/blog'

export function useBlogApi() {
  const { get, post, put, delete: del, loading, error } = useApi()

  /**
   * Fetch paginated list of published blog posts (public endpoint)
   */
  const fetchBlogPosts = async (
    page: number = 1,
    limit: number = 10,
    sort: 'newest' | 'oldest' = 'newest'
  ): Promise<BlogPostListResponse | null> => {
    return await get<BlogPostListResponse>(
      `/api/blog?page=${page}&limit=${limit}&sort=${sort}`
    )
  }

  /**
   * Fetch a single published blog post by slug (public endpoint)
   */
  const fetchBlogPost = async (slug: string): Promise<BlogPost | null> => {
    return await get<BlogPost>(`/api/blog/${slug}`)
  }

  /**
   * Fetch ALL blog posts including unpublished (admin endpoint)
   */
  const fetchAllBlogPosts = async (
    page: number = 1,
    limit: number = 10,
    sort: 'newest' | 'oldest' = 'newest'
  ): Promise<BlogPostListResponse | null> => {
    return await get<BlogPostListResponse>(
      `/api/admin/blog?page=${page}&limit=${limit}&sort=${sort}`
    )
  }

  /**
   * Fetch a single blog post by ID (admin endpoint)
   */
  const fetchBlogPostById = async (id: number): Promise<BlogPost | null> => {
    return await get<BlogPost>(`/api/admin/blog/${id}`)
  }

  /**
   * Create a new blog post (admin endpoint)
   */
  const createBlogPost = async (
    data: BlogPostCreate
  ): Promise<BlogPost | null> => {
    return await post<BlogPost>('/api/admin/blog', data)
  }

  /**
   * Update an existing blog post (admin endpoint)
   */
  const updateBlogPost = async (
    id: number,
    data: BlogPostUpdate
  ): Promise<BlogPost | null> => {
    return await put<BlogPost>(`/api/admin/blog/${id}`, data)
  }

  /**
   * Delete a blog post (admin endpoint)
   */
  const deleteBlogPost = async (
    id: number
  ): Promise<{ success: boolean; message: string; deleted_id: number } | null> => {
    return await del(`/api/admin/blog/${id}`)
  }

  return {
    // State
    loading,
    error,

    // Public methods
    fetchBlogPosts,
    fetchBlogPost,

    // Admin methods
    fetchAllBlogPosts,
    fetchBlogPostById,
    createBlogPost,
    updateBlogPost,
    deleteBlogPost
  }
}
