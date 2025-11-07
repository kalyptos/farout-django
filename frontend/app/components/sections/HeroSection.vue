<template>
  <section class="hero-section hero-2 section-padding">
    <div class="container">
      <div class="row">
        <div class="col-lg-12">
          <div class="hero-content">
                        <AnimatedElement animation="fade-in-up" :delay="'.3s'">
              <h1 v-html="sanitizedTitle"></h1>
            </AnimatedElement>
            <div class="content">
              <p data-animation="fade-in-up">
                {{ description }}
              </p>
              <BaseButton
                v-if="ctaText"
                :to="ctaLink"
                variant="theme-btn"
                data-animation="fade-in-up"
              >
                {{ ctaText }}
              </BaseButton>
            </div>
          </div>
        </div>
      </div>
      <div class="row g-4">
                <AnimatedElement animation="fade-in-up" :delay="'.3s'" class="col-xl-9">
          <div class="hero-image">
            <NuxtImg :src="heroImage" alt="hero" />
          </div>
        </AnimatedElement>
        <div v-if="stats && stats.length" class="col-xl-3">
          <div class="hero-counter">
                        <AnimatedElement
              v-for="(stat, index) in stats"
              :key="index"
              animation="fade-in-up"
              :delay="`${0.3 + index * 0.2}s`"
            >
              <CounterItem
                :value="stat.value"
                :unit="stat.unit"
                :label="stat.label"
                :active="stat.active"
              />
            </AnimatedElement>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Stat } from '~/types'
import DOMPurify from 'isomorphic-dompurify'

interface Props {
  title: string
  description: string
  heroImage: string
  ctaText?: string
  ctaLink?: string
  stats?: Stat[]
}

const props = defineProps<Props>()

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
/* Hero section styles are handled by the main template CSS */
</style>
