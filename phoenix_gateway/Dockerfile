# Use the official Elixir image
FROM elixir:1.15-otp-26-alpine

# Install system dependencies
RUN apk add --no-cache \
    build-base \
    git \
    nodejs \
    npm

# Set build ENV
ENV MIX_ENV=prod

# Create app directory
WORKDIR /app

# Install hex and rebar
RUN mix local.hex --force && \
    mix local.rebar --force

# Copy mix files
COPY mix.exs mix.lock ./

# Install mix dependencies
RUN mix deps.get --only prod && \
    mix deps.compile

# Copy application code
COPY . .

# Compile the application
RUN mix compile

# Build release
RUN mix release

# Start a new stage for the runtime
FROM alpine:3.18

# Install runtime dependencies
RUN apk add --no-cache \
    bash \
    openssl \
    ncurses-libs

# Create app user
RUN addgroup -g 1001 -S appuser && \
    adduser -S -D -H -u 1001 -h /app -s /bin/bash -G appuser appuser

# Set build ENV
ENV MIX_ENV=prod

# Create app directory
WORKDIR /app

# Copy built application
COPY --from=0 --chown=appuser:appuser /app/_build/prod/rel/phoenix_gateway ./

# Change to appuser
USER appuser

# Expose port
EXPOSE 4000

# Set health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:4000/health || exit 1

# Start the application
CMD ["./bin/phoenix_gateway", "start"]
