<template>
  <Transition name="mobile-menu">
    <div v-if="isOpen" class="mobile-menu-overlay" @click="$emit('close')">
      <div class="mobile-menu-content" @click.stop>
        <div class="mobile-menu-header">
          <h3>Menu</h3>
          <button class="close-btn" @click="$emit('close')" aria-label="Close menu">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <nav class="mobile-menu-nav">
          <ul>
            <li v-for="item in menuItems" :key="item.to">
              <NuxtLink :to="item.to" @click="$emit('close')">
                {{ item.label }}
              </NuxtLink>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import type { MenuItem } from '~/types/navigation'

interface Props {
  isOpen: boolean
  menuItems: MenuItem[]
}

defineProps<Props>()
defineEmits<{
  close: []
}>()
</script>

<style scoped lang="scss">
.mobile-menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: $background-overlay;
  z-index: 9999;
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  backdrop-filter: blur(5px);
}

.mobile-menu-content {
  background: $bg-primary;
  width: 100%;
  max-width: 300px;
  height: 100%;
  box-shadow: -5px 0 20px $shadow-color;
  border-left: 2px solid rgba($color-primary, 0.3);
  display: flex;
  flex-direction: column;
}

.mobile-menu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-xl;
  border-bottom: 1px solid rgba($color-primary, 0.2);

  h3 {
    color: $color-primary;
    margin: 0;
    font-size: $text-xl;
    font-weight: $font-semibold;
  }

  .close-btn {
    background: transparent;
    border: none;
    color: $text-primary;
    font-size: $text-xl;
    cursor: pointer;
    padding: $spacing-sm;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: $radius-sm;

    &:hover {
      background: rgba($color-primary, 0.1);
      color: $color-primary;
    }
  }
}

.mobile-menu-nav {
  flex: 1;
  overflow-y: auto;
  padding: $spacing-md 0;

  ul {
    list-style: none;
    padding: 0;
    margin: 0;

    li {
      a {
        display: block;
        padding: $spacing-md $spacing-xl;
        color: $text-primary;
        text-decoration: none;
        font-weight: $font-medium;
        font-size: $text-base;
        transition: all 0.3s ease;
        border-left: 3px solid transparent;

        &:hover,
        &.router-link-active {
          color: $color-primary;
          background: rgba($color-primary, 0.1);
          border-left-color: $color-primary;
        }
      }
    }
  }
}

// Transition animations
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: opacity 0.3s ease;

  .mobile-menu-content {
    transition: transform 0.3s ease;
  }
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;

  .mobile-menu-content {
    transform: translateX(100%);
  }
}

.mobile-menu-enter-to,
.mobile-menu-leave-from {
  opacity: 1;

  .mobile-menu-content {
    transform: translateX(0);
  }
}
</style>
