<template>
  <div :class="itemClasses" ref="target">
    <h2>
      <span class="count">{{ count }}</span>{{ unit }}
    </h2>
    <p>{{ label }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useCountUp } from '~/composables/useCountUp'

interface Props {
  value: number
  unit?: string
  label: string
  variant?: 'default' | 'style-2'
  active?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  unit: '+',
  variant: 'default',
  active: false
})

const itemClasses = computed(() => {
  const classes = ['counter-items']
  if (props.variant === 'style-2') classes.push('style-2')
  if (props.active) classes.push('active')
  return classes.join(' ')
})

const target = ref(null)
const { count } = useCountUp(target, props.value)
</script>

<style scoped>
/* Counter item styles are handled by the main template CSS */
</style>
