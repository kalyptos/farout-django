import { ref, onMounted, onUnmounted } from 'vue'

export function useStickyHeader(scrollThreshold = 100) {
  const isSticky = ref(false)

  const handleScroll = () => {
    isSticky.value = window.scrollY > scrollThreshold
  }

  onMounted(() => {
    window.addEventListener('scroll', handleScroll)
  })

  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
  })

  return {
    isSticky
  }
}
