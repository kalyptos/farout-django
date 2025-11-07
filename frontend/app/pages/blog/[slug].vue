<template>
  <!-- Loading State -->
  <div v-if="loading">
    <!-- Breadcrumb -->
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
            <h1 class="wow fadeInUp" data-wow-delay=".3s">Loading...</h1>
          </div>
          <ul class="breadcrumb-items wow fadeInUp" data-wow-delay=".5s">
            <li><NuxtLink to="/">Home</NuxtLink></li>
            <li><i class="fa-regular fa-chevrons-right"></i></li>
            <li><NuxtLink to="/blog">Blog</NuxtLink></li>
            <li><i class="fa-regular fa-chevrons-right"></i></li>
            <li>Loading...</li>
          </ul>
        </div>
      </div>
      <div class="marquee-section fix">
        <div class="mycustom-marque">
          <div class="scrolling-wrap">
            <div class="comm">
              <div class="cmn-textslide textitalick text-custom-storke">LOADING</div>
              <div class="cmn-textslide textitalick">LOADING</div>
              <div class="cmn-textslide textitalick text-custom-storke">LOADING</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <section class="section-padding">
      <div class="container text-center">
        <p>Loading post...</p>
      </div>
    </section>
  </div>

  <!-- Error State -->
  <div v-else-if="error || !post">
    <!-- Breadcrumb -->
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
            <h1 class="wow fadeInUp" data-wow-delay=".3s">POST NOT FOUND</h1>
          </div>
          <ul class="breadcrumb-items wow fadeInUp" data-wow-delay=".5s">
            <li><NuxtLink to="/">Home</NuxtLink></li>
            <li><i class="fa-regular fa-chevrons-right"></i></li>
            <li><NuxtLink to="/blog">Blog</NuxtLink></li>
            <li><i class="fa-regular fa-chevrons-right"></i></li>
            <li>Not Found</li>
          </ul>
        </div>
      </div>
    </div>

    <section class="section-padding">
      <div class="container text-center">
        <div class="alert alert-danger">
          <h4>Error loading post</h4>
          <p>{{ error?.message || 'Post not found' }}</p>
          <NuxtLink to="/blog" class="theme-btn mt-3">Back to Blog</NuxtLink>
        </div>
      </div>
    </section>
  </div>

  <!-- Post Content -->
  <div v-else>
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
            <h1 class="wow fadeInUp" data-wow-delay=".3s">BLOG DETAILS</h1>
          </div>
          <ul class="breadcrumb-items wow fadeInUp" data-wow-delay=".5s">
            <li><NuxtLink to="/">Home</NuxtLink></li>
            <li><i class="fa-regular fa-chevrons-right"></i></li>
            <li><NuxtLink to="/blog">Blog</NuxtLink></li>
            <li><i class="fa-regular fa-chevrons-right"></i></li>
            <li>{{ post.heading }}</li>
          </ul>
        </div>
      </div>
      <div class="marquee-section fix">
        <div class="mycustom-marque">
          <div class="scrolling-wrap">
            <div class="comm">
              <div class="cmn-textslide textitalick text-custom-storke">BLOG DETAILS</div>
              <div class="cmn-textslide textitalick">BLOG DETAILS</div>
              <div class="cmn-textslide textitalick text-custom-storke">BLOG DETAILS</div>
            </div>
            <div class="comm">
              <div class="cmn-textslide textitalick text-custom-storke">BLOG DETAILS</div>
              <div class="cmn-textslide textitalick">BLOG DETAILS</div>
              <div class="cmn-textslide textitalick text-custom-storke">BLOG DETAILS</div>
            </div>
            <div class="comm">
              <div class="cmn-textslide textitalick text-custom-storke">BLOG DETAILS</div>
              <div class="cmn-textslide textitalick">BLOG DETAILS</div>
              <div class="cmn-textslide textitalick text-custom-storke">BLOG DETAILS</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Blog Section Start -->
    <section class="news-details-section fix section-padding">
      <div class="container">
        <div class="news-details-area">
          <div class="row g-4">
            <!-- Main Content -->
            <div class="col-12 col-lg-8">
              <div class="blog-post-details">
                <div class="single-blog-post">
                  <!-- Featured Image -->
                  <div
                    class="post-featured-thumb bg-cover"
                    :style="{ backgroundImage: `url('${post.feature_image}')` }"
                  ></div>

                  <!-- Post Content -->
                  <div class="post-content">
                    <!-- Post Meta -->
                    <ul class="post-list d-flex align-items-center">
                      <li>
                        <i class="fa-regular fa-user"></i>
                        By {{ post.author }}
                      </li>
                      <li>
                        <i class="fa-solid fa-calendar-days"></i>
                        {{ formatDate(post.created_at) }}
                      </li>
                      <li>
                        <i class="fa-solid fa-tag"></i>
                        News
                      </li>
                    </ul>

                    <!-- Post Title -->
                    <h3>{{ post.heading }}</h3>

                    <!-- Post Content -->
                    <div v-html="formatContent(post.content)"></div>
                  </div>
                </div>

                <!-- Tags & Share -->
                <div class="row tag-share-wrap mt-4 mb-5">
                  <div class="col-lg-8 col-12">
                    <div class="tagcloud">
                      <span>Tags:</span>
                      <NuxtLink to="/blog?tag=starcitizen">Star Citizen</NuxtLink>
                      <NuxtLink to="/blog?tag=organization">Organization</NuxtLink>
                      <NuxtLink to="/blog?tag=news">News</NuxtLink>
                    </div>
                  </div>
                  <div class="col-lg-4 col-12 mt-3 mt-lg-0 text-lg-end">
                    <div class="social-share">
                      <span class="me-3">Share:</span>
                      <a href="#"><i class="fab fa-facebook-f"></i></a>
                      <a href="#"><i class="fab fa-twitter"></i></a>
                      <a href="#"><i class="fab fa-linkedin-in"></i></a>
                      <a href="#"><i class="fab fa-youtube"></i></a>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Sidebar -->
            <div class="col-12 col-lg-4">
              <BlogSidebar />
            </div>
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
import DOMPurify from 'isomorphic-dompurify'

const route = useRoute()
const slug = route.params.slug as string

// Fetch blog post from API
const { fetchBlogPost, loading, error } = useBlogApi()
const post = ref<BlogPost | null>(null)

// Load post
const loadPost = async () => {
  const response = await fetchBlogPost(slug)
  if (response) {
    post.value = response
  }
}

// Load post on client-side mount to prevent SSR hanging
onMounted(async () => {
  await loadPost()
})

// Format date
const formatDate = (dateString: string) => {
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

// Format content - preserve line breaks and SANITIZE to prevent XSS (SSR-safe with isomorphic-dompurify)
const formatContent = (content: string) => {
  if (!content) return ''
  // Replace newlines with <br> and wrap paragraphs
  const paragraphs = content.split('\n\n').filter(p => p.trim())
  const html = paragraphs.map(p => `<p class="mb-3">${p.replace(/\n/g, '<br>')}</p>`).join('')

  // SECURITY: Sanitize HTML to prevent XSS attacks (SSR-safe with isomorphic-dompurify)
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['p', 'br', 'b', 'i', 'em', 'strong', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'code', 'pre'],
    ALLOWED_ATTR: ['href', 'target', 'rel', 'class'],
    ALLOW_DATA_ATTR: false
  })
}

// SEO - CRITICAL FIX: Use function form of useHead to make it reactive
useHead(() => {
  if (loading.value) {
    return {
      title: 'Loading... - FarOut Blog',
      meta: [
        { name: 'description', content: 'Loading blog post' }
      ]
    }
  }

  if (error.value || !post.value) {
    return {
      title: 'Post Not Found - FarOut Blog',
      meta: [
        { name: 'description', content: 'The requested blog post was not found' }
      ]
    }
  }

  return {
    title: `${post.value.heading} - FarOut Blog`,
    meta: [
      {
        name: 'description',
        content: post.value.content.substring(0, 160)
      }
    ]
  }
})
</script>

<style scoped lang="scss">
.post-featured-thumb {
  height: 500px;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.post-content {
  ::v-deep(p) {
    line-height: 1.8;
    color: var(--text-secondary, #ddd);
    margin-bottom: 1.5rem;
  }

  ::v-deep(img) {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 1rem 0;
  }

  ::v-deep(h1),
  ::v-deep(h2),
  ::v-deep(h3),
  ::v-deep(h4) {
    color: var(--text-primary, #fff);
    margin-top: 2rem;
    margin-bottom: 1rem;
  }
}
</style>
