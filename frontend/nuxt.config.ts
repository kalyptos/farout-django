// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },

  future: {
    compatibilityVersion: 4,
  },

  // CRITICAL: Explicit source directory for Nuxt 4 app/ structure
  srcDir: 'app/',

  // Directory paths for Nuxt 4 structure (relative to srcDir)
  dir: {
    pages: 'pages',
    layouts: 'layouts'
  },

  // Component auto-import configuration
  components: [
    {
      path: '~/components',  // With srcDir: 'app/', this resolves to app/components
      pathPrefix: false,
    }
  ],

  css: ['~/assets/scss/main.scss', 'vue-final-modal/style.css'],  // With srcDir, ~ resolves to app/

  // Add the @nuxt/image module
  modules: [
    '@nuxt/image'
  ],

  // IMAGE OPTIMIZATION CONFIG
  image: {
    quality: 80,
    format: ['webp', 'jpeg'],
    screens: {
      xs: 320,
      sm: 640,
      md: 768,
      lg: 1024,
      xl: 1280,
      xxl: 1536,
    },
    presets: {
      background: {
        modifiers: {
          format: 'webp',
          quality: 70,
          width: 1920,
        }
      }
    }
  },

  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          api: 'modern-compiler',
          additionalData: `
            @use "~/assets/scss/variables/_colors.scss" as *;
            @use "~/assets/scss/variables/_typography.scss" as *;
            @use "~/assets/scss/variables/_breakpoints.scss" as *;
            @use "~/assets/scss/mixins/_responsive.scss" as *;
          `
        }
      }
    }
  },

  app: {
    head: {
      title: 'Far Out - Star Citizen Organization',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content: 'Far Out - A Star Citizen organization dedicated to exploration, trading, mining, and adventure across the \'Verse. Join our crew today!'
        }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/assets/img/favicon.svg' },
        // PRELOAD BACKGROUND IMAGE for faster initial render
        { rel: 'preload', as: 'image', href: '/assets/space-background.jpg', type: 'image/jpeg' },
        // Library CSS files (for better caching - not bundled)
        { rel: 'stylesheet', href: '/assets/css/bootstrap.min.css' },
        { rel: 'stylesheet', href: '/assets/css/all.min.css' },
        { rel: 'stylesheet', href: '/assets/css/animate.css' },
        { rel: 'stylesheet', href: '/assets/css/magnific-popup.css' },
        { rel: 'stylesheet', href: '/assets/css/meanmenu.css' },
        { rel: 'stylesheet', href: '/assets/css/swiper-bundle.min.css' },
        { rel: 'stylesheet', href: '/assets/css/nice-select.css' }
      ],
      script: [
        // All JS files have been removed.
        // Interactivity must be re-implemented using
        // npm packages and client-side plugins.
      ]
    }
  },

  // Runtime config for API
  runtimeConfig: {
    // Private (server-only) - for SSR calls within Docker network
    apiBaseServer: process.env.NUXT_API_BASE_SERVER || 'http://farout_backend:8000',
    // Public (both server and client) - for browser calls to public IP
    // CRITICAL: Must be set via NUXT_PUBLIC_API_BASE environment variable
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE
    }
  }
})