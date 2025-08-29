import Config

# Service URLs
config :phoenix_gateway,
  auth_service_url: System.get_env("AUTH_SERVICE_URL", "http://auth-service:5000"),
  chat_service_url: System.get_env("CHAT_SERVICE_URL", "http://chat-service:8000")

# Configures Swoosh API Client
config :swoosh, api_client: Swoosh.ApiClient.Finch, finch_name: PhoenixGateway.Finch

# Disable Swoosh Local Memory Storage
config :swoosh, local: false

# Do not print debug messages in production
config :logger, level: :info

# Runtime production configuration, including reading
# of environment variables, is done on config/runtime.exs.
