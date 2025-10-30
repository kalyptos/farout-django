// frontend/nuxt.config.ts
export default defineNuxtConfig({
  ssr: true,
  nitro: { preset: 'node' },
  css: ['assets/styles/main.scss'],
})