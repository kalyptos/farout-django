<template>
  <div>
    <!-- Page Header -->
    <PageHeader
      title="Our Divisions"
      subtitle="Specialized Units"
      :breadcrumbs="breadcrumbs"
    />

    <!-- Divisions Grid Section -->
    <section class="divisions-section section-padding">
      <div class="container">
        <AnimatedElement animation="fade-in-up" :delay="'.3s'">
          <SectionTitle
            title="Division Overview"
            subtitle="Specialized Operations"
            centered
          />
        </AnimatedElement>

        <div class="row g-4 mt-5">
          <AnimatedElement
            v-for="(division, index) in divisions"
            :key="division.id"
            animation="fade-in-up"
            :delay="`${0.2 + index * 0.1}s`"
            class="col-lg-4 col-md-6"
          >
            <PortfolioCard
              :title="division.name"
              :category="division.category"
              :description="division.description"
              :image="division.image"
              :hoverImage="division.hoverImage"
              :slug="`/divisions/${division.slug}`"
            />
          </AnimatedElement>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <LetsTalkSection />
  </div>
</template>

<script setup lang="ts">
import { divisions } from '~/data/divisions'

useHead({
  title: 'Divisions - FarOut Organization',
  meta: [
    {
      name: 'description',
      content: 'Explore our specialized divisions, from combat operations to exploration and trading.'
    }
  ]
})

const breadcrumbs = [
  { label: 'Home', path: '/' },
  { label: 'Divisions' }
]
</script>

<style scoped lang="scss">
.divisions-section {
  padding: 100px 0;
}
</style>
