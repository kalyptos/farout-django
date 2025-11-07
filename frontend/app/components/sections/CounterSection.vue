<template>
  <section class="counter-section section-bg section-padding">
    <div class="container">
      <div class="row">
                <AnimatedElement
          v-for="(stat, index) in stats"
          :key="index"
          :class="columnClass"
          animation="fade-in-up"
          :delay="`${0.2 + index * 0.2}s`"
        >
          <CounterItem
            :value="stat.value"
            :unit="stat.unit"
            :label="stat.label"
            :variant="index % 2 === 0 ? 'style-2' : 'default'"
          />
        </AnimatedElement>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Stat } from '~/types'

interface Props {
  stats: Stat[]
  columns?: 3 | 4
}

const props = withDefaults(defineProps<Props>(), {
  columns: 4
})

const columnClass = computed(() => {
  return props.columns === 3
    ? 'col-xl-4 col-lg-4 col-md-6'
    : 'col-xl-3 col-lg-4 col-md-6'
})
</script>

<style scoped>
/* Counter section styles are handled by the main template CSS */
</style>
