<template>
  <div class="admin-blog">
    <PageHeader title="Manage Blog Posts" subtitle="Admin Panel" />

    <section class="section-padding">
      <div class="container">
        <div class="mb-4">
          <NuxtLink to="/admin/blog/create" class="theme-btn">
            <i class="fa-solid fa-plus me-2"></i>
            Add New Post
          </NuxtLink>
        </div>

        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
          <p class="mt-3">Loading posts...</p>
          <p class="text-muted mt-2">If this takes too long, check your internet connection</p>
        </div>

        <div v-else-if="error" class="alert alert-danger">
          Error: {{ error?.message || error }}
        </div>

        <div v-else class="table-responsive">
          <table class="table admin-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Author</th>
                <th>Status</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="post in posts" :key="post.id">
                <td>{{ post.heading }}</td>
                <td>{{ post.author }}</td>
                <td>
                  <span :class="['status-badge', post.published ? 'published' : 'draft']">
                    {{ post.published ? 'Published' : 'Draft' }}
                  </span>
                </td>
                <td>{{ formatDate(post.created_at) }}</td>
                <td>
                  <div class="action-buttons">
                    <NuxtLink :to="`/blog/${post.slug}`" class="btn btn-sm btn-info" target="_blank">
                      <i class="fa-solid fa-eye"></i>
                    </NuxtLink>
                    <NuxtLink :to="`/admin/blog/${post.id}`" class="btn btn-sm btn-primary">
                      <i class="fa-solid fa-pen"></i>
                    </NuxtLink>
                    <button @click="deletePost(post.id)" class="btn btn-sm btn-danger">
                      <i class="fa-solid fa-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>

          <div v-if="posts.length === 0" class="text-center py-5">
            <p class="text-muted">No blog posts found. Create your first post!</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import type { BlogPost } from '~/types/blog'

definePageMeta({
  layout: 'default',
  middleware: ['admin', 'force-password-change']
})

const { fetchAllBlogPosts, deleteBlogPost } = useBlogApi()
const posts = ref<BlogPost[]>([])
const loading = ref(false)
const error = ref<Error | null>(null)
let loadingTimeout: NodeJS.Timeout | null = null

const loadPosts = async () => {
  loading.value = true
  error.value = null

  // Safety timeout: force loading to false after 10 seconds
  if (loadingTimeout) clearTimeout(loadingTimeout)
  loadingTimeout = setTimeout(() => {
    loading.value = false
    error.value = new Error('Request timeout - API took too long to respond')
  }, 10000)

  try {
    const response = await fetchAllBlogPosts(1, 50)

    if (response) {
      posts.value = response.posts
    } else {
      error.value = new Error('Failed to load posts - no response from server')
    }
  } catch (err: unknown) {
    error.value = err instanceof Error ? err : new Error(String(err))
  } finally {
    if (loadingTimeout) clearTimeout(loadingTimeout)
    loading.value = false
  }
}

// Load posts on client-side mount to prevent SSR hanging
onMounted(() => {
  // Use nextTick to ensure DOM is ready
  nextTick(() => {
    loadPosts().catch(err => {
      loading.value = false
      error.value = err
    })
  })
})

const deletePost = async (id: number) => {
  if (confirm('Are you sure you want to delete this post? This action cannot be undone.')) {
    await deleteBlogPost(id)
    await loadPosts()
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

useHead({
  title: 'Manage Blog Posts - Admin'
})
</script>

<style scoped lang="scss">
@use 'sass:color';

.admin-blog {
  min-height: 80vh;
}

.section-padding {
  padding: 60px 0;
}

.admin-table {
  background: var(--bg-card);
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border-color);

  thead {
    background: rgba($color-accent-1, 0.1);

    th {
      color: var(--text-primary);
      font-weight: 600;
      padding: 1rem;
      border: none;
      text-transform: uppercase;
      font-size: 0.85rem;
      letter-spacing: 0.5px;
    }
  }

  tbody {
    tr {
      border-bottom: 1px solid var(--border-color);
      transition: background 0.2s ease;

      &:hover {
        background: rgba($color-accent-1, 0.05);
      }

      &:last-child {
        border-bottom: none;
      }

      td {
        padding: 1rem;
        color: var(--text-secondary);
        vertical-align: middle;

        &:first-child {
          color: var(--text-primary);
          font-weight: 500;
        }
      }
    }
  }
}

.status-badge {
  padding: 0.35rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
  display: inline-block;

  &.published {
    background: rgba($success, 0.2);
    color: $success;
  }

  &.draft {
    background: rgba($warning, 0.2);
    color: $warning;
  }
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  align-items: center;

  .btn {
    padding: 0.4rem 0.75rem;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease;
    border-radius: 4px;

    &:hover {
      transform: translateY(-2px);
    }

    i {
      font-size: 0.9rem;
    }
  }

  .btn-info {
    background: $info;
    color: $color-light;

    &:hover {
      background: color.adjust($info, $lightness: -10%);
    }
  }

  .btn-primary {
    background: var(--color-accent-1);
    color: $color-dark;

    &:hover {
      background: color.adjust($color-accent-1, $lightness: -10%);
    }
  }

  .btn-danger {
    background: $error;
    color: $color-light;

    &:hover {
      background: color.adjust($error, $lightness: -10%);
    }
  }
}

.theme-btn {
  i {
    transition: transform 0.2s ease;
  }

  &:hover i {
    transform: scale(1.1);
  }
}

.spinner-border {
  width: 3rem;
  height: 3rem;
  border-width: 0.3rem;
}
</style>
