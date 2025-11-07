<template>
  <div :class="cardClasses">
    <div class="icon">
      <NuxtImg :src="icon" :alt="title" />
    </div>
    <div class="content">
      <h3>
        <NuxtLink :to="link">{{ title }}</NuxtLink>
      </h3>
      <p>{{ description }}</p>
      <div class="service-btn">
        <NuxtLink :to="link" class="link-btn">{{ linkText }}</NuxtLink>
        <NuxtLink :to="link" class="arrow-icon">
          <NuxtImg src="/assets/img/icon/02.svg" alt="arrow" />
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  icon: string
  title: string
  description: string
  link: string
  linkText?: string
  variant?: '1' | '2'
  borderless?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  linkText: 'View Details',
  variant: '1',
  borderless: false
})

const cardClasses = computed(() => {
  const classes = ['service-box-items']
  if (props.variant === '2') classes.push('style-2')
  if (props.borderless) classes.push('border-none')
  return classes.join(' ')
})
</script>

<style scoped>
/* Service card styles are handled by the main template CSS */
</style>
