<template>
  <section :class="sectionClasses">
    <div class="container">
      <div class="section-title-area">
        <SectionTitle :subtitle="subtitle" :title="title" />
                <AnimatedElement animation="fade-in-up" :delay="'.5s'">
          <BaseButton
            v-if="showAllLink"
            :to="allServicesLink"
            variant="theme-btn"
          >
            See All Services
          </BaseButton>
        </AnimatedElement>
      </div>
      <div :class="variant === '1' ? 'row g-0' : 'row'">
                <AnimatedElement
          v-for="(service, index) in services"
          :key="service.id"
          :class="columnClass"
          animation="fade-in-up"
          :delay="`${0.2 + index * 0.2}s`"
        >
          <ServiceCard
            :icon="service.icon"
            :title="service.title"
            :description="service.description"
            :link="service.link"
            :variant="variant"
            :borderless="index === services.length - 1 && variant === '1'"
          />
        </AnimatedElement>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Service } from '~/types'

interface Props {
  title: string
  subtitle?: string
  services: Service[]
  variant?: '1' | '2'
  showAllLink?: boolean
  allServicesLink?: string
  bgSection?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: '2',
  showAllLink: true,
  allServicesLink: '/divisions',
  bgSection: false
})

const sectionClasses = computed(() => {
  const classes = ['service-section', 'fix', 'section-padding']
  if (props.bgSection) classes.push('section-bg')
  return classes.join(' ')
})

const columnClass = computed(() => {
  return props.variant === '1' ? 'col-xl-3 col-lg-4 col-md-6' : 'col-xl-4 col-lg-6 col-md-6'
})
</script>

<style scoped>
/* Service section styles are handled by the main template CSS */
</style>
