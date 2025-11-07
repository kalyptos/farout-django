<template>
  <div class="user-dashboard">
    <div class="dashboard-container">
      <!-- Page Header -->
      <div class="dashboard-header">
        <h1>Personal Dashboard</h1>
        <p class="subtitle">Welcome back, {{ profile?.username || 'Member' }}</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <i class="fa-solid fa-spinner fa-spin"></i>
        <p>Loading your profile...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error-state">
        <div class="error-card">
          <i class="fa-solid fa-exclamation-circle"></i>
          <h3>Failed to Load Profile</h3>
          <p>{{ error }}</p>
          <button @click="fetchProfile" class="retry-button">
            <i class="fa-solid fa-rotate-right"></i>
            Retry
          </button>
        </div>
      </div>

      <!-- Dashboard Content -->
      <div v-else-if="profile" class="dashboard-grid">
        <!-- Profile Card -->
        <div class="card profile-card">
          <div class="card-content">
            <div class="avatar-section">
              <img
                :src="profile.member_data?.avatar_url || 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDEyMCAxMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjEyMCIgaGVpZ2h0PSIxMjAiIGZpbGw9IiMxYTFhMWEiLz48Y2lyY2xlIGN4PSI2MCIgY3k9IjQ1IiByPSIyMCIgZmlsbD0iIzAwN2JmZiIvPjxwYXRoIGQ9Ik0gMzAgOTUgUSA2MCA3NSA5MCA5NSIgZmlsbD0iIzAwN2JmZiIvPjwvc3ZnPg=='"
                :alt="profile.username"
                class="avatar"
                @error="handleImageError"
              />
            </div>
            <div class="profile-info">
              <h2>{{ profile.username }}</h2>
              <p class="email">{{ profile.email }}</p>
              <span :class="['role-badge', profile.role]">
                <i :class="profile.role === 'admin' ? 'fa-solid fa-shield-halved' : 'fa-solid fa-user'"></i>
                {{ profile.role.toUpperCase() }}
              </span>
              <p class="member-since">
                <i class="fa-solid fa-calendar-days"></i>
                Member since {{ formatDate(profile.created_at) }}
              </p>
              <p v-if="profile.last_login" class="last-login">
                <i class="fa-solid fa-clock"></i>
                Last login: {{ formatDateTime(profile.last_login) }}
              </p>
            </div>
          </div>
        </div>

        <!-- Rank Card -->
        <div class="card rank-card">
          <div class="card-header">
            <h3>
              <i class="fa-solid fa-medal"></i>
              Rank
            </h3>
          </div>
          <div class="card-content">
            <div v-if="profile.rank_image" class="rank-image-container">
              <img :src="profile.rank_image" alt="Rank Badge" class="rank-image" />
            </div>
            <div class="rank-badge-large">{{ profile.rank || 'Member' }}</div>
          </div>
        </div>

        <!-- Stats Card (if member_data exists) -->
        <div v-if="profile.member_data" class="card stats-card">
          <div class="card-header">
            <h3>
              <i class="fa-solid fa-chart-line"></i>
              Statistics
            </h3>
          </div>
          <div class="card-content">
            <div class="stat-item">
              <div class="stat-icon missions">
                <i class="fa-solid fa-rocket"></i>
              </div>
              <div class="stat-details">
                <div class="stat-label">Missions Completed</div>
                <div class="stat-value">{{ profile.member_data.missions_completed?.length || 0 }}</div>
              </div>
            </div>
            <div class="stat-item">
              <div class="stat-icon trainings">
                <i class="fa-solid fa-graduation-cap"></i>
              </div>
              <div class="stat-details">
                <div class="stat-label">Trainings Completed</div>
                <div class="stat-value">{{ profile.member_data.trainings_completed?.length || 0 }}</div>
              </div>
            </div>
            <div v-if="profile.member_data.member_since" class="stat-item">
              <div class="stat-icon member-since">
                <i class="fa-solid fa-flag"></i>
              </div>
              <div class="stat-details">
                <div class="stat-label">Member Since</div>
                <div class="stat-value">{{ formatDate(profile.member_data.member_since) }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Bio Card (if bio exists) -->
        <div v-if="profile.member_data?.bio" class="card bio-card">
          <div class="card-header">
            <h3>
              <i class="fa-solid fa-user-astronaut"></i>
              Bio
            </h3>
          </div>
          <div class="card-content">
            <p class="bio-text">{{ profile.member_data.bio }}</p>
          </div>
        </div>

        <!-- Quick Actions Card -->
        <div class="card actions-card">
          <div class="card-header">
            <h3>
              <i class="fa-solid fa-bolt"></i>
              Quick Actions
            </h3>
          </div>
          <div class="card-content">
            <NuxtLink to="/change-password" class="action-link">
              <i class="fa-solid fa-key"></i>
              Change Password
            </NuxtLink>
            <NuxtLink to="/members" class="action-link">
              <i class="fa-solid fa-users"></i>
              View Organization Members
            </NuxtLink>
            <NuxtLink v-if="profile.role === 'admin'" to="/admin" class="action-link admin">
              <i class="fa-solid fa-shield-halved"></i>
              Admin Panel
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
  middleware: 'auth'
})

useHead({
  title: 'My Dashboard - FarOut Organization',
  meta: [
    {
      name: 'description',
      content: 'Your personal dashboard for FarOut organization.'
    }
  ]
})

const { profile, loading, error, fetchProfile } = useUserProfile()

onMounted(() => {
  fetchProfile()
})

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
}

const formatDateTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const handleImageError = (event: Event) => {
  const target = event.target as HTMLImageElement
  // Use a base64 encoded default avatar SVG
  target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDEyMCAxMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjEyMCIgaGVpZ2h0PSIxMjAiIGZpbGw9IiMxYTFhMWEiLz48Y2lyY2xlIGN4PSI2MCIgY3k9IjQ1IiByPSIyMCIgZmlsbD0iIzAwN2JmZiIvPjxwYXRoIGQ9Ik0gMzAgOTUgUSA2MCA3NSA5MCA5NSIgZmlsbD0iIzAwN2JmZiIvPjwvc3ZnPg=='
}
</script>

<style scoped lang="scss">
.user-dashboard {
  min-height: 100vh;
  background: $background-primary;
  padding: 2rem 1rem;
}

.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 3rem;
  padding-top: 2rem;

  h1 {
    color: $text-primary;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
  }

  .subtitle {
    color: $text-secondary;
    font-size: 1.125rem;
  }
}

// Loading State
.loading-state {
  text-align: center;
  padding: 4rem 2rem;
  color: $text-secondary;

  i {
    font-size: 3rem;
    color: $color-primary;
    margin-bottom: 1rem;
  }

  p {
    font-size: 1.125rem;
  }
}

// Error State
.error-state {
  display: flex;
  justify-content: center;
  padding: 2rem;
}

.error-card {
  background: $background-card;
  border: 1px solid $border-color;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  max-width: 500px;

  i {
    font-size: 3rem;
    color: $error;
    margin-bottom: 1rem;
  }

  h3 {
    color: $text-primary;
    margin-bottom: 0.5rem;
  }

  p {
    color: $text-secondary;
    margin-bottom: 1.5rem;
  }

  .retry-button {
    background: $button-primary-bg;
    color: $button-primary-text;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    transition: background $transition-base;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;

    &:hover {
      background: $button-primary-hover;
    }

    i {
      font-size: 1rem;
      color: inherit;
      margin: 0;
    }
  }
}

// Dashboard Grid
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

// Card Base Styles
.card {
  background: $background-card;
  border: 1px solid $border-color;
  border-radius: 12px;
  box-shadow: 0 4px 12px $shadow-color;
  overflow: hidden;
  transition: transform $transition-base, box-shadow $transition-base;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px $shadow-dark;
  }

  .card-header {
    padding: 1.5rem;
    border-bottom: 1px solid $border-color;

    h3 {
      color: $text-primary;
      font-size: 1.25rem;
      font-weight: 600;
      margin: 0;
      display: flex;
      align-items: center;
      gap: 0.5rem;

      i {
        color: $color-primary;
      }
    }
  }

  .card-content {
    padding: 1.5rem;
  }
}

// Profile Card
.profile-card {
  grid-column: span 2;

  .card-content {
    display: flex;
    gap: 2rem;
    align-items: center;
  }

  .avatar-section {
    flex-shrink: 0;
  }

  .avatar {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 4px solid $color-primary;
    object-fit: cover;
    box-shadow: 0 4px 12px $shadow-dark;
  }

  .profile-info {
    flex: 1;

    h2 {
      color: $text-primary;
      font-size: 1.875rem;
      margin-bottom: 0.5rem;
      font-weight: 700;
    }

    .email {
      color: $text-secondary;
      font-size: 1rem;
      margin-bottom: 1rem;
    }

    .role-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.375rem 1rem;
      border-radius: 24px;
      font-size: 0.875rem;
      font-weight: 700;
      letter-spacing: 0.5px;
      margin-bottom: 1rem;

      &.admin {
        background: $success;
        color: white;
      }

      &.member {
        background: $color-primary;
        color: white;
      }
    }

    .member-since,
    .last-login {
      color: $text-muted;
      font-size: 0.875rem;
      margin-top: 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;

      i {
        color: $color-primary;
      }
    }
  }
}

// Rank Card
.rank-card {
  .rank-image-container {
    text-align: center;
    margin-bottom: 1rem;

    .rank-image {
      max-width: 100px;
      max-height: 100px;
      object-fit: contain;
    }
  }

  .rank-badge-large {
    text-align: center;
    font-size: 1.5rem;
    font-weight: 700;
    color: $color-secondary;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
}

// Stats Card
.stats-card {
  .card-content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .stat-item {
    display: flex;
    align-items: center;
    gap: 1rem;

    .stat-icon {
      width: 48px;
      height: 48px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.25rem;
      flex-shrink: 0;

      &.missions {
        background: rgba($color-primary, 0.2);
        color: $color-primary;
      }

      &.trainings {
        background: rgba($color-secondary, 0.2);
        color: $color-secondary;
      }

      &.member-since {
        background: rgba($color-accent, 0.2);
        color: $color-accent;
      }
    }

    .stat-details {
      flex: 1;

      .stat-label {
        color: $text-muted;
        font-size: 0.875rem;
        margin-bottom: 0.25rem;
      }

      .stat-value {
        color: $text-primary;
        font-size: 1.5rem;
        font-weight: 700;
      }
    }
  }
}

// Bio Card
.bio-card {
  grid-column: span 2;

  .bio-text {
    color: $text-secondary;
    line-height: 1.75;
    font-size: 1rem;
  }
}

// Actions Card
.actions-card {
  .card-content {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .action-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    background: $background-secondary;
    border: 1px solid $border-color;
    border-radius: 8px;
    color: $text-primary;
    text-decoration: none;
    transition: all $transition-base;

    i {
      color: $color-primary;
      font-size: 1.25rem;
      width: 24px;
      text-align: center;
    }

    &:hover {
      background: $background-light;
      border-color: $color-primary;
      transform: translateX(4px);
    }

    &.admin {
      i {
        color: $success;
      }

      &:hover {
        border-color: $success;
      }
    }
  }
}

// Responsive Design
@include md {
  .user-dashboard {
    padding: 3rem 2rem;
  }

  .dashboard-header {
    h1 {
      font-size: 3rem;
    }
  }

  .dashboard-grid {
    gap: 2rem;
  }
}

@include lg {
  .dashboard-grid {
    grid-template-columns: repeat(3, 1fr);

    .profile-card {
      grid-column: span 3;
    }

    .bio-card {
      grid-column: span 3;
    }
  }
}

// Mobile Optimization
@media (max-width: $breakpoint-md) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .profile-card {
    .card-content {
      flex-direction: column;
      text-align: center;
    }

    .profile-info {
      .member-since,
      .last-login {
        justify-content: center;
      }
    }
  }

  .dashboard-header {
    h1 {
      font-size: 2rem;
    }

    .subtitle {
      font-size: 1rem;
    }
  }
}
</style>
