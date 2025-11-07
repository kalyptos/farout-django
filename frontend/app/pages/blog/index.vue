<template>
  <div>
    <!-- Breadcrumb Section -->
    <div class="breadcrumb-wrapper section-bg bg-cover" style="background-image: url('/assets/img/breadcrumb-shape.png');">
      <div class="arrow-shape">
        <img src="/assets/img/arrow-shape.png" alt="img">
      </div>
      <div class="circle-shape">
        <img src="/assets/img/circle-shape.png" alt="img">
      </div>
      <div class="container">
        <div class="page-heading">
          <div class="breadcrumb-sub-title">
            <h1 class="wow fadeInUp" data-wow-delay=".3s">BLOG</h1>
          </div>
          <ul class="breadcrumb-items wow fadeInUp" data-wow-delay=".5s">
            <li>
              <NuxtLink to="/">Home</NuxtLink>
            </li>
            <li>
              <i class="fa-regular fa-chevrons-right"></i>
            </li>
            <li>Blog</li>
          </ul>
        </div>
      </div>
      <div class="marquee-section fix">
        <div class="mycustom-marque">
          <div class="scrolling-wrap">
            <div class="comm">
              <div class="cmn-textslide textitalick text-custom-storke">BLOG</div>
              <div class="cmn-textslide textitalick">BLOG</div>
              <div class="cmn-textslide textitalick text-custom-storke">BLOG</div>
            </div>
            <div class="comm">
              <div class="cmn-textslide textitalick text-custom-storke">BLOG</div>
              <div class="cmn-textslide textitalick">BLOG</div>
              <div class="cmn-textslide textitalick text-custom-storke">BLOG</div>
            </div>
            <div class="comm">
              <div class="cmn-textslide textitalick text-custom-storke">BLOG</div>
              <div class="cmn-textslide textitalick">BLOG</div>
              <div class="cmn-textslide textitalick text-custom-storke">BLOG</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- News Section Start -->
    <section class="news-section fix section-padding">
      <div class="container">
        <!-- Loading State -->
        <div v-if="loading" class="text-center">
          <p>Loading blog posts...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center">
          <div class="alert alert-danger">
            <h4>Error loading blog posts</h4>
            <p>{{ error.message }}</p>
          </div>
        </div>

        <!-- No Posts -->
        <div v-else-if="!posts.length" class="text-center">
          <h3>No blog posts yet</h3>
          <p>Check back soon for updates!</p>
        </div>

        <!-- Blog Posts Grid -->
        <div v-else>
          <div class="row g-4">
            <div
              v-for="(post, index) in posts"
              :key="post.id"
              class="col-xl-4 col-lg-6 col-md-6 wow fadeInUp"
              :data-wow-delay="`.${3 + index * 2}s`"
            >
              <BlogCard
                :title="post.heading"
                :excerpt="getExcerpt(post.content)"
                :image="post.feature_image"
                :date="formatDate(post.created_at)"
                :link="`/blog/${post.slug}`"
              />
            </div>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="page-nav-wrap pt-5 text-center wow fadeInUp" data-wow-delay=".3s">
            <ul>
              <li>
                <a
                  class="page-numbers icon"
                  :class="{ disabled: currentPage === 1 }"
                  @click.prevent="changePage(currentPage - 1)"
                  href="#"
                >
                  <i class="fa-solid fa-arrow-left-long"></i>
                </a>
              </li>
              <li v-for="page in totalPages" :key="page">
                <a
                  class="page-numbers"
                  :class="{ active: page === currentPage }"
                  @click.prevent="changePage(page)"
                  href="#"
                >
                  {{ String(page).padStart(2, '0') }}
                </a>
              </li>
              <li>
                <a
                  class="page-numbers icon"
                  :class="{ disabled: currentPage === totalPages }"
                  @click.prevent="changePage(currentPage + 1)"
                  href="#"
                >
                  <i class="fa-solid fa-arrow-right-long"></i>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Lets Talk Section -->
    <LetsTalkSection />
  </div>
</template>

<script setup lang="ts">
import type { BlogPost } from '~/types/blog'

useHead({
  title: 'Blog & News - FarOut Organization',
  meta: [
    {
      name: 'description',
      content: 'Stay updated with the latest news, events, and updates from FarOut organization.'
    }
  ]
})

// Fetch blog posts from API
const { fetchBlogPosts, loading, error } = useBlogApi()
const posts = ref<BlogPost[]>([])
const currentPage = ref(1)
const totalPages = ref(1)

// Load posts on mount
const loadPosts = async (page: number = 1) => {
  const response = await fetchBlogPosts(page, 9, 'newest')
  if (response) {
    posts.value = response.posts
    currentPage.value = response.page
    totalPages.value = response.total_pages
  }
}

// Load posts on client-side mount to prevent SSR hanging
onMounted(async () => {
  await loadPosts()
})

// Change page
const changePage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    loadPosts(page)
  }
}

// Helper functions
const getExcerpt = (content: string, length: number = 150): string => {
  if (!content) return ''
  return content.length > length
    ? content.substring(0, length) + '...'
    : content
}

const formatDate = (dateString: string): string => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch (e) {
    return dateString
  }
}

const getReadTime = (content: string): string => {
  if (!content) return '1 min read'
  const wordsPerMinute = 200
  const words = content.split(/\s+/).length
  const minutes = Math.ceil(words / wordsPerMinute)
  return `${minutes} min read`
}
</script>
