<template>
  <div>
    <div ref="cursorOuter" class="mouse-cursor cursor-outer"></div>
    <div ref="cursorInner" class="mouse-cursor cursor-inner"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const cursorOuter = ref<HTMLElement | null>(null)
const cursorInner = ref<HTMLElement | null>(null)

let mouseX = 0
let mouseY = 0
let outerX = 0
let outerY = 0
let innerX = 0
let innerY = 0

const updateCursor = () => {
  // Smooth follow effect for outer cursor
  outerX += (mouseX - outerX) * 0.1
  outerY += (mouseY - outerY) * 0.1

  // Faster follow for inner cursor
  innerX += (mouseX - innerX) * 0.3
  innerY += (mouseY - innerY) * 0.3

  if (cursorOuter.value) {
    cursorOuter.value.style.transform = `translate(${outerX}px, ${outerY}px)`
  }
  if (cursorInner.value) {
    cursorInner.value.style.transform = `translate(${innerX}px, ${innerY}px)`
  }

  requestAnimationFrame(updateCursor)
}

const handleMouseMove = (e: MouseEvent) => {
  mouseX = e.clientX
  mouseY = e.clientY
}

onMounted(() => {
  // Only enable custom cursor on desktop
  if (window.innerWidth > 768) {
    document.addEventListener('mousemove', handleMouseMove)
    requestAnimationFrame(updateCursor)
  }
})

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove)
})
</script>

<style scoped>
/* Cursor styles are handled by the main template CSS */
</style>
