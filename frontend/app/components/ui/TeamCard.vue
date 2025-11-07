<template>
  <div :class="cardClasses">
    <div class="team-image">
      <NuxtImg :src="image" :alt="name" />
      <div v-if="variant === 'box'" class="social-icon">
        <a
          v-for="social in socialLinks"
          :key="social.platform"
          :href="social.url"
          :aria-label="social.platform"
          class="icon"
        >
          <i :class="social.icon"></i>
        </a>
      </div>
    </div>
    <div class="team-content" :class="{ 'text-center': variant === 'card' }">
      <h3>
        <NuxtLink :to="detailsLink">{{ name }}</NuxtLink>
      </h3>
      <p>{{ role }}</p>
      <div v-if="variant === 'card'" class="social-icon">
        <a
          v-for="social in socialLinks"
          :key="social.platform"
          :href="social.url"
          :aria-label="social.platform"
        >
          <i :class="social.icon"></i>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface SocialLink {
  platform: string
  url: string
  icon: string
}

interface Props {
  name: string
  role: string
  image: string
  detailsLink: string
  socialLinks: SocialLink[]
  variant?: 'box' | 'card' // box = hover social, card = always visible
  active?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'box',
  active: false
})

const cardClasses = computed(() => {
  const classes = props.variant === 'box' ? ['team-box-items'] : ['team-card-items']
  if (props.active && props.variant === 'card') classes.push('active')
  return classes.join(' ')
})
</script>

<style scoped>
/* Team card styles are handled by the main template CSS */
</style>
