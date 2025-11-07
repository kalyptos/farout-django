<template>
  <section class="lets-talk-section fix section-padding" :class="[bgSection ? 'section-bg' : '', paddingBottom]">
    <div class="container">
      <div class="lets-talk-wrapper">
                <AnimatedElement animation="fade-in-up" :delay="'.3s'">
          <h2 v-html="sanitizedTitle"></h2>
        </AnimatedElement>
                <AnimatedElement animation="fade-in-up" :delay="'.5s'">
          <BaseButton
            :to="ctaLink"
            variant="theme-btn"
          >
            {{ ctaText }}
          </BaseButton>
        </AnimatedElement>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import DOMPurify from 'isomorphic-dompurify'

interface Props {
  title: string
  ctaText: string
  ctaLink: string
  bgSection?: boolean
  paddingBottom?: 'pb-0' | ''
}

const props = withDefaults(defineProps<Props>(), {
  bgSection: false,
  paddingBottom: 'pb-0'
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
/* Let's talk section styles are handled by the main template CSS */
</style>
