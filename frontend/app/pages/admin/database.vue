<template>
  <div class="container section-padding">
    <div class="row">
      <div class="col-12">
        <h1 class="mb-4">Database Management</h1>
        
        <!-- Database Status Cards -->
        <div class="row mb-4">
          <div v-for="(db, name) in databases" :key="name" class="col-md-6 mb-3">
            <div class="database-card" :class="db.connected ? 'connected' : 'disconnected'">
              <div class="card-header">
                <h3>{{ db.database_name }}</h3>
                <span class="status-badge" :class="db.connected ? 'online' : 'offline'">
                  {{ db.connected ? 'ONLINE' : 'OFFLINE' }}
                </span>
              </div>
              <div class="card-body">
                <p><strong>Host:</strong> {{ db.host }}</p>
                <p><strong>Port:</strong> {{ db.port }}</p>
                <p v-if="db.connected"><strong>Tables:</strong> {{ db.tables_count }}</p>
                <p v-if="db.error" class="error-message">{{ db.error }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Test Connection Form -->
        <div class="test-connection-card">
          <h2>Test Database Connection</h2>
          <form @submit.prevent="testConnection">
            <div class="form-group">
              <label>Host</label>
              <input v-model="testForm.host" type="text" required />
            </div>
            <div class="form-group">
              <label>Port</label>
              <input v-model.number="testForm.port" type="number" required />
            </div>
            <div class="form-group">
              <label>Database</label>
              <input v-model="testForm.database" type="text" required />
            </div>
            <div class="form-group">
              <label>Username</label>
              <input v-model="testForm.username" type="text" required />
            </div>
            <div class="form-group">
              <label>Password</label>
              <input v-model="testForm.password" type="password" required />
            </div>
            <button type="submit" class="theme-btn" :disabled="testing">
              {{ testing ? 'Testing...' : 'Test Connection' }}
            </button>
          </form>
          
          <div v-if="testResult" class="test-result" :class="testResult.success ? 'success' : 'error'">
            {{ testResult.message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

definePageMeta({
  middleware: ['auth', 'admin']
})

const databases = ref({})
const testing = ref(false)
const testResult = ref(null)

const testForm = ref({
  host: '',
  port: 5432,
  database: '',
  username: '',
  password: ''
})

const fetchDatabaseStatus = async () => {
  try {
    const config = useRuntimeConfig()
    const response = await $fetch(`${config.public.apiBase}/api/admin/database/status`, {
      credentials: 'include'
    })
    databases.value = response
  } catch (error) {
    console.error('Failed to fetch database status:', error)
  }
}

const testConnection = async () => {
  testing.value = true
  testResult.value = null
  
  try {
    const config = useRuntimeConfig()
    const response = await $fetch(`${config.public.apiBase}/api/admin/database/test-connection`, {
      method: 'POST',
      body: testForm.value,
      credentials: 'include'
    })
    testResult.value = { success: true, message: response.message }
  } catch (error: any) {
    testResult.value = { 
      success: false, 
      message: error.data?.detail || 'Connection test failed' 
    }
  } finally {
    testing.value = false
  }
}

onMounted(() => {
  fetchDatabaseStatus()
})
</script>

<style scoped>
.section-padding {
  padding: 80px 0;
}

.database-card {
  background: rgba(26, 26, 26, 0.95);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.database-card.connected {
  border-color: #4CAF50;
}

.database-card.disconnected {
  border-color: #DB2E21;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
}

.card-header h3 {
  color: #fff;
  margin: 0;
  font-size: 1.25rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-badge.online {
  background: #4CAF50;
  color: #fff;
}

.status-badge.offline {
  background: #DB2E21;
  color: #fff;
}

.card-body p {
  color: rgba(255, 255, 255, 0.85);
  margin-bottom: 0.5rem;
}

.card-body p strong {
  color: #fff;
}

.test-connection-card {
  background: rgba(26, 26, 26, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 2rem;
  margin-top: 2rem;
}

.test-connection-card h2 {
  color: #fff;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #fff;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  color: #fff;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #0EA5E9;
}

.theme-btn {
  background: #0EA5E9;
  color: #fff;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s ease;
}

.theme-btn:hover:not(:disabled) {
  background: #0284C7;
}

.theme-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.test-result {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 4px;
  font-weight: 500;
}

.test-result.success {
  background: rgba(76, 175, 80, 0.2);
  border: 1px solid #4CAF50;
  color: #4CAF50;
}

.test-result.error {
  background: rgba(219, 46, 33, 0.2);
  border: 1px solid #DB2E21;
  color: #DB2E21;
}

.error-message {
  color: #DB2E21;
  font-size: 0.875rem;
}
</style>
