<template>
  <header class="container" style="padding: 1rem 0;">
    <nav aria-label="Main navigation">
      <ul class="nav">
        <li v-for="item in nav" :key="item.to">
          <NuxtLink :to="item.to">{{ item.label }}</NuxtLink>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script setup lang="ts">
const nav = useNavigation() // auto-imported composable
</script>

<style scoped>
.container { max-width: 1040px; margin: 0 auto; }
.nav { display: flex; gap: 1rem; list-style: none; padding: 0; margin: 0; }
</style>
