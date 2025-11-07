<template>
    <div :class="['section-title', alignment && `text-${alignment}`]">
    <AnimatedElement v-if="subtitle" animation="fade-in-up">
      <h6>{{ subtitle }}</h6>
    </AnimatedElement>
    <AnimatedElement animation="fade-in-up" :delay="'.3s'">
      <h2 v-html="sanitizedTitle"></h2>
    </AnimatedElement>
  </div>
</template>

<script setup lang="ts">
import DOMPurify from 'isomorphic-dompurify'

interface Props {
  title: string
  subtitle?: string
  alignment?: 'left' | 'center' | 'right'
}

const props = withDefaults(defineProps<Props>(), {
  alignment: 'left'
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
/* Section title styles are handled by the main template CSS */
</style>
