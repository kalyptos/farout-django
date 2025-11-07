import { ref, onMounted, onUnmounted, type Ref } from 'vue'

export function useCountUp(target: Ref<HTMLElement | null>, endVal: number, duration = 2000) {
  const count = ref(0)
  const observer = ref<IntersectionObserver | null>(null)
  let animationFrameId: number | null = null

  const animateCount = () => {
    let startTime: number | null = null
    const step = (timestamp: number) => {
      if (!startTime) startTime = timestamp
      const progress = Math.min((timestamp - startTime) / duration, 1)
      count.value = Math.floor(progress * endVal)
      if (progress < 1) {
        animationFrameId = window.requestAnimationFrame(step)
      } else {
        animationFrameId = null
      }
    }
    animationFrameId = window.requestAnimationFrame(step)
  }

  onMounted(() => {
    observer.value = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          animateCount()
          observer.value?.disconnect()
        }
      },
      { threshold: 0.5 }
    )

    if (target.value) {
      observer.value.observe(target.value)
    }
  })

  onUnmounted(() => {
    // Cancel any pending animation frame
    if (animationFrameId !== null) {
      window.cancelAnimationFrame(animationFrameId)
      animationFrameId = null
    }
    // Cleanup observer
    observer.value?.disconnect()
    observer.value = null
  })

  return {
    count
  }
}
