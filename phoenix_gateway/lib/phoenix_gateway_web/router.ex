defmodule PhoenixGatewayWeb.Router do
  use PhoenixGatewayWeb, :router

  alias PhoenixGatewayWeb.Plugs.JwtAuth

  pipeline :api do
    plug :accepts, ["json"]
    plug CORSPlug, origin: ["http://localhost:3000", "http://localhost:80"]
  end

  pipeline :auth_required do
    plug JwtAuth
  end

  pipeline :auth_optional do
    plug JwtAuth, :optional_auth
  end

  # Health check endpoint
  scope "/", PhoenixGatewayWeb do
    pipe_through :api
    
    get "/health", HealthController, :health_check
  end

  # Public authentication endpoints
  scope "/api/auth", PhoenixGatewayWeb do
    pipe_through :api

    post "/register", AuthController, :register
    post "/login", AuthController, :login
    post "/refresh", AuthController, :refresh_token
    post "/logout", AuthController, :logout
  end

  # Protected authentication endpoints
  scope "/api/auth", PhoenixGatewayWeb do
    pipe_through [:api, :auth_required]

    get "/validate", AuthController, :validate_token
    get "/profile", AuthController, :profile
  end

  # Protected chat endpoints
  scope "/api/chat", PhoenixGatewayWeb do
    pipe_through [:api, :auth_required]

    post "/message", ChatController, :send_message
    get "/history", ChatController, :get_history
    get "/avatar", ChatController, :get_avatar
    post "/avatar", ChatController, :generate_avatar
  end

  # Combined dashboard endpoint
  scope "/api/dashboard", PhoenixGatewayWeb do
    pipe_through [:api, :auth_required]

    get "/", ChatController, :dashboard
  end

  # Enable LiveDashboard and Swoosh mailbox preview in development
  if Application.compile_env(:phoenix_gateway, :dev_routes) do
    # If you want to use the LiveDashboard in production, you should put
    # it behind authentication and allow only admins to access it.
    # If your application does not have an admins-only section yet,
    # you can use Plug.BasicAuth to set up some basic authentication
    # as long as you are also using SSL (which you should anyway).
    import Phoenix.LiveDashboard.Router

    scope "/dev" do
      pipe_through [:fetch_session, :protect_from_forgery]

      live_dashboard "/dashboard", metrics: PhoenixGatewayWeb.Telemetry
      forward "/mailbox", Plug.Swoosh.MailboxPreview
    end
  end
end
