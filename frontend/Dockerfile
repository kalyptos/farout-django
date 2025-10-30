# --- Build stage ---
FROM node:20-alpine AS build

WORKDIR /app

# Prepare workspace and use non-root user
RUN mkdir -p /app && chown -R node:node /app
USER node

# Install deps (use lockfile if present)
COPY --chown=node:node package.json package-lock.json* ./
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# Copy source and build Nuxt (Nitro) to .output
COPY --chown=node:node . .
RUN npx nuxi prepare && npx nuxi build

# Sanity: fail the image build if Nitro server isn't present
RUN test -f .output/server/index.mjs || (echo "❌ No Nitro server found in .output/server. Ensure ssr: true and nitro.preset: 'node' in nuxt.config.ts" && exit 1)

# --- Runtime stage ---
FROM node:20-alpine
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
CMD ["node", ".output/server/index.mjs"]