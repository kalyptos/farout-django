<template>
  <header id="header-sticky" class="header-1">
    <div class="container">
      <div class="mega-menu-wrapper">
        <div class="header-main">
          <!-- Logo -->
          <div class="logo">
            <NuxtLink to="/" class="header-logo">
              <NuxtImg src="/assets/img/logo/white-logo.svg" alt="logo" />
            </NuxtLink>
          </div>

          <!-- Desktop Navigation -->
          <div class="mean__menu-wrapper">
            <div class="main-menu">
              <nav id="mobile-menu">
                <ul>
                  <li
                    v-for="item in navigation"
                    :key="item.path"
                    :class="{ active: item.active }"
                  >
                    <NuxtLink :to="item.path">
                      {{ item.label }}
                    </NuxtLink>
                  </li>
                </ul>
              </nav>
            </div>
          </div>

          <!-- Header Right Actions -->
          <div class="header-right d-flex justify-content-end align-items-center">
            <div class="header-button">
              <!-- Auth Section -->
              <template v-if="isAuthenticated">
                <!-- User Info (Clickable) -->
                <NuxtLink
                  :to="isAdmin ? '/admin' : '/user'"
                  class="user-info"
                >
                  <span class="username">{{ user?.username }}</span>
                  <span v-if="isAdmin" class="admin-badge">ADMIN</span>
                  <span v-else class="member-badge">MEMBER</span>
                </NuxtLink>

                <!-- Logout Button -->
                <button @click="handleLogout" class="theme-btn theme-btn-secondary">
                  <i class="fa-solid fa-right-from-bracket"></i>
                  Logout
                </button>
              </template>
              <template v-else>
                <!-- Login Button -->
                <NuxtLink to="/login" class="theme-btn">Login</NuxtLink>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { mainNavigation, getNavigationWithActive } from '~/data/navigation'

// Get current route
const route = useRoute()

// Get navigation with active states
const navigation = computed(() => {
  return getNavigationWithActive(route.path)
})

// Auth composable
const { user, isAuthenticated, isAdmin, logout, initAuth } = useAuth()

// Initialize auth on mount
onMounted(async () => {
  await initAuth()
})

// Handle logout
const handleLogout = async () => {
  await logout()
}
</script>

<style scoped lang="scss">
/* Header styles are handled by the main template CSS */
/* Custom adjustments if needed */

.header-button {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-button .theme-btn {
  margin-left: auto;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(17, 171, 233, 0.1);
  border-radius: 20px;
  border: 1px solid rgba(17, 171, 233, 0.3);
  text-decoration: none;
  transition: all 0.3s ease;

  &:hover {
    background: rgba(17, 171, 233, 0.2);
    border-color: rgba(17, 171, 233, 0.5);
    cursor: pointer;
    transform: translateY(-1px);
  }

  .username {
    color: var(--text-primary);
    font-weight: 500;
    font-size: 0.9rem;
  }

  .admin-badge {
    background: #ffc107;
    color: #000;
    padding: 0.2rem 0.6rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
  }

  .member-badge {
    background: #17a2b8;
    color: #fff;
    padding: 0.2rem 0.6rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
  }
}

.nav-link-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  color: var(--text-primary);
  text-decoration: none;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.3s ease;

  i {
    color: var(--color-accent-1);
  }

  &:hover {
    background: rgba(17, 171, 233, 0.1);
    color: var(--color-accent-1);
  }
}

.theme-btn-secondary {
  background: rgba(220, 53, 69, 0.9);

  &:hover {
    background: rgba(220, 53, 69, 1);
  }

  i {
    margin-right: 0.25rem;
  }
}
</style>
