<template>
  <div class="brand-section section-padding fix pt-0" :class="{ 'section-bg': bgSection }">
    <div class="container">
      <div class="brand-text">
        <h5 :class="{ 'text-white': bgSection }">{{ heading }}</h5>
      </div>
      <Swiper
        :modules="[Autoplay]"
        :slides-per-view="5"
        :space-between="30"
        :loop="true"
        :autoplay="{ delay: 2500, disableOnInteraction: false }"
      >
        <SwiperSlide v-for="brand in brands" :key="brand.id">
          <BrandItem
            :name="brand.name"
            :logo="brand.logo"
            :url="brand.url"
          />
        </SwiperSlide>
      </Swiper>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Brand } from '~/types'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay } from 'swiper/modules'
import 'swiper/css'

interface Props {
  heading: string
  brands: Brand[]
  bgSection?: boolean
}

withDefaults(defineProps<Props>(), {
  bgSection: false
})
</script>

<style scoped>
/* Brand slider styles are handled by the main template CSS */
</style>
