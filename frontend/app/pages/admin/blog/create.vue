<template>
  <div class="admin-blog-create">
    <PageHeader title="Create Blog Post" subtitle="Admin Panel" />

    <section class="section-padding">
      <div class="container">
        <div class="row">
          <div class="col-lg-8 mx-auto">
            <div class="form-card">
              <form @submit.prevent="handleSubmit" class="blog-form">
                <div class="mb-4">
                  <label class="form-label">Title</label>
                  <input
                    v-model="formData.heading"
                    type="text"
                    class="form-control"
                    placeholder="Enter post title"
                    required
                  >
                </div>

                <div class="mb-4">
                  <label class="form-label">Content</label>
                  <textarea
                    v-model="formData.content"
                    class="form-control"
                    rows="12"
                    placeholder="Write your blog post content here..."
                    required
                  ></textarea>
                  <small class="form-text">You can use line breaks for paragraphs.</small>
                </div>

                <div class="mb-4">
                  <label class="form-label">Author</label>
                  <input
                    v-model="formData.author"
                    type="text"
                    class="form-control"
                    placeholder="Enter author name"
                    required
                  >
                </div>

                <div class="mb-4">
                  <label class="form-label">Feature Image URL</label>
                  <input
                    v-model="formData.feature_image"
                    type="text"
                    class="form-control"
                    placeholder="/assets/img/blog/image.jpg"
                    required
                  >
                  <small class="form-text">Enter the path or URL to the feature image.</small>
                </div>

                <div class="mb-4">
                  <div class="form-check form-switch">
                    <input
                      v-model="formData.published"
                      type="checkbox"
                      class="form-check-input"
                      id="published"
                    >
                    <label class="form-check-label" for="published">
                      Publish immediately
                    </label>
                  </div>
                  <small class="form-text">If unchecked, the post will be saved as a draft.</small>
                </div>

                <div class="form-actions">
                  <button type="submit" class="theme-btn" :disabled="loading">
                    <i class="fa-solid fa-save me-2"></i>
                    {{ loading ? 'Creating...' : 'Create Post' }}
                  </button>
                  <NuxtLink to="/admin/blog" class="btn btn-secondary">
                    <i class="fa-solid fa-times me-2"></i>
                    Cancel
                  </NuxtLink>
                </div>

                <div v-if="error" class="alert alert-danger mt-3">
                  <i class="fa-solid fa-exclamation-circle me-2"></i>
                  {{ error?.message || error }}
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import type { BlogPostCreate } from '~/types/blog'

definePageMeta({
  layout: 'default',
  middleware: ['admin', 'force-password-change']
})

const { createBlogPost } = useBlogApi()
const router = useRouter()
const loading = ref(false)
const error = ref<Error | null>(null)

const formData = reactive<BlogPostCreate>({
  heading: '',
  content: '',
  author: '',
  feature_image: '',
  published: true
})

const handleSubmit = async () => {
  loading.value = true
  error.value = null
  try {
    const result = await createBlogPost(formData)
    if (result) {
      alert('Blog post created successfully!')
      router.push('/admin/blog')
    }
  } catch (err: unknown) {
    error.value = err instanceof Error ? err : new Error(String(err))
  } finally {
    loading.value = false
  }
}

useHead({
  title: 'Create Blog Post - Admin'
})
</script>

<style scoped lang="scss">
@use 'sass:color';

.admin-blog-create {
  min-height: 80vh;
}

.section-padding {
  padding: 60px 0;
}

.form-card {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 2.5rem;
  border: 1px solid var(--border-color);
  box-shadow: 0 2px 8px $shadow-light;
}

.blog-form {
  .form-label {
    color: var(--text-primary);
    font-weight: 600;
    margin-bottom: 0.5rem;
    display: block;
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .form-control {
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 0.75rem 1rem;
    border-radius: 6px;
    font-size: 1rem;
    transition: all 0.3s ease;
    width: 100%;

    &:focus {
      outline: none;
      border-color: var(--color-accent-1);
      box-shadow: 0 0 0 3px rgba($color-accent-1, 0.1);
      background: var(--bg-card);
    }

    &::placeholder {
      color: var(--text-muted);
    }

    &[type="text"],
    &[type="url"] {
      font-family: inherit;
    }
  }

  textarea.form-control {
    resize: vertical;
    min-height: 200px;
    font-family: inherit;
    line-height: 1.6;
  }

  .form-text {
    color: var(--text-muted);
    font-size: 0.85rem;
    margin-top: 0.35rem;
    display: block;
  }

  .form-check {
    padding-left: 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;

    .form-check-input {
      width: 50px;
      height: 26px;
      cursor: pointer;
      background-color: var(--bg-primary);
      border: 2px solid var(--border-color);
      margin: 0;

      &:checked {
        background-color: var(--color-accent-1);
        border-color: var(--color-accent-1);
      }

      &:focus {
        box-shadow: 0 0 0 3px rgba($color-accent-1, 0.2);
        outline: none;
      }
    }

    .form-check-label {
      color: var(--text-primary);
      font-weight: 500;
      cursor: pointer;
      margin: 0;
    }
  }
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border-color);

  .theme-btn,
  .btn {
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    font-weight: 600;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    display: inline-flex;
    align-items: center;

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }

    i {
      font-size: 0.9rem;
    }
  }

  .btn-secondary {
    background: var(--bg-primary);
    color: var(--text-secondary);
    border: 1px solid var(--border-color);

    &:hover {
      background: var(--bg-card);
      color: var(--text-primary);
    }
  }
}

.alert {
  padding: 1rem 1.25rem;
  border-radius: 6px;
  border: none;

  &.alert-danger {
    background: rgba($error, 0.1);
    color: $error;
    border-left: 4px solid $error;
  }
}
</style>
