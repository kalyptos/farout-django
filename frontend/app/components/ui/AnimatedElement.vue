<template>
  <component
    :is="tag"
    :data-animation="animation"
    :style="delay ? { transitionDelay: delay } : {}"
  >
    <slot />
  </component>
</template>

<script setup lang="ts">
import { useAnimateOnScroll } from '~/composables/useAnimateOnScroll'

interface Props {
  animation?: string
  tag?: string
  delay?: string
}

withDefaults(defineProps<Props>(), {
  animation: 'fade-in-up',
  tag: 'div',
  delay: undefined
})

useAnimateOnScroll()
</script>

<style scoped>
[data-animation] {
  opacity: 0;
  transition: all 0.5s ease-out;
}

.fade-in-up {
  transform: translateY(20px);
}

.visible {
  opacity: 1;
  transform: translateY(0);
}
</style>
