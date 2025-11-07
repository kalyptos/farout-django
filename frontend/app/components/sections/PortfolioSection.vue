<template>
  <section class="portfolio-section fix section-bg section-padding">
    <div v-if="variant === 'slider'" class="container">
      <div class="section-title-area">
        <SectionTitle :subtitle="subtitle" :title="title" />
        <BaseButton
          v-if="showAllLink"
          :to="allWorksLink"
          variant="theme-btn"
          data-animation="fade-in-up"
        >
          See All Works
        </BaseButton>
      </div>
    </div>

    <div v-if="variant === 'slider'">
      <Swiper
        :modules="[Navigation, Pagination, Autoplay]"
        :slides-per-view="3"
        :space-between="30"
        :loop="true"
        :pagination="{ clickable: true }"
        :autoplay="{ delay: 2500, disableOnInteraction: false }"
        :navigation="true"
      >
        <SwiperSlide v-for="project in projects" :key="project.id">
          <PortfolioCard
            :title="project.title"
            :category="project.category"
            :image="project.image"
            :link="`/divisions/${project.slug}`"
            variant="slider"
          />
        </SwiperSlide>
      </Swiper>
    </div>

    <div v-else class="container">
      <div class="section-title-area">
        <SectionTitle :subtitle="subtitle" :title="title" />
        <BaseButton
          v-if="showAllLink"
          :to="allWorksLink"
          variant="theme-btn"
        >
          See All Works
        </BaseButton>
      </div>
      <div class="row">
        <div class="col-lg-12">
                    <AnimatedElement
            v-for="project in projects"
            :key="project.id"
            animation="fade-in-up"
            :delay="'.3s'"
          >
            <PortfolioCard
              :title="project.title"
              :category="project.category"
              :description="project.description"
              :hover-image="project.hoverImage"
              :link="`/divisions/${project.slug}`"
              variant="box"
            />
          </AnimatedElement>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Project } from '~/types'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation, Pagination, Autoplay } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

interface Props {
  title: string
  subtitle?: string
  projects: Project[]
  variant?: 'slider' | 'box'
  showAllLink?: boolean
  allWorksLink?: string
}

withDefaults(defineProps<Props>(), {
  variant: 'slider',
  showAllLink: true,
  allWorksLink: '/divisions'
})
</script>

<style scoped>
/* Portfolio section styles are handled by the main template CSS */
</style>
