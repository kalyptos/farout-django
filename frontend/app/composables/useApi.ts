import { ref } from 'vue'

interface ApiError {
  message: string
  statusCode?: number
  data?: unknown
}

interface UseApiOptions {
  onError?: (error: ApiError) => void
  showErrorToast?: boolean
}

export function useApi(options: UseApiOptions = {}) {
  const config = useRuntimeConfig()
  const loading = ref(false)
  const error = ref<ApiError | null>(null)

  // Determine the correct API base URL based on environment
  const getApiBase = () => {
    if (import.meta.server) {
      // Server-side: use internal Docker network
      const serverBase = config.apiBaseServer || 'http://farout_backend:8000'
      return serverBase
    } else {
      // Client-side: use public API base
      const clientBase = config.public.apiBase
      if (!clientBase) {
        throw new Error(
          'API base URL not configured. Set NUXT_PUBLIC_API_BASE environment variable in .env file.'
        )
      }
      return clientBase
    }
  }

  const fetchApi = async <T = any>(
    endpoint: string,
    fetchOptions: RequestInit = {}
  ): Promise<T> => {
    loading.value = true
    error.value = null

    try {
      const apiBase = getApiBase()
      const url = `${apiBase}${endpoint.startsWith('/api') ? endpoint : `/api${endpoint}`}`

      const response = await $fetch<T>(url, {
        ...fetchOptions,
        credentials: 'include', // Send cookies with requests
        headers: {
          'Content-Type': 'application/json',
          ...fetchOptions.headers,
        },
      })

      return response
    } catch (err: unknown) {
      // Type guard for error object
      const isErrorWithMessage = (error: unknown): error is { message: string } => {
        return typeof error === 'object' && error !== null && 'message' in error
      }

      const isErrorWithStatus = (error: unknown): error is { statusCode?: number; status?: number; data?: unknown } => {
        return typeof error === 'object' && error !== null && ('statusCode' in error || 'status' in error)
      }

      const apiError: ApiError = {
        message: isErrorWithMessage(err) ? err.message : 'An error occurred',
        statusCode: isErrorWithStatus(err) ? (err.statusCode || err.status) : undefined,
        data: isErrorWithStatus(err) ? err.data : undefined,
      }

      error.value = apiError

      // Call custom error handler if provided
      if (options.onError) {
        options.onError(apiError)
      }

      // Optionally show error toast (requires a toast library to be implemented)
      if (options.showErrorToast) {
        // TODO: Integrate with a toast notification system
      }

      throw err
    } finally {
      loading.value = false
    }
  }

  const get = async <T = any>(endpoint: string): Promise<T> => {
    return fetchApi<T>(endpoint, { method: 'GET' })
  }

  const post = async <T = unknown, TBody = unknown>(
    endpoint: string,
    body: TBody
  ): Promise<T> => {
    return fetchApi<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(body),
    })
  }

  const put = async <T = unknown, TBody = unknown>(
    endpoint: string,
    body: TBody
  ): Promise<T> => {
    return fetchApi<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body),
    })
  }

  const del = async <T = any>(endpoint: string): Promise<T> => {
    return fetchApi<T>(endpoint, { method: 'DELETE' })
  }

  const clearError = () => {
    error.value = null
  }

  return {
    loading,
    error,
    fetchApi,
    get,
    post,
    put,
    delete: del,
    clearError,
  }
}
