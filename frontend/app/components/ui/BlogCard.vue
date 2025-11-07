<template>
  <div class="news-box-items mt-0">
    <div class="news-image">
      <img :src="image" :alt="title">
      <img :src="image" :alt="title">
    </div>
    <div class="news-content">
      <p>{{ formattedDate }}</p>
      <h3>
        <NuxtLink :to="link">{{ title }}</NuxtLink>
      </h3>
      <div class="news-btn">
        <NuxtLink :to="link" class="link-btn">{{ linkText }}</NuxtLink>
        <NuxtLink :to="link" class="arrow-icon">
          <img src="/assets/img/icon/02.svg" alt="img">
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title: string
  excerpt: string
  image: string
  date: string | Date
  link: string
  linkText?: string
}

const props = withDefaults(defineProps<Props>(), {
  linkText: 'View Details'
})

const formattedDate = computed(() => {
  if (typeof props.date === 'string') {
    return props.date
  }
  // Format Date object if needed
  return props.date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})
</script>

<style scoped>
/* Blog card styles are handled by the main template CSS */
</style>
