<template>
  <component
    :is="componentType"
    :to="to"
    :href="href"
    :class="buttonClasses"
    :type="type"
    @click="handleClick"
  >
    <i v-if="icon && iconPosition === 'left'" :class="icon"></i>
    <slot />
    <i v-if="icon && iconPosition === 'right'" :class="icon"></i>
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'theme-btn' | 'radius-btn' | 'link-btn' | 'arrow-icon'
  to?: string
  href?: string
  type?: 'button' | 'submit' | 'reset'
  icon?: string
  iconPosition?: 'left' | 'right'
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'theme-btn',
  type: 'button',
  iconPosition: 'right',
  disabled: false
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

// Determine component type based on props
const componentType = computed(() => {
  if (props.to) return 'NuxtLink'
  if (props.href) return 'a'
  return 'button'
})

// Build CSS classes
const buttonClasses = computed(() => {
  const classes = [props.variant]
  if (props.disabled) classes.push('disabled')
  return classes.join(' ')
})

const handleClick = (event: MouseEvent) => {
  if (!props.disabled) {
    emit('click', event)
  }
}
</script>

<style scoped>
/* Button styles are handled by the main template CSS */
/* Additional custom styles can be added here if needed */
</style>
