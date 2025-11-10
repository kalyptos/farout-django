# Build argument for Node version
ARG NODE_VERSION=20

# --- Build stage ---
FROM node:${NODE_VERSION}-alpine AS builder

WORKDIR /app

# Install build dependencies for native modules (node-gyp, etc.)
RUN apk add --no-cache python3 make g++

# Copy package files
COPY package*.json ./

# Install ALL dependencies with verbose output
RUN echo "Installing dependencies..." && \
    npm install --verbose 2>&1 | tee npm-install.log || \
    (echo "❌ NPM INSTALL FAILED" && cat npm-install.log && exit 1)

# Copy source code
COPY . .

# Run Nuxt prepare and build with verbose output
RUN echo "Running Nuxt prepare..." && \
    npm run prepare --verbose 2>&1 | tee npm-prepare.log || \
    (echo "❌ PREPARE FAILED" && cat npm-prepare.log && exit 1)

RUN echo "Running Nuxt build..." && \
    npm run build --verbose 2>&1 | tee npm-build.log || \
    (echo "❌ BUILD FAILED" && cat npm-build.log && exit 1)

# Debug: Show what was built
RUN echo "=== Build output ===" && \
    ls -la .output/ && \
    ls -la .output/server/ && \
    echo "=== End build output ===" || echo "Build directory not found"

# Verify build output exists - fail fast if build didn't work
RUN test -f .output/server/index.mjs || \
    (echo "❌ ERROR: Build failed - .output/server/index.mjs not found" && \
     echo "This usually means:" && \
     echo "  1. npm run build failed silently" && \
     echo "  2. SSR is not enabled in nuxt.config.ts" && \
     echo "  3. Dependencies are missing" && \
     exit 1)

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
COPY --from=builder --chown=app:app /app/.output ./.output

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
