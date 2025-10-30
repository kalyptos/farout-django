<template>
  <main class="container">
    <h1>Farout Nuxt + FastAPI</h1>
    <p>Backend health: <strong>{{ health?.status ?? '...' }}</strong></p>
    <button @click="addItem">Create demo item</button>
    <ul>
      <li v-for="it in items" :key="it.id">{{ it.title }}</li>
    </ul>
  </main>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()
const api = config.public.apiBase

const { data: health } = await useFetch(`${api}/health`)
const { data: items, refresh } = await useFetch(`${api}/items`)

async function addItem() {
  await $fetch(`${api}/items`, {
    method: 'POST',
    body: { title: `Item ${Date.now()}` }
  })
  await refresh()
}
</script>

<style scoped>
.container { max-width: 720px; margin: 3rem auto; }
</style>
