# Build argument for Node version
ARG NODE_VERSION=20

# --- Build stage ---
FROM node:${NODE_VERSION}-alpine AS build

WORKDIR /app

# Prepare workspace and use non-root user
RUN mkdir -p /app && chown -R node:node /app
USER node

# Install deps (use lockfile if present)
# WORKAROUND: npm has a bug with optional dependencies on Alpine Linux
# Remove package-lock.json to avoid oxc-parser native binding issues
COPY --chown=node:node package.json ./
RUN npm install

# Copy source and build Nuxt (Nitro) to .output
COPY --chown=node:node . .
RUN npx nuxi prepare && npx nuxi build

# Sanity: fail the image build if Nitro server isn't present
RUN test -f .output/server/index.mjs || (echo "❌ No Nitro server found in .output/server. Ensure ssr: true and nitro.preset: 'node' in nuxt.config.ts" && exit 1)

# --- Runtime stage ---
FROM node:${NODE_VERSION}-alpine

# OCI labels
LABEL org.opencontainers.image.title="Farout Frontend" \
      org.opencontainers.image.description="Nuxt 4 SSR frontend for Star Citizen organization management" \
      org.opencontainers.image.vendor="Farout" \
      org.opencontainers.image.version="1.0.0"

WORKDIR /app

# Install healthcheck tool and create non-root user
RUN apk add --no-cache curl && \
    addgroup -g 10000 app && \
    adduser -D -u 10000 -G app app

# Copy only runtime artifacts with proper ownership
COPY --from=build --chown=app:app /app/.output ./.output

# Switch to non-root user
USER app

# Ensure Nitro binds correctly
ENV NODE_ENV=production \
    PORT=3000 \
    NITRO_PORT=3000 \
    NUXT_PORT=3000 \
    HOST=0.0.0.0 \
    NITRO_HOST=0.0.0.0 \
    NUXT_HOST=0.0.0.0

EXPOSE 3000

# Health check
HEALTHCHECK --interval=10s --timeout=3s --start-period=30s --retries=3 \
  CMD curl -fsS --max-time 2 http://127.0.0.1:3000/ || exit 1

CMD ["node", ".output/server/index.mjs"]
