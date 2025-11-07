<template>
  <section class="testimonial-section fix section-padding" :class="{ 'section-bg': bgSection }">
    <div class="container">
      <div class="tesimonial-wrapper-2">
        <div class="row g-4">
          <div class="col-lg-5">
            <div class="testimonial-image">
              <NuxtImg :src="sideImage" alt="testimonial" />
            </div>
          </div>
          <div class="col-lg-5">
            <div class="testimonial-content">
              <SectionTitle :subtitle="subtitle" :title="title" />
              <p data-animation="fade-in-up">
                {{ description }}
              </p>
            </div>
          </div>
        </div>
        <Swiper
          :modules="[Pagination]"
          :slides-per-view="1"
          :space-between="30"
          :loop="true"
          :pagination="{ clickable: true, el: '.swiper-dot .dot' }"
        >
          <SwiperSlide v-for="testimonial in testimonials" :key="testimonial.id">
            <TestimonialCard
              :content="testimonial.content"
              :client-name="testimonial.clientName"
              :client-role="testimonial.clientRole"
              :client-image="testimonial.clientImage"
              :rating="testimonial.rating"
            />
          </SwiperSlide>
        </Swiper>
        <div class="swiper-dot pt-5">
          <div class="dot"></div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Testimonial } from '~/types'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Pagination } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'

interface Props {
  title: string
  subtitle?: string
  description: string
  sideImage: string
  testimonials: Testimonial[]
  bgSection?: boolean
}

withDefaults(defineProps<Props>(), {
  bgSection: false
})
</script>

<style scoped>
/* Testimonial section styles are handled by the main template CSS */
</style>
