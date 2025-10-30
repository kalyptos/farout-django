<template>
  <section class="container" style="padding: 2rem 0;">
    <h1>Farout Nuxt + FastAPI</h1>
    <p>Backend health: <strong>{{ health?.status ?? '...' }}</strong></p>
    <button @click="addItem">Create demo item</button>
    <ul>
      <li v-for="it in items" :key="it.id">{{ it.title }}</li>
    </ul>
  </section>
</template>

<script setup lang="ts">
const api = useRuntimeConfig().public.apiBase
const { data: health } = await useFetch<{ status: string }>(`${api}/health`)
const { data: items, refresh } = await useFetch<Array<{ id:number; title:string }>>(`${api}/items`)
async function addItem() {
  await $fetch(`${api}/items`, { method: 'POST', body: { title: `Item ${Date.now()}` } })
  await refresh()
}
</script>
