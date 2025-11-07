<template>
  <section class="team-section fix section-padding" :class="{ 'section-bg': bgSection }">
    <div class="container">
      <SectionTitle :subtitle="subtitle" :title="title" alignment="center" />
      <div class="row">
                <AnimatedElement
          v-for="(member, index) in team"
          :key="member.id"
          :class="columnClass"
          animation="fade-in-up"
          :delay="`${0.2 + index * 0.2}s`"
        >
          <TeamCard
            :name="member.name"
            :role="member.role"
            :image="member.image"
            :details-link="`/members/${member.id}`"
            :social-links="member.socialLinks"
            :variant="cardVariant"
            :active="index === 1"
          />
        </AnimatedElement>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { TeamMember } from '~/types'

interface Props {
  title: string
  subtitle?: string
  team: TeamMember[]
  bgSection?: boolean
  cardVariant?: 'box' | 'card'
  columns?: 3 | 4
}

const props = withDefaults(defineProps<Props>(), {
  bgSection: false,
  cardVariant: 'card',
  columns: 3
})

const columnClass = computed(() => {
  return props.columns === 3
    ? 'col-xl-4 col-lg-6 col-md-6'
    : 'col-xl-3 col-lg-4 col-md-6'
})
</script>

<style scoped>
/* Team section styles are handled by the main template CSS */
</style>
