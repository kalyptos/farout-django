<template>
  <div class="search-wrap" :class="{ active: isOpen }">
    <div class="search-inner">
      <i
        class="fas fa-times search-close"
        id="search-close"
        @click="closeSearch"
      ></i>
      <div class="search-cell">
        <form @submit.prevent="handleSearch">
          <div class="search-field-holder">
            <input
              v-model="searchQuery"
              type="search"
              class="main-search-input"
              placeholder="Search..."
              autofocus
            />
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const isOpen = ref(false)
const searchQuery = ref('')

const openSearch = () => {
  isOpen.value = true
  document.body.classList.add('search-open')
}

const closeSearch = () => {
  isOpen.value = false
  document.body.classList.remove('search-open')
  searchQuery.value = ''
}

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    // TODO: Implement search functionality
    // Could navigate to /search?q=query or trigger search API
    // navigateTo(`/search?q=${encodeURIComponent(searchQuery.value)}`)
  }
}

// Watch for Escape key
watch(isOpen, (newVal) => {
  if (newVal) {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        closeSearch()
      }
    }
    document.addEventListener('keydown', handleEscape)
    return () => document.removeEventListener('keydown', handleEscape)
  }
})

// Expose methods for parent components
defineExpose({
  openSearch,
  closeSearch
})
</script>

<style scoped>
/* Search modal styles are handled by the main template CSS */
</style>
