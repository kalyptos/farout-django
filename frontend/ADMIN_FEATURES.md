# Admin Portal Features Reference

Quick reference for developers working on the admin portal.

---

## File Structure

```
frontend/app/
├── composables/
│   └── useAdminUsers.ts          # Admin user management composable
├── pages/
│   └── admin/
│       ├── index.vue              # Admin dashboard
│       ├── users.vue              # User management
│       └── blog/
│           ├── index.vue          # Blog list
│           ├── create.vue         # Create post
│           └── [id].vue           # Edit post
├── middleware/
│   └── admin.ts                   # Admin-only middleware
└── types/
    └── user.ts                    # User type definitions
```

---

## Composables API

### useAdminUsers()

**Usage:**
```typescript
const {
  users,         // Ref<AdminUser[]> - List of users
  loading,       // Ref<boolean> - Loading state
  error,         // Ref<string | null> - Error message
  total,         // Ref<number> - Total user count
  page,          // Ref<number> - Current page
  limit,         // Ref<number> - Users per page
  pages,         // Ref<number> - Total pages
  search,        // Ref<string> - Search query
  roleFilter,    // Ref<'' | 'admin' | 'member'> - Role filter
  fetchUsers,    // () => Promise<void> - Fetch users
  changeRole,    // (userId, newRole) => Promise<Result>
  changeRank,    // (userId, rank, rankImage) => Promise<Result>
  deleteUser,    // (userId) => Promise<Result>
  nextPage,      // () => void - Next page
  prevPage,      // () => void - Previous page
  goToPage,      // (page) => void - Go to page
  resetFilters   // () => void - Reset all filters
} = useAdminUsers()
```

**Methods:**

```typescript
// Fetch users with current filters
await fetchUsers()

// Change user role
const result = await changeRole(userId, 'admin')
if (result.success) {
  // Show success message
} else {
  // Show error: result.error
}

// Update user rank
const result = await changeRank(
  userId, 
  'Captain', 
  'https://example.com/captain.png'
)

// Delete user (soft delete)
const result = await deleteUser(userId)
```

---

## Type Definitions

### AdminUser
```typescript
interface AdminUser {
  id: number
  username: string
  discord_id: string | null
  email: string
  role: 'admin' | 'member'
  rank: string
  rank_image: string | null
  is_active: boolean
  created_at: string
  last_login: string | null
}
```

### UserListResponse
```typescript
interface UserListResponse {
  users: AdminUser[]
  total: number
  page: number
  limit: number
  pages: number
}
```

---

## API Endpoints

### GET /api/admin/users
**Query Params:**
- `page` (int, default: 1)
- `limit` (int, default: 20)
- `role` (string, optional: 'admin' | 'member')
- `search` (string, optional)

**Response:** UserListResponse

### PUT /api/admin/users/{id}/role
**Body:** `{ role: 'admin' | 'member' }`
**Response:** AdminUser

### PUT /api/admin/users/{id}/rank
**Body:** `{ rank: string, rank_image: string | null }`
**Response:** AdminUser

### DELETE /api/admin/users/{id}
**Response:** `{ success: true, message: string, deleted_user_id: number }`

---

## Component Patterns

### Modal Template
```vue
<Teleport to="body">
  <div v-if="showModal" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>Modal Title</h3>
        <button @click="closeModal" class="modal-close">
          <i class="fa-solid fa-times"></i>
        </button>
      </div>
      <div class="modal-body">
        <!-- Content -->
      </div>
      <div class="modal-footer">
        <button @click="closeModal" class="modal-btn btn-cancel">
          Cancel
        </button>
        <button @click="confirm" :disabled="loading" class="modal-btn btn-confirm">
          <i v-if="loading" class="fa-solid fa-spinner fa-spin"></i>
          <span v-else>Confirm</span>
        </button>
      </div>
    </div>
  </div>
</Teleport>
```

### Toast Notification
```vue
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

<script setup>
const toast = ref({
  show: false,
  message: '',
  type: 'success' // 'success' | 'error'
})

const showToast = (message, type = 'success') => {
  toast.value = { show: true, message, type }
  setTimeout(() => {
    toast.value.show = false
  }, 4000)
}
</script>
```

### Debounced Search
```vue
<input
  v-model="search"
  @input="handleSearch"
  type="text"
  placeholder="Search..."
/>

<script setup>
let searchTimeout: NodeJS.Timeout

const handleSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    page.value = 1
    fetchUsers()
  }, 500)
}
</script>
```

---

## Styling Guidelines

### Color Variables
```scss
// Use these SCSS variables (auto-imported)
$text-primary         // Main text color
$text-secondary       // Secondary text
$text-muted           // Muted text

$background-card      // Card backgrounds
$background-secondary // Secondary backgrounds
$background-light     // Light backgrounds

$border-color         // Default borders
$border-color-light   // Light borders

$color-primary        // Primary blue
$color-secondary      // Lime green
$color-accent         // Red accent
$color-accent-1       // Star Citizen blue

$success              // Success green
$warning              // Warning orange
$error                // Error red

$button-primary-bg    // Primary button
$button-primary-hover // Primary button hover
```

### Responsive Breakpoints
```scss
// Mobile
@media (max-width: 768px) { }

// Tablet
@media (max-width: 1200px) { }

// Desktop (default)
```

### Badge Pattern
```scss
.role-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.875rem;
  border-radius: 16px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;

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
}
```

---

## Best Practices

### 1. State Management
```typescript
// Use refs for reactive state
const loading = ref(false)
const error = ref<string | null>(null)
const data = ref<Type[]>([])

// Use computed for derived state
const isEmpty = computed(() => data.value.length === 0)
const hasError = computed(() => error.value !== null)
```

### 2. Error Handling
```typescript
try {
  const result = await fetchApi('/endpoint')
  // Handle success
} catch (e: any) {
  error.value = e.message || 'An error occurred'
  
  // Handle specific errors
  if (e.statusCode === 403) {
    await navigateTo('/user')
  } else if (e.statusCode === 401) {
    await navigateTo('/login')
  }
}
```

### 3. Loading States
```typescript
const performAction = async () => {
  loading.value = true
  try {
    await doSomething()
    showToast('Success!', 'success')
  } catch (e) {
    showToast('Failed!', 'error')
  } finally {
    loading.value = false
  }
}
```

### 4. Security
```typescript
// Always check permissions
definePageMeta({
  middleware: ['admin', 'force-password-change']
})

// Never trust client-side validation alone
// Backend must validate all inputs

// Prevent self-modification
if (targetUserId === currentUser.id) {
  throw new Error('Cannot modify your own account')
}
```

### 5. Accessibility
```html
<!-- Use semantic HTML -->
<button type="button">Click me</button>

<!-- Add aria labels -->
<button aria-label="Delete user">
  <i class="fa-solid fa-trash"></i>
</button>

<!-- Use proper form labels -->
<label for="username">Username:</label>
<input id="username" type="text" />

<!-- Indicate loading states -->
<button :disabled="loading" :aria-busy="loading">
  Submit
</button>
```

---

## Common Tasks

### Adding a New Modal
1. Add state: `const showModal = ref(false)`
2. Add open function: `const openModal = () => { showModal.value = true }`
3. Add close function: `const closeModal = () => { showModal.value = false }`
4. Add template with `<Teleport to="body">`
5. Add styles for `.modal-overlay` and `.modal-content`

### Adding a New Filter
1. Add ref: `const newFilter = ref('')`
2. Add to URL params in `fetchUsers()`
3. Add UI control (select, input, etc.)
4. Add @change handler to call `fetchUsers()`
5. Include in `resetFilters()`

### Adding a New Action
1. Add method to composable
2. Add button to actions cell in table
3. Add modal if needed
4. Handle loading state
5. Show toast on success/error
6. Refresh data after action

---

## Debugging Tips

### Check API Response
```typescript
const data = await fetchApi('/endpoint')
console.log('API Response:', data)
```

### Check Reactive State
```vue
<script setup>
watch(users, (newVal) => {
  console.log('Users changed:', newVal)
})
</script>
```

### Check Component Rendering
```vue
<template>
  <div>
    <pre>{{ JSON.stringify(users, null, 2) }}</pre>
  </div>
</template>
```

### Check Network Requests
- Open browser DevTools
- Go to Network tab
- Filter by XHR/Fetch
- Check request/response

---

## Performance Tips

1. **Debounce search:** Prevent excessive API calls
2. **Paginate data:** Limit results per page
3. **Use v-show for modals:** Faster than v-if
4. **Lazy load images:** Use loading="lazy" attribute
5. **Memoize computed values:** Use computed() not ref()
6. **Avoid deep watchers:** Watch specific properties
7. **Use keys in v-for:** Helps Vue optimize rendering

---

## Testing Checklist

- [ ] Page loads without errors
- [ ] All data displays correctly
- [ ] Search works
- [ ] Filters work
- [ ] Pagination works
- [ ] Actions complete successfully
- [ ] Modals open/close correctly
- [ ] Toasts appear and dismiss
- [ ] Loading states prevent double-clicks
- [ ] Error handling works
- [ ] Responsive design works
- [ ] No console errors
- [ ] No memory leaks (check DevTools)

---

## Related Documentation

- Backend API: `/home/ubuntu/docker/farout/BACKEND_CHANGES.md`
- Testing Guide: `/home/ubuntu/docker/farout/ADMIN_PORTAL_TESTING_GUIDE.md`
- Completion Report: `/home/ubuntu/docker/farout/ADMIN_PORTAL_COMPLETE.md`
- Project Overview: `/home/ubuntu/docker/farout/CLAUDE.md`
