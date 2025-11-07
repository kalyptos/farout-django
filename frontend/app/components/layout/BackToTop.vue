<template>
  <button
    v-show="isVisible"
    id="back-top"
    class="back-to-top"
    @click="scrollToTop"
    aria-label="Back to top"
  >
    <i class="fa-regular fa-arrow-up"></i>
  </button>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const isVisible = ref(false)

const handleScroll = () => {
  isVisible.value = window.scrollY > 300
}

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
/* Back to top styles are handled by the main template CSS */
</style>
