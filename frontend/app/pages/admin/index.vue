<template>
  <div>
    <!-- Page Header -->
    <PageHeader
      title="Admin Dashboard"
      subtitle="Manage Your Organization"
      :breadcrumbs="breadcrumbs"
    />

    <!-- Admin Section -->
    <section class="admin-section section-padding">
      <div class="container">
        <!-- Welcome Message -->
        <div class="welcome-message">
          <h2>Welcome, {{ user?.username || 'Admin' }}!</h2>
          <p>Manage your organization's content and users from this dashboard.</p>
        </div>

        <div class="row g-4">
          <!-- User Management -->
          <div class="col-lg-4 col-md-6">
            <AnimatedElement animation="fade-in-up" :delay="'.3s'">
              <NuxtLink to="/admin/users" class="admin-card">
                <div class="card-icon users">
                  <i class="fa-solid fa-users"></i>
                </div>
                <h3>User Management</h3>
                <p>Manage users and permissions</p>
                <div v-if="!statsLoading" class="card-stats">
                  <div class="stat">
                    <span class="stat-value">{{ stats.totalUsers }}</span>
                    <span class="stat-label">Total Users</span>
                  </div>
                  <div class="stat">
                    <span class="stat-value">{{ stats.adminUsers }}</span>
                    <span class="stat-label">Admins</span>
                  </div>
                </div>
                <div v-else class="card-stats loading">
                  <i class="fa-solid fa-spinner fa-spin"></i>
                </div>
                <div class="card-arrow">
                  <i class="fa-solid fa-arrow-right"></i>
                </div>
              </NuxtLink>
            </AnimatedElement>
          </div>

          <!-- Blog Management -->
          <div class="col-lg-4 col-md-6">
            <AnimatedElement animation="fade-in-up" :delay="'.5s'">
              <NuxtLink to="/admin/blog" class="admin-card">
                <div class="card-icon blog">
                  <i class="fa-solid fa-blog"></i>
                </div>
                <h3>Blog Posts</h3>
                <p>Create and manage blog posts</p>
                <div v-if="!statsLoading" class="card-stats">
                  <div class="stat">
                    <span class="stat-value">{{ stats.totalBlogPosts }}</span>
                    <span class="stat-label">Total Posts</span>
                  </div>
                  <div class="stat">
                    <span class="stat-value">{{ stats.publishedBlogPosts }}</span>
                    <span class="stat-label">Published</span>
                  </div>
                </div>
                <div v-else class="card-stats loading">
                  <i class="fa-solid fa-spinner fa-spin"></i>
                </div>
                <div class="card-arrow">
                  <i class="fa-solid fa-arrow-right"></i>
                </div>
              </NuxtLink>
            </AnimatedElement>
          </div>

          <!-- Members -->
          <div class="col-lg-4 col-md-6">
            <AnimatedElement animation="fade-in-up" :delay="'.7s'">
              <NuxtLink to="/members" class="admin-card">
                <div class="card-icon members">
                  <i class="fa-solid fa-user-astronaut"></i>
                </div>
                <h3>Members</h3>
                <p>View organization members</p>
                <div class="card-arrow">
                  <i class="fa-solid fa-arrow-right"></i>
                </div>
              </NuxtLink>
            </AnimatedElement>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
  middleware: ['admin', 'force-password-change']
})

useHead({
  title: 'Admin Dashboard - FarOut Organization',
  meta: [
    {
      name: 'description',
      content: 'Admin dashboard for FarOut organization management.'
    }
  ]
})

const breadcrumbs = [
  { label: 'Home', path: '/' },
  { label: 'Admin' }
]

const { user } = useAuth()
const { fetchApi } = useApi()

const stats = ref({
  totalUsers: 0,
  adminUsers: 0,
  totalBlogPosts: 0,
  publishedBlogPosts: 0
})
const statsLoading = ref(true)

onMounted(async () => {
  await loadStats()
})

const loadStats = async () => {
  statsLoading.value = true
  try {
    // Fetch user stats
    const usersResponse = await fetchApi<any>('/admin/users?limit=1')
    stats.value.totalUsers = usersResponse.total || 0

    // Fetch admin count
    const adminsResponse = await fetchApi<any>('/admin/users?role=admin&limit=1')
    stats.value.adminUsers = adminsResponse.total || 0

    // Fetch blog stats
    const blogResponse = await fetchApi<any>('/admin/blog')
    const blogPosts = Array.isArray(blogResponse) ? blogResponse : blogResponse.posts || []
    stats.value.totalBlogPosts = blogPosts.length
    stats.value.publishedBlogPosts = blogPosts.filter((post: any) => post.published).length
  } catch (err) {
    console.error('Failed to load stats:', err)
  } finally {
    statsLoading.value = false
  }
}
</script>

<style scoped lang="scss">
.admin-section {
  padding: 100px 0;
}

.welcome-message {
  text-align: center;
  margin-bottom: 3rem;

  h2 {
    color: $text-primary;
    font-size: 2rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
  }

  p {
    color: $text-secondary;
    font-size: 1.125rem;
  }
}

.admin-card {
  display: block;
  background: $background-card;
  border-radius: 12px;
  padding: 2.5rem;
  border: 1px solid $border-color;
  text-decoration: none;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  min-height: 320px;

  &:hover {
    transform: translateY(-10px);
    border-color: $color-accent-1;
    box-shadow: 0 15px 40px rgba(17, 171, 233, 0.3);

    .card-arrow {
      transform: translateX(5px);
    }

    .card-icon {
      transform: scale(1.1);
    }
  }

  .card-icon {
    width: 70px;
    height: 70px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.5rem;
    transition: transform 0.3s ease;

    i {
      font-size: 2rem;
      color: white;
    }

    &.blog {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    &.users {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }

    &.members {
      background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
  }

  h3 {
    color: $text-primary;
    font-size: 1.5rem;
    margin-bottom: 0.75rem;
    font-weight: 600;
  }

  p {
    color: $text-secondary;
    margin-bottom: 1.5rem;
  }

  .card-stats {
    display: flex;
    gap: 1.5rem;
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid $border-color;

    &.loading {
      justify-content: center;
      padding: 1rem 0;

      i {
        font-size: 1.5rem;
        color: $color-accent-1;
      }
    }

    .stat {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;

      .stat-value {
        color: $color-accent-1;
        font-size: 1.75rem;
        font-weight: 700;
        line-height: 1;
      }

      .stat-label {
        color: $text-muted;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }
    }
  }

  .card-arrow {
    position: absolute;
    top: 2rem;
    right: 2rem;
    color: $color-accent-1;
    font-size: 1.5rem;
    transition: transform 0.3s ease;
  }
}

// Responsive
@media (max-width: 768px) {
  .welcome-message {
    h2 {
      font-size: 1.5rem;
    }

    p {
      font-size: 1rem;
    }
  }

  .admin-card {
    min-height: auto;

    .card-stats {
      flex-direction: column;
      gap: 1rem;
    }
  }
}
</style>
