<template>
  <div class="brand-image text-center">
    <a v-if="url" :href="url" target="_blank" rel="noopener noreferrer">
      <NuxtImg :src="logo" :alt="name" />
    </a>
    <NuxtImg v-else :src="logo" :alt="name" />
  </div>
</template>

<script setup lang="ts">
interface Props {
  name: string
  logo: string
  url?: string
}

defineProps<Props>()
</script>

<style scoped>
/* Brand item styles are handled by the main template CSS */
</style>
