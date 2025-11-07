<template>
  <div class="breadcrumb-wrapper section-bg bg-cover" :style="backgroundStyle">
    <!-- Decorative Shapes -->
    <div class="arrow-shape">
      <NuxtImg src="/assets/img/arrow-shape.png" alt="arrow" />
    </div>
    <div class="circle-shape">
      <NuxtImg src="/assets/img/circle-shape.png" alt="circle" />
    </div>

    <!-- Page Heading & Breadcrumbs -->
    <div class="container">
      <div class="page-heading">
        <!-- Subtitle (optional) -->
        <AnimatedElement v-if="subtitle" animation="fade-in-up" :delay="'.2s'">
          <p class="breadcrumb-subtitle">{{ subtitle }}</p>
        </AnimatedElement>

        <!-- Main Title -->
        <div class="breadcrumb-sub-title">
          <AnimatedElement animation="fade-in-up" :delay="'.3s'">
            <h1>{{ title }}</h1>
          </AnimatedElement>
        </div>

        <!-- Breadcrumb Navigation -->
        <AnimatedElement animation="fade-in-up" :delay="'.5s'">
          <ul class="breadcrumb-items">
            <li v-for="(crumb, index) in breadcrumbs" :key="index">
              <NuxtLink v-if="crumb.path" :to="crumb.path">
                {{ crumb.label }}
              </NuxtLink>
              <span v-else>{{ crumb.label }}</span>
              <i v-if="index < breadcrumbs.length - 1" class="fa-regular fa-chevrons-right"></i>
            </li>
          </ul>
        </AnimatedElement>
      </div>
    </div>

    <!-- Marquee Section -->
    <div v-if="showMarquee" class="marquee-section fix">
      <div class="mycustom-marque">
        <div class="scrolling-wrap">
          <div class="comm">
            <div class="cmn-textslide textitalick text-custom-storke">{{ marqueeText }}</div>
            <div class="cmn-textslide textitalick">{{ marqueeText }}</div>
            <div class="cmn-textslide textitalick text-custom-storke">{{ marqueeText }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Breadcrumb {
  label: string
  path?: string
}

interface Props {
  title: string
  subtitle?: string
  breadcrumbs?: Breadcrumb[]
  backgroundImage?: string
  showMarquee?: boolean
  marqueeText?: string
}

const props = withDefaults(defineProps<Props>(), {
  breadcrumbs: () => [
    { label: 'Home', path: '/' },
    { label: 'Current Page' }
  ],
  backgroundImage: '/assets/img/breadcrumb-shape.png',
  showMarquee: true,
  marqueeText: undefined
})

const backgroundStyle = computed(() => ({
  backgroundImage: `url('${props.backgroundImage}')`
}))

// Use title as marquee text if not provided
const marqueeText = computed(() => props.marqueeText || props.title.toUpperCase())
</script>

<style scoped>
/* Component-specific styles if needed */
/* Most styles come from the template's main.css */

.breadcrumb-subtitle {
  color: var(--color-accent-1);
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 1rem;
}
</style>
