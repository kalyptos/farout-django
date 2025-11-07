<template>
  <div>
    <!-- Page Header -->
    <PageHeader
      title="Change Password"
      subtitle="Update Your Password"
      :breadcrumbs="breadcrumbs"
    />

    <!-- Change Password Section -->
    <section class="change-password-section section-padding">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-6 col-md-8">
            <AnimatedElement animation="fade-in-up" :delay="'.3s'">
              <div class="password-card">
                <div v-if="user?.must_change_password" class="notice-box">
                  <i class="fa-solid fa-exclamation-triangle"></i>
                  <p>You must change your password before continuing.</p>
                </div>

                <form @submit.prevent="handleChangePassword" class="password-form">
                  <!-- Current Password -->
                  <div class="form-group">
                    <label for="old-password">Current Password</label>
                    <div class="input-wrapper">
                      <i class="fa-solid fa-lock"></i>
                      <input
                        id="old-password"
                        v-model="oldPassword"
                        type="password"
                        placeholder="Enter current password"
                        required
                      />
                    </div>
                  </div>

                  <!-- New Password -->
                  <div class="form-group">
                    <label for="new-password">New Password</label>
                    <div class="input-wrapper">
                      <i class="fa-solid fa-key"></i>
                      <input
                        id="new-password"
                        v-model="newPassword"
                        type="password"
                        placeholder="Enter new password (min 8 characters)"
                        required
                        minlength="8"
                      />
                    </div>
                  </div>

                  <!-- Confirm Password -->
                  <div class="form-group">
                    <label for="confirm-password">Confirm New Password</label>
                    <div class="input-wrapper">
                      <i class="fa-solid fa-key"></i>
                      <input
                        id="confirm-password"
                        v-model="confirmPassword"
                        type="password"
                        placeholder="Confirm new password"
                        required
                      />
                    </div>
                  </div>

                  <!-- Error Message -->
                  <div v-if="error" class="error-message">
                    <i class="fa-solid fa-exclamation-circle"></i>
                    {{ error }}
                  </div>

                  <!-- Success Message -->
                  <div v-if="success" class="success-message">
                    <i class="fa-solid fa-check-circle"></i>
                    Password changed successfully! Redirecting...
                  </div>

                  <!-- Submit Button -->
                  <button type="submit" class="theme-btn w-100" :disabled="loading">
                    <span v-if="!loading">Change Password</span>
                    <span v-else>
                      <i class="fa-solid fa-spinner fa-spin"></i>
                      Changing...
                    </span>
                  </button>
                </form>
              </div>
            </AnimatedElement>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
  middleware: ['auth']
})

useHead({
  title: 'Change Password - FarOut Organization',
  meta: [
    {
      name: 'description',
      content: 'Change your account password.'
    }
  ]
})

const breadcrumbs = [
  { label: 'Home', path: '/' },
  { label: 'Change Password' }
]

const { changePassword, user } = useAuth()
const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const error = ref('')
const success = ref(false)
const loading = ref(false)

const handleChangePassword = async () => {
  error.value = ''
  success.value = false

  // Validate passwords match
  if (newPassword.value !== confirmPassword.value) {
    error.value = 'New passwords do not match'
    return
  }

  // Validate password length
  if (newPassword.value.length < 8) {
    error.value = 'Password must be at least 8 characters'
    return
  }

  loading.value = true

  const result = await changePassword(oldPassword.value, newPassword.value)

  loading.value = false

  if (result.success) {
    success.value = true
    setTimeout(() => {
      navigateTo('/admin')
    }, 2000)
  } else {
    error.value = result.error || 'Password change failed'
  }
}
</script>

<style scoped lang="scss">
.change-password-section {
  padding: 100px 0;
}

.password-card {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 3rem;
  border: 1px solid var(--border-color);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.notice-box {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.3);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;

  i {
    color: #dc3545;
    font-size: 1.5rem;
    flex-shrink: 0;
  }

  p {
    color: #dc3545;
    font-weight: 500;
    margin: 0;
  }
}

.password-form {
  .form-group {
    margin-bottom: 1.5rem;

    label {
      display: block;
      color: var(--text-primary);
      font-weight: 500;
      margin-bottom: 0.5rem;
    }

    .input-wrapper {
      position: relative;
      display: flex;
      align-items: center;

      i {
        position: absolute;
        left: 1rem;
        color: var(--color-accent-1);
        pointer-events: none;
      }

      input {
        width: 100%;
        padding: 0.875rem 1rem 0.875rem 3rem;
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-primary);
        font-size: 1rem;
        transition: all 0.3s ease;

        &:focus {
          outline: none;
          border-color: var(--color-accent-1);
          box-shadow: 0 0 0 3px rgba(17, 171, 233, 0.1);
        }

        &::placeholder {
          color: var(--text-muted);
        }
      }
    }
  }

  .error-message {
    color: #dc3545;
    padding: 0.75rem;
    background: rgba(220, 53, 69, 0.1);
    border: 1px solid rgba(220, 53, 69, 0.3);
    border-radius: 8px;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;

    i {
      font-size: 1.1rem;
    }
  }

  .success-message {
    color: #28a745;
    padding: 0.75rem;
    background: rgba(40, 167, 69, 0.1);
    border: 1px solid rgba(40, 167, 69, 0.3);
    border-radius: 8px;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;

    i {
      font-size: 1.1rem;
    }
  }

  .theme-btn {
    margin-top: 1rem;

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  }
}
</style>
