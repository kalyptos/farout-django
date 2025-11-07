<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
import { useAnimateOnScroll } from '~/composables/useAnimateOnScroll'

useAnimateOnScroll()
</script>
