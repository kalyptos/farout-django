import { onMounted, onUnmounted, ref } from 'vue'

export function useAnimateOnScroll() {
  const observer = ref<IntersectionObserver | null>(null)
  const observedElements = ref<Element[]>([])

  const animate = (element: HTMLElement) => {
    const animation = element.dataset.animation || 'fade-in-up'
    element.classList.add(animation, 'visible')
  }

  onMounted(() => {
    observer.value = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animate(entry.target as HTMLElement)
            observer.value?.unobserve(entry.target)
            // Remove from tracked elements
            const index = observedElements.value.indexOf(entry.target)
            if (index > -1) {
              observedElements.value.splice(index, 1)
            }
          }
        })
      },
      { threshold: 0.1 }
    )

    const elements = document.querySelectorAll('[data-animation]')
    elements.forEach((element) => {
      observer.value?.observe(element)
      observedElements.value.push(element)
    })
  })

  onUnmounted(() => {
    // Unobserve all tracked elements before disconnecting
    observedElements.value.forEach((element) => {
      observer.value?.unobserve(element)
    })
    observer.value?.disconnect()
    observer.value = null
    observedElements.value = []
  })
}
