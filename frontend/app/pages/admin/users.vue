<template>
  <div>
    <!-- Page Header -->
    <PageHeader
      title="User Management"
      subtitle="Manage System Users and Permissions"
      :breadcrumbs="breadcrumbs"
    />

    <!-- Users Management Section -->
    <section class="users-section section-padding">
      <div class="container">
        <AnimatedElement animation="fade-in-up" :delay="'.3s'">
          <div class="users-card">
            <!-- Card Header with Controls -->
            <div class="card-header">
              <div class="header-top">
                <div class="header-info">
                  <h2>All Users</h2>
                  <p v-if="!loading">{{ total }} total users</p>
                </div>
              </div>

              <!-- Search and Filter Controls -->
              <div class="controls">
                <div class="search-box">
                  <i class="fa-solid fa-search"></i>
                  <input
                    v-model="search"
                    @input="handleSearch"
                    type="text"
                    placeholder="Search by username, email, or Discord ID..."
                    class="search-input"
                  />
                  <button
                    v-if="search"
                    @click="clearSearch"
                    class="clear-button"
                  >
                    <i class="fa-solid fa-times"></i>
                  </button>
                </div>

                <div class="filter-box">
                  <select v-model="roleFilter" @change="handleFilterChange" class="filter-select">
                    <option value="">All Roles</option>
                    <option value="admin">Admins Only</option>
                    <option value="member">Members Only</option>
                  </select>
                </div>

                <button v-if="search || roleFilter" @click="resetFilters" class="reset-button">
                  <i class="fa-solid fa-rotate-right"></i>
                  Reset
                </button>
              </div>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="loading-state">
              <i class="fa-solid fa-spinner fa-spin"></i>
              <p>Loading users...</p>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="error-state">
              <i class="fa-solid fa-exclamation-triangle"></i>
              <p>{{ error }}</p>
              <button @click="fetchUsers" class="retry-button">
                <i class="fa-solid fa-rotate-right"></i>
                Retry
              </button>
            </div>

            <!-- Users Table -->
            <div v-else-if="users.length > 0" class="table-wrapper">
              <table class="users-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Rank</th>
                    <th>Discord</th>
                    <th>Status</th>
                    <th>Joined</th>
                    <th class="actions-header">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in users" :key="user.id" :class="{ inactive: !user.is_active }">
                    <td class="id-cell">{{ user.id }}</td>
                    <td class="username-cell">
                      <i class="fa-solid fa-user"></i>
                      {{ user.username }}
                    </td>
                    <td class="email-cell">{{ user.email || '-' }}</td>
                    <td>
                      <span :class="['role-badge', user.role]">
                        <i :class="user.role === 'admin' ? 'fa-solid fa-shield-halved' : 'fa-solid fa-user'"></i>
                        {{ user.role }}
                      </span>
                    </td>
                    <td class="rank-cell">
                      <div class="rank-display">
                        <img
                          v-if="user.rank_image"
                          :src="user.rank_image"
                          :alt="user.rank"
                          class="rank-image"
                          @error="handleRankImageError"
                        />
                        <span>{{ user.rank }}</span>
                      </div>
                    </td>
                    <td class="discord-cell">
                      <span v-if="user.discord_id" class="discord-tag">
                        <i class="fab fa-discord"></i>
                        {{ user.discord_id }}
                      </span>
                      <span v-else class="local-badge">Local</span>
                    </td>
                    <td>
                      <span :class="['status-badge', user.is_active ? 'active' : 'inactive']">
                        <i :class="user.is_active ? 'fa-solid fa-check-circle' : 'fa-solid fa-times-circle'"></i>
                        {{ user.is_active ? 'Active' : 'Inactive' }}
                      </span>
                    </td>
                    <td class="date-cell">{{ formatDate(user.created_at) }}</td>
                    <td class="actions-cell">
                      <div class="action-buttons">
                        <button
                          @click="openRoleModal(user)"
                          class="action-btn btn-primary"
                          title="Change Role"
                        >
                          <i class="fa-solid fa-user-shield"></i>
                        </button>
                        <button
                          @click="openRankModal(user)"
                          class="action-btn btn-secondary"
                          title="Edit Rank"
                        >
                          <i class="fa-solid fa-medal"></i>
                        </button>
                        <button
                          @click="openDeleteModal(user)"
                          class="action-btn btn-danger"
                          :disabled="!user.is_active"
                          title="Delete User"
                        >
                          <i class="fa-solid fa-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Empty State -->
            <div v-else class="empty-state">
              <i class="fa-solid fa-users-slash"></i>
              <p>No users found</p>
              <button v-if="search || roleFilter" @click="resetFilters" class="reset-button">
                Clear Filters
              </button>
            </div>

            <!-- Pagination -->
            <div v-if="pages > 1" class="pagination">
              <button
                @click="prevPage"
                :disabled="page === 1"
                class="pagination-btn"
              >
                <i class="fa-solid fa-chevron-left"></i>
                Previous
              </button>

              <div class="page-numbers">
                <button
                  v-for="pageNum in displayPages"
                  :key="pageNum"
                  @click="goToPage(pageNum)"
                  :class="['page-btn', { active: pageNum === page }]"
                >
                  {{ pageNum }}
                </button>
              </div>

              <button
                @click="nextPage"
                :disabled="page === pages"
                class="pagination-btn"
              >
                Next
                <i class="fa-solid fa-chevron-right"></i>
              </button>

              <div class="page-info">
                Page {{ page }} of {{ pages }} ({{ total }} users)
              </div>
            </div>
          </div>
        </AnimatedElement>
      </div>
    </section>

    <!-- Role Change Modal -->
    <Teleport to="body">
      <div v-if="showRoleModal" class="modal-overlay" @click="closeRoleModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Change User Role</h3>
            <button @click="closeRoleModal" class="modal-close">
              <i class="fa-solid fa-times"></i>
            </button>
          </div>
          <div class="modal-body">
            <div v-if="selectedUser" class="user-info">
              <p><strong>User:</strong> {{ selectedUser.username }}</p>
              <p><strong>Current Role:</strong> <span :class="['role-badge', selectedUser.role]">{{ selectedUser.role }}</span></p>
            </div>
            <div class="form-group">
              <label for="new-role">New Role:</label>
              <select v-model="newRole" id="new-role" class="modal-select">
                <option value="member">Member</option>
                <option value="admin">Admin</option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeRoleModal" class="modal-btn btn-cancel">Cancel</button>
            <button @click="confirmRoleChange" :disabled="roleChangeLoading" class="modal-btn btn-confirm">
              <i v-if="roleChangeLoading" class="fa-solid fa-spinner fa-spin"></i>
              <span v-else>Confirm</span>
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Rank Edit Modal -->
    <Teleport to="body">
      <div v-if="showRankModal" class="modal-overlay" @click="closeRankModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>Edit User Rank</h3>
            <button @click="closeRankModal" class="modal-close">
              <i class="fa-solid fa-times"></i>
            </button>
          </div>
          <div class="modal-body">
            <div v-if="selectedUser" class="user-info">
              <p><strong>User:</strong> {{ selectedUser.username }}</p>
            </div>
            <div class="form-group">
              <label for="rank-name">Rank Name:</label>
              <input
                v-model="newRank"
                id="rank-name"
                type="text"
                maxlength="50"
                placeholder="Enter rank name"
                class="modal-input"
              />
            </div>
            <div class="form-group">
              <label for="rank-image">Rank Image URL (optional):</label>
              <input
                v-model="newRankImage"
                id="rank-image"
                type="text"
                maxlength="500"
                placeholder="https://example.com/badge.png"
                class="modal-input"
              />
            </div>
            <div v-if="newRankImage" class="rank-preview">
              <p><strong>Preview:</strong></p>
              <img :src="newRankImage" alt="Rank Preview" @error="handlePreviewError" />
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeRankModal" class="modal-btn btn-cancel">Cancel</button>
            <button @click="confirmRankChange" :disabled="rankChangeLoading || !newRank" class="modal-btn btn-confirm">
              <i v-if="rankChangeLoading" class="fa-solid fa-spinner fa-spin"></i>
              <span v-else>Save</span>
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Delete Confirmation Modal -->
    <Teleport to="body">
      <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
        <div class="modal-content modal-danger" @click.stop>
          <div class="modal-header">
            <h3>Delete User</h3>
            <button @click="closeDeleteModal" class="modal-close">
              <i class="fa-solid fa-times"></i>
            </button>
          </div>
          <div class="modal-body">
            <div class="warning-icon">
              <i class="fa-solid fa-exclamation-triangle"></i>
            </div>
            <p v-if="selectedUser" class="warning-text">
              Are you sure you want to delete <strong>{{ selectedUser.username }}</strong>?
              This will deactivate their account and they will no longer be able to login.
            </p>
          </div>
          <div class="modal-footer">
            <button @click="closeDeleteModal" class="modal-btn btn-cancel">Cancel</button>
            <button @click="confirmDelete" :disabled="deleteLoading" class="modal-btn btn-danger">
              <i v-if="deleteLoading" class="fa-solid fa-spinner fa-spin"></i>
              <span v-else>Delete User</span>
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Toast Notification -->
    <Teleport to="body">
      <Transition name="toast">
        <div v-if="toast.show" :class="['toast', toast.type]">
          <i :class="toastIcon"></i>
          <span>{{ toast.message }}</span>
          <button @click="closeToast" class="toast-close">
            <i class="fa-solid fa-times"></i>
          </button>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import type { AdminUser } from '~/types/user'

definePageMeta({
  layout: 'default',
  middleware: ['admin', 'force-password-change']
})

useHead({
  title: 'User Management - Admin',
  meta: [
    {
      name: 'description',
      content: 'Manage system users and permissions.'
    }
  ]
})

const breadcrumbs = [
  { label: 'Home', path: '/' },
  { label: 'Admin', path: '/admin' },
  { label: 'Users' }
]

const {
  users,
  loading,
  error,
  total,
  page,
  pages,
  search,
  roleFilter,
  fetchUsers,
  changeRole,
  changeRank,
  deleteUser,
  nextPage,
  prevPage,
  goToPage,
  resetFilters
} = useAdminUsers()

// Search debounce
let searchTimeout: NodeJS.Timeout
const handleSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    page.value = 1
    fetchUsers()
  }, 500)
}

const clearSearch = () => {
  search.value = ''
  page.value = 1
  fetchUsers()
}

const handleFilterChange = () => {
  page.value = 1
  fetchUsers()
}

// Modal states
const showRoleModal = ref(false)
const showRankModal = ref(false)
const showDeleteModal = ref(false)
const selectedUser = ref<AdminUser | null>(null)
const newRole = ref<'admin' | 'member'>('member')
const newRank = ref('')
const newRankImage = ref('')
const roleChangeLoading = ref(false)
const rankChangeLoading = ref(false)
const deleteLoading = ref(false)

// Toast
const toast = ref({
  show: false,
  message: '',
  type: 'success' as 'success' | 'error'
})

const toastIcon = computed(() => {
  return toast.value.type === 'success' ? 'fa-solid fa-check-circle' : 'fa-solid fa-exclamation-circle'
})

const showToast = (message: string, type: 'success' | 'error' = 'success') => {
  toast.value = { show: true, message, type }
  setTimeout(() => {
    toast.value.show = false
  }, 4000)
}

const closeToast = () => {
  toast.value.show = false
}

// Role change modal
const openRoleModal = (user: AdminUser) => {
  selectedUser.value = user
  newRole.value = user.role
  showRoleModal.value = true
}

const closeRoleModal = () => {
  showRoleModal.value = false
  selectedUser.value = null
}

const confirmRoleChange = async () => {
  if (!selectedUser.value) return
  
  roleChangeLoading.value = true
  const result = await changeRole(selectedUser.value.id, newRole.value)
  roleChangeLoading.value = false
  
  if (result.success) {
    showToast(result.message || 'Role updated successfully', 'success')
    closeRoleModal()
  } else {
    showToast(result.error || 'Failed to update role', 'error')
  }
}

// Rank edit modal
const openRankModal = (user: AdminUser) => {
  selectedUser.value = user
  newRank.value = user.rank
  newRankImage.value = user.rank_image || ''
  showRankModal.value = true
}

const closeRankModal = () => {
  showRankModal.value = false
  selectedUser.value = null
  newRank.value = ''
  newRankImage.value = ''
}

const confirmRankChange = async () => {
  if (!selectedUser.value || !newRank.value) return
  
  rankChangeLoading.value = true
  const result = await changeRank(
    selectedUser.value.id,
    newRank.value,
    newRankImage.value || null
  )
  rankChangeLoading.value = false
  
  if (result.success) {
    showToast(result.message || 'Rank updated successfully', 'success')
    closeRankModal()
  } else {
    showToast(result.error || 'Failed to update rank', 'error')
  }
}

// Delete modal
const openDeleteModal = (user: AdminUser) => {
  selectedUser.value = user
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  selectedUser.value = null
}

const confirmDelete = async () => {
  if (!selectedUser.value) return
  
  deleteLoading.value = true
  const result = await deleteUser(selectedUser.value.id)
  deleteLoading.value = false
  
  if (result.success) {
    showToast(result.message || 'User deleted successfully', 'success')
    closeDeleteModal()
  } else {
    showToast(result.error || 'Failed to delete user', 'error')
  }
}

// Pagination display
const displayPages = computed(() => {
  const maxDisplay = 5
  const current = page.value
  const total = pages.value
  
  if (total <= maxDisplay) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }
  
  const pages: number[] = []
  if (current <= 3) {
    for (let i = 1; i <= 5; i++) pages.push(i)
  } else if (current >= total - 2) {
    for (let i = total - 4; i <= total; i++) pages.push(i)
  } else {
    for (let i = current - 2; i <= current + 2; i++) pages.push(i)
  }
  
  return pages
})

// Utility functions
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const handleRankImageError = (event: Event) => {
  const target = event.target as HTMLImageElement
  target.style.display = 'none'
}

const handlePreviewError = (event: Event) => {
  const target = event.target as HTMLImageElement
  target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODAiIGhlaWdodD0iODAiIHZpZXdCb3g9IjAgMCA4MCA4MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iODAiIGhlaWdodD0iODAiIGZpbGw9IiMzMzMiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZmlsbD0iIzY2NiIgZm9udC1zaXplPSIxMiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlIEVycm9yPC90ZXh0Pjwvc3ZnPg=='
}

// Load users on mount
onMounted(() => {
  fetchUsers()
})
</script>

<style scoped lang="scss">
.users-section {
  padding: 100px 0;
  min-height: 100vh;
}

.users-card {
  background: $background-card;
  border-radius: 12px;
  border: 1px solid $border-color;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

// Card Header
.card-header {
  padding: 2rem;
  border-bottom: 1px solid $border-color;

  .header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;

    .header-info {
      h2 {
        color: $text-primary;
        font-size: 1.8rem;
        margin-bottom: 0.25rem;
        font-weight: 700;
      }

      p {
        color: $text-secondary;
        margin: 0;
        font-size: 0.9rem;
      }
    }
  }

  .controls {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    align-items: center;

    .search-box {
      flex: 1;
      min-width: 250px;
      position: relative;
      display: flex;
      align-items: center;

      i.fa-search {
        position: absolute;
        left: 1rem;
        color: $text-muted;
        pointer-events: none;
      }

      .search-input {
        width: 100%;
        padding: 0.75rem 3rem 0.75rem 2.5rem;
        background: $background-secondary;
        border: 1px solid $border-color;
        border-radius: 8px;
        color: $text-primary;
        font-size: 0.95rem;
        transition: all 0.2s ease;

        &:focus {
          outline: none;
          border-color: $color-accent-1;
          box-shadow: 0 0 0 3px rgba(17, 171, 233, 0.1);
        }

        &::placeholder {
          color: $text-muted;
        }
      }

      .clear-button {
        position: absolute;
        right: 0.5rem;
        background: none;
        border: none;
        color: $text-muted;
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 4px;
        transition: all 0.2s ease;

        &:hover {
          color: $text-primary;
          background: $background-light;
        }
      }
    }

    .filter-box {
      .filter-select {
        padding: 0.75rem 1rem;
        background: $background-secondary;
        border: 1px solid $border-color;
        border-radius: 8px;
        color: $text-primary;
        font-size: 0.95rem;
        cursor: pointer;
        transition: all 0.2s ease;
        min-width: 150px;

        &:hover {
          border-color: $color-accent-1;
        }

        &:focus {
          outline: none;
          border-color: $color-accent-1;
          box-shadow: 0 0 0 3px rgba(17, 171, 233, 0.1);
        }
      }
    }

    .reset-button {
      padding: 0.75rem 1.5rem;
      background: $background-secondary;
      border: 1px solid $border-color;
      border-radius: 8px;
      color: $text-primary;
      font-size: 0.95rem;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 0.5rem;

      &:hover {
        background: $background-light;
        border-color: $color-accent-1;
      }
    }
  }
}

// Loading, Error, Empty States
.loading-state,
.error-state,
.empty-state {
  padding: 4rem 2rem;
  text-align: center;

  i {
    font-size: 3rem;
    margin-bottom: 1rem;
    display: block;
  }

  p {
    color: $text-secondary;
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
  }

  .retry-button {
    padding: 0.75rem 1.5rem;
    background: $button-primary-bg;
    color: $button-primary-text;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    transition: background 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;

    &:hover {
      background: $button-primary-hover;
    }
  }
}

.loading-state i {
  color: $color-accent-1;
}

.error-state i {
  color: $error;
}

.empty-state i {
  color: $text-muted;
}

// Table
.table-wrapper {
  overflow-x: auto;
}

.users-table {
  width: 100%;
  border-collapse: collapse;

  thead {
    background: $background-secondary;

    th {
      padding: 1rem 1.5rem;
      text-align: left;
      font-weight: 600;
      color: $text-primary;
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 2px solid $border-color;
      white-space: nowrap;

      &.actions-header {
        text-align: center;
      }
    }
  }

  tbody {
    tr {
      border-bottom: 1px solid $border-color;
      transition: background 0.2s ease;

      &:hover {
        background: $background-secondary;
      }

      &.inactive {
        opacity: 0.6;
      }
    }

    td {
      padding: 1rem 1.5rem;
      color: $text-secondary;
      vertical-align: middle;
    }

    .id-cell {
      color: $text-muted;
      font-size: 0.9rem;
    }

    .username-cell {
      color: $text-primary;
      font-weight: 600;

      i {
        color: $color-accent-1;
        margin-right: 0.5rem;
      }
    }

    .email-cell {
      font-size: 0.9rem;
    }

    .rank-cell {
      .rank-display {
        display: flex;
        align-items: center;
        gap: 0.5rem;

        .rank-image {
          width: 24px;
          height: 24px;
          object-fit: contain;
        }

        span {
          font-weight: 500;
          color: $text-primary;
        }
      }
    }

    .discord-cell {
      .discord-tag {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;

        i {
          color: #5865F2;
        }
      }

      .local-badge {
        color: $text-muted;
        font-style: italic;
        font-size: 0.9rem;
      }
    }

    .date-cell {
      font-size: 0.9rem;
      white-space: nowrap;
    }

    .actions-cell {
      .action-buttons {
        display: flex;
        gap: 0.5rem;
        justify-content: center;

        .action-btn {
          padding: 0.5rem 0.75rem;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          font-size: 0.9rem;
          transition: all 0.2s ease;
          display: flex;
          align-items: center;
          justify-content: center;

          &:disabled {
            opacity: 0.4;
            cursor: not-allowed;
          }

          &.btn-primary {
            background: rgba($color-primary, 0.2);
            color: $color-primary;

            &:hover:not(:disabled) {
              background: rgba($color-primary, 0.3);
            }
          }

          &.btn-secondary {
            background: rgba($color-secondary, 0.2);
            color: $color-secondary;

            &:hover:not(:disabled) {
              background: rgba($color-secondary, 0.3);
            }
          }

          &.btn-danger {
            background: rgba($error, 0.2);
            color: $error;

            &:hover:not(:disabled) {
              background: rgba($error, 0.3);
            }
          }
        }
      }
    }
  }
}

// Badges
.role-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.875rem;
  border-radius: 16px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;

  &.admin {
    background: rgba(255, 193, 7, 0.2);
    color: #ffc107;
    border: 1px solid rgba(255, 193, 7, 0.3);
  }

  &.member {
    background: rgba(17, 171, 233, 0.2);
    color: $color-accent-1;
    border: 1px solid rgba(17, 171, 233, 0.3);
  }

  i {
    font-size: 0.85rem;
  }
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.875rem;
  border-radius: 16px;
  font-size: 0.8rem;
  font-weight: 600;

  &.active {
    background: rgba($success, 0.2);
    color: $success;
    border: 1px solid rgba($success, 0.3);
  }

  &.inactive {
    background: rgba($error, 0.2);
    color: $error;
    border: 1px solid rgba($error, 0.3);
  }

  i {
    font-size: 0.85rem;
  }
}

// Pagination
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  border-top: 1px solid $border-color;
  flex-wrap: wrap;

  .pagination-btn {
    padding: 0.625rem 1rem;
    background: $background-secondary;
    border: 1px solid $border-color;
    border-radius: 6px;
    color: $text-primary;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    &:not(:disabled):hover {
      background: $color-accent-1;
      color: white;
      border-color: $color-accent-1;
    }
  }

  .page-numbers {
    display: flex;
    gap: 0.5rem;

    .page-btn {
      padding: 0.625rem 0.875rem;
      background: $background-secondary;
      border: 1px solid $border-color;
      border-radius: 6px;
      color: $text-primary;
      cursor: pointer;
      transition: all 0.2s ease;
      font-size: 0.9rem;
      min-width: 40px;

      &.active {
        background: $color-accent-1;
        color: white;
        border-color: $color-accent-1;
      }

      &:not(.active):hover {
        background: $background-light;
        border-color: $color-accent-1;
      }
    }
  }

  .page-info {
    color: $text-muted;
    font-size: 0.875rem;
    white-space: nowrap;
  }
}

// Modal
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.modal-content {
  background: $background-card;
  border-radius: 12px;
  border: 1px solid $border-color;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);

  &.modal-danger {
    border-color: rgba($error, 0.5);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid $border-color;

  h3 {
    color: $text-primary;
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0;
  }

  .modal-close {
    background: none;
    border: none;
    color: $text-muted;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 6px;
    transition: all 0.2s ease;
    font-size: 1.25rem;

    &:hover {
      color: $text-primary;
      background: $background-secondary;
    }
  }
}

.modal-body {
  padding: 1.5rem;

  .user-info {
    padding: 1rem;
    background: $background-secondary;
    border-radius: 8px;
    margin-bottom: 1.5rem;

    p {
      margin: 0.5rem 0;
      color: $text-secondary;

      strong {
        color: $text-primary;
      }
    }
  }

  .warning-icon {
    text-align: center;
    margin-bottom: 1rem;

    i {
      font-size: 3rem;
      color: $error;
    }
  }

  .warning-text {
    color: $text-secondary;
    text-align: center;
    line-height: 1.6;

    strong {
      color: $text-primary;
    }
  }

  .form-group {
    margin-bottom: 1.5rem;

    &:last-child {
      margin-bottom: 0;
    }

    label {
      display: block;
      color: $text-primary;
      font-weight: 600;
      margin-bottom: 0.5rem;
      font-size: 0.9rem;
    }

    .modal-input,
    .modal-select {
      width: 100%;
      padding: 0.75rem;
      background: $background-secondary;
      border: 1px solid $border-color;
      border-radius: 8px;
      color: $text-primary;
      font-size: 0.95rem;
      transition: all 0.2s ease;

      &:focus {
        outline: none;
        border-color: $color-accent-1;
        box-shadow: 0 0 0 3px rgba(17, 171, 233, 0.1);
      }
    }

    .modal-select {
      cursor: pointer;
    }
  }

  .rank-preview {
    margin-top: 1rem;
    padding: 1rem;
    background: $background-secondary;
    border-radius: 8px;
    text-align: center;

    p {
      margin-bottom: 0.75rem;
      color: $text-primary;
      font-weight: 600;
    }

    img {
      max-width: 100px;
      max-height: 100px;
      object-fit: contain;
    }
  }
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid $border-color;

  .modal-btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 600;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }

    &.btn-cancel {
      background: $background-secondary;
      color: $text-primary;
      border: 1px solid $border-color;

      &:hover:not(:disabled) {
        background: $background-light;
      }
    }

    &.btn-confirm {
      background: $button-primary-bg;
      color: $button-primary-text;

      &:hover:not(:disabled) {
        background: $button-primary-hover;
      }
    }

    &.btn-danger {
      background: $error;
      color: white;

      &:hover:not(:disabled) {
        background: darken($error, 10%);
      }
    }
  }
}

// Toast
.toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: $background-card;
  border: 1px solid $border-color;
  border-radius: 8px;
  padding: 1rem 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  gap: 1rem;
  z-index: 10000;
  min-width: 300px;

  &.success {
    border-color: rgba($success, 0.5);

    i {
      color: $success;
    }
  }

  &.error {
    border-color: rgba($error, 0.5);

    i {
      color: $error;
    }
  }

  i {
    font-size: 1.5rem;
  }

  span {
    flex: 1;
    color: $text-primary;
  }

  .toast-close {
    background: none;
    border: none;
    color: $text-muted;
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 4px;
    transition: all 0.2s ease;

    &:hover {
      color: $text-primary;
      background: $background-secondary;
    }
  }
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.toast-leave-to {
  transform: translateY(100%);
  opacity: 0;
}

// Responsive
@media (max-width: 1200px) {
  .users-table {
    th:nth-child(6),
    td:nth-child(6) {
      display: none; // Hide Discord column
    }
  }
}

@media (max-width: 768px) {
  .users-section {
    padding: 60px 0;
  }

  .card-header {
    .controls {
      flex-direction: column;
      align-items: stretch;

      .search-box {
        min-width: 100%;
      }

      .filter-box .filter-select {
        width: 100%;
      }
    }
  }

  .users-table {
    th:nth-child(1),
    td:nth-child(1),
    th:nth-child(8),
    td:nth-child(8) {
      display: none; // Hide ID and Joined columns
    }

    .actions-cell .action-buttons {
      flex-direction: column;
    }
  }

  .pagination {
    flex-direction: column;
    gap: 0.75rem;

    .page-info {
      order: -1;
    }
  }

  .modal-content {
    margin: 1rem;
  }

  .toast {
    left: 1rem;
    right: 1rem;
    bottom: 1rem;
    min-width: auto;
  }
}
</style>
