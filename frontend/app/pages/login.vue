<template>
  <div>
    <!-- Page Header -->
    <PageHeader
      title="Member Login"
      subtitle="Access Your Account"
      :breadcrumbs="breadcrumbs"
    />

    <!-- Login Section -->
    <section class="login-section section-padding">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-6 col-md-8">
            <AnimatedElement animation="fade-in-up" :delay="'.3s'">
              <div class="login-card">
                <div class="login-header">
                  <h2>Welcome Back</h2>
                  <p>Sign in to access your member dashboard</p>
                </div>

                <!-- Discord Login -->
                <div class="discord-login">
                  <button @click="handleDiscordLogin" class="discord-button theme-btn w-100">
                    <i class="fab fa-discord"></i>
                    Login with Discord
                  </button>
                </div>

                <div class="divider">
                  <span>OR</span>
                </div>

                <!-- Admin Login Form -->
                <div class="admin-login">
                  <h3>Admin Login</h3>
                  <form @submit.prevent="handleAdminLogin" class="login-form">
                    <!-- Username Field -->
                    <div class="form-group">
                      <label for="username">Username</label>
                      <div class="input-wrapper">
                        <i class="fa-solid fa-user"></i>
                        <input
                          id="username"
                          v-model="username"
                          type="text"
                          placeholder="Enter username"
                          required
                        />
                      </div>
                    </div>

                    <!-- Password Field -->
                    <div class="form-group">
                      <label for="password">Password</label>
                      <div class="input-wrapper">
                        <i class="fa-solid fa-lock"></i>
                        <input
                          id="password"
                          v-model="password"
                          :type="showPassword ? 'text' : 'password'"
                          placeholder="Enter password"
                          required
                        />
                        <button
                          type="button"
                          class="toggle-password"
                          @click="showPassword = !showPassword"
                          aria-label="Toggle password visibility"
                        >
                          <i :class="showPassword ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye'"></i>
                        </button>
                      </div>
                    </div>

                    <!-- Error Message -->
                    <div v-if="error" class="error-message">
                      <i class="fa-solid fa-exclamation-circle"></i>
                      {{ error }}
                    </div>

                    <!-- Submit Button -->
                    <button type="submit" class="theme-btn w-100" :disabled="loading">
                      <span v-if="!loading">Login</span>
                      <span v-else>
                        <i class="fa-solid fa-spinner fa-spin"></i>
                        Logging in...
                      </span>
                    </button>
                  </form>
                </div>
              </div>
            </AnimatedElement>

            <!-- Info Box -->
            <AnimatedElement animation="fade-in-up" :delay="'.5s'">
              <div class="info-box mt-4">
                <i class="fa-solid fa-info-circle"></i>
                <p>New members can join using Discord OAuth. Admin accounts use local authentication.</p>
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
  middleware: []
})

useHead({
  title: 'Login - FarOut Organization',
  meta: [
    {
      name: 'description',
      content: 'Login to access your FarOut organization member dashboard.'
    }
  ]
})

const breadcrumbs = [
  { label: 'Home', path: '/' },
  { label: 'Login' }
]

const { login, loginWithDiscord } = useAuth()
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const error = ref('')
const loading = ref(false)

const handleDiscordLogin = async () => {
  await loginWithDiscord()
}

const handleAdminLogin = async () => {
  error.value = ''
  loading.value = true

  const result = await login(username.value, password.value)

  loading.value = false

  if (result.success) {
    // Check if password change required
    const { user } = useAuth()
    if (user.value?.must_change_password) {
      navigateTo('/change-password')
    } else {
      navigateTo('/admin')
    }
  } else {
    error.value = result.error || 'Login failed'
  }
}
</script>

<style scoped lang="scss">
.login-section {
  padding: 100px 0;
}

.login-card {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 3rem;
  border: 1px solid var(--border-color);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;

  h2 {
    color: var(--text-primary);
    font-size: 2rem;
    margin-bottom: 0.5rem;
  }

  p {
    color: var(--text-secondary);
  }
}

.discord-login {
  margin-bottom: 1.5rem;

  .discord-button {
    background: #5865F2;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    font-size: 1rem;
    padding: 1rem;

    &:hover {
      background: #4752C4;
    }

    i {
      font-size: 1.5rem;
    }
  }
}

.divider {
  text-align: center;
  margin: 2rem 0;
  position: relative;

  &::before,
  &::after {
    content: '';
    position: absolute;
    top: 50%;
    width: 45%;
    height: 1px;
    background: var(--border-color);
  }

  &::before {
    left: 0;
  }

  &::after {
    right: 0;
  }

  span {
    background: var(--bg-card);
    padding: 0 1rem;
    color: var(--text-muted);
    font-size: 0.9rem;
  }
}

.admin-login {
  h3 {
    color: var(--text-primary);
    font-size: 1.3rem;
    margin-bottom: 1.5rem;
    text-align: center;
  }
}

.login-form {
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

      .toggle-password {
        position: absolute;
        right: 1rem;
        background: none;
        border: none;
        color: var(--text-muted);
        cursor: pointer;
        padding: 0.5rem;
        transition: color 0.3s ease;

        &:hover {
          color: var(--color-accent-1);
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

  .theme-btn {
    margin-top: 1rem;

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  }
}

.info-box {
  background: rgba(17, 171, 233, 0.1);
  border: 1px solid rgba(17, 171, 233, 0.3);
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;

  i {
    color: var(--color-accent-1);
    font-size: 1.5rem;
    flex-shrink: 0;
  }

  p {
    color: var(--text-secondary);
    margin: 0;
    line-height: 1.6;
  }
}
</style>
