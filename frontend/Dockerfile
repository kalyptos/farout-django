# Build argument for Node version
ARG NODE_VERSION=20

# --- Build stage ---
FROM node:${NODE_VERSION}-alpine AS builder

WORKDIR /app

# Install build dependencies for native modules (sass, sharp, etc.)
RUN apk add --no-cache python3 make g++

# Copy package files
COPY package*.json ./

# Install dependencies (npm ci for reproducible builds)
RUN npm ci

# Copy all source code (includes app/ directory - Nuxt 4 uses srcDir: 'app/')
COPY . .

# Build Nuxt 4 application (nuxt.config.ts specifies srcDir: 'app/')
RUN npm run build

# Verify build output exists
RUN test -f .output/server/index.mjs || \
    (echo "❌ Build failed - .output/server/index.mjs not found" && exit 1)

# --- Runtime stage ---
FROM node:${NODE_VERSION}-alpine

WORKDIR /app

# Install curl for healthcheck and create non-root user
RUN apk add --no-cache curl && \
    addgroup -g 10000 app && \
    adduser -D -u 10000 -G app app

# Copy built output from builder
COPY --from=builder --chown=app:app /app/.output /app/.output

# Switch to non-root user
USER app

# Ensure Nitro binds correctly
ENV NODE_ENV=production \
    PORT=3000 \
    NITRO_PORT=3000 \
    HOST=0.0.0.0 \
    NITRO_HOST=0.0.0.0

EXPOSE 3000

# Health check
HEALTHCHECK --interval=10s --timeout=3s --start-period=30s --retries=3 \
  CMD curl -fsS --max-time 2 http://127.0.0.1:3000/ || exit 1

CMD ["node", ".output/server/index.mjs"]
