<template>
  <div class="testimonial-card-items">
    <div class="testi-top">
      <div class="star">
        <i
          v-for="star in 5"
          :key="star"
          :class="getStarClass(star)"
        ></i>
      </div>
      <div class="quote-icon">
        <NuxtImg src="/assets/img/testimonial/quote.png" alt="quote" />
      </div>
    </div>
    <p>{{ content }}</p>
    <div class="client-info">
      <div class="client-img">
        <NuxtImg :src="clientImage" :alt="clientName" />
      </div>
      <div class="content">
        <h5>{{ clientName }}</h5>
        <span>{{ clientRole }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  content: string
  clientName: string
  clientRole: string
  clientImage: string
  rating: number // e.g., 4.5
}

const props = defineProps<Props>()

const getStarClass = (position: number): string => {
  const fullStars = Math.floor(props.rating)
  const hasHalfStar = props.rating % 1 !== 0

  if (position <= fullStars) {
    return 'fa-solid fa-star'
  } else if (position === fullStars + 1 && hasHalfStar) {
    return 'fa-solid fa-star-half-stroke'
  } else {
    return 'fa-regular fa-star'
  }
}
</script>

<style scoped>
/* Testimonial card styles are handled by the main template CSS */
</style>
