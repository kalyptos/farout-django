<template>
  <div v-if="variant === 'slider'" class="portfolio-image-items">
    <NuxtImg :src="image" :alt="title" />
    <div class="content">
      <p>{{ category }}</p>
      <h3>
        <NuxtLink :to="link">{{ title }}</NuxtLink>
      </h3>
    </div>
  </div>

  <div v-else-if="variant === 'box'" class="portfolio-box-items">
    <div class="project-wrap">
      <div class="content">
        <span>{{ category }}</span>
        <h3>
          <NuxtLink :to="link" v-html="sanitizedTitle"></NuxtLink>
        </h3>
      </div>
      <p>{{ description }}</p>
    </div>
    <NuxtLink :to="link" class="radius-btn">
      <i class="fa-sharp fa-solid fa-arrow-right"></i>
      View Details
    </NuxtLink>
    <div
      v-if="hoverImage"
      class="project-hover d-none d-md-block bg-cover"
      :style="{ backgroundImage: `url('${hoverImage}')` }"
    ></div>
  </div>
</template>

<script setup lang="ts">
import DOMPurify from 'isomorphic-dompurify'

interface Props {
  title: string
  category: string
  image?: string
  hoverImage?: string
  description?: string
  link: string
  variant?: 'slider' | 'box'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'slider'
})

// SECURITY: Sanitize title to prevent XSS attacks (SSR-safe with isomorphic-dompurify)
const sanitizedTitle = computed(() => {
  return DOMPurify.sanitize(props.title, {
    ALLOWED_TAGS: ['br', 'span', 'strong', 'em', 'b', 'i'],
    ALLOWED_ATTR: ['class'],
    ALLOW_DATA_ATTR: false
  })
})
</script>

<style scoped>
/* Portfolio card styles are handled by the main template CSS */
</style>
