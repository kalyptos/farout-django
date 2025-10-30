<template>
  <footer class="container" style="padding: 2rem 0; opacity:.7;">
    <p>© {{ year }} Farout Corporation</p>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
</script>

<style scoped>
.container { max-width: 1040px; margin: 0 auto; }
</style>
