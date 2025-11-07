<template>
  <div class="body-bg">
    <!-- Custom Mouse Cursor -->
    <MouseCursor />

    <!-- Back to Top Button -->
    <BackToTop />

    <!-- Main Header -->
    <AppHeader @open-search="openSearchModal" />

    <!-- Search Modal -->
    <SearchModal ref="searchRef" />

    <!-- Main Content -->
    <main>
      <slot />
    </main>

    <!-- Footer -->
    <AppFooter :variant="footerVariant" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  footerVariant?: 'default' | 'style-2'
}

const props = withDefaults(defineProps<Props>(), {
  footerVariant: 'default'
})

// Ref for search modal
const searchRef = ref<InstanceType<typeof SearchModal> | null>(null)

// Methods to control search modal
const openSearchModal = () => {
  searchRef.value?.openSearch()
}
</script>

<style scoped>
.body-bg {
  position: relative;
  min-height: 100vh;
  background-image: url('~/assets/space-background.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  background-repeat: no-repeat;
}

.body-bg::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(20, 20, 20, 0.85);
  pointer-events: none;
  z-index: 0;
}

.body-bg > * {
  position: relative;
  z-index: 1;
}
</style>
