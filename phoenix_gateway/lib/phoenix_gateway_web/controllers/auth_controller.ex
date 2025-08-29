defmodule PhoenixGatewayWeb.AuthController do
  use PhoenixGatewayWeb, :controller

  alias PhoenixGateway.Services.AuthService
  alias PhoenixGatewayWeb.Plugs.JwtAuth

  require Logger

  @doc """
  Register a new user.
  """
  def register(conn, user_params) do
    case AuthService.register_user(user_params) do
      {:ok, response} ->
        Logger.info("User registration successful")
        
        conn
        |> put_status(:created)
        |> json(response)

      {:error, {:validation_error, errors}} ->
        Logger.info("User registration failed - validation errors")
        
        conn
        |> put_status(:bad_request)
        |> json(%{error: "Validation failed", details: errors})

      {:error, {:user_exists, message}} ->
        Logger.info("User registration failed - user already exists")
        
        conn
        |> put_status(:conflict)
        |> json(%{error: "User already exists", message: message})

      {:error, :service_error} ->
        Logger.error("Auth service error during registration")
        
        conn
        |> put_status(:internal_server_error)
        |> json(%{error: "Registration service temporarily unavailable"})

      {:error, :connection_failed} ->
        Logger.error("Failed to connect to auth service during registration")
        
        conn
        |> put_status(:service_unavailable)
        |> json(%{error: "Authentication service unavailable"})
    end
  end

  @doc """
  Login user and return authentication token.
  """
  def login(conn, credentials) do
    case AuthService.login_user(credentials) do
      {:ok, response} ->
        Logger.info("User login successful")
        
        # Set cookie if token is in response
        conn = case Map.get(response, "access_token") do
          nil -> conn
          token ->
            conn
            |> put_resp_cookie("access_token", token, [
              http_only: true,
              secure: false, # Set to true in production with HTTPS
              max_age: 24 * 60 * 60, # 24 hours
              same_site: "Lax"
            ])
        end

        conn
        |> put_status(:ok)
        |> json(response)

      {:error, :invalid_credentials} ->
        Logger.info("User login failed - invalid credentials")
        
        conn
        |> put_status(:unauthorized)
        |> json(%{error: "Invalid credentials"})

      {:error, :service_error} ->
        Logger.error("Auth service error during login")
        
        conn
        |> put_status(:internal_server_error)
        |> json(%{error: "Login service temporarily unavailable"})

      {:error, :connection_failed} ->
        Logger.error("Failed to connect to auth service during login")
        
        conn
        |> put_status(:service_unavailable)
        |> json(%{error: "Authentication service unavailable"})
    end
  end

  @doc """
  Refresh authentication token.
  """
  def refresh_token(conn, %{"refresh_token" => refresh_token}) do
    case AuthService.refresh_token(refresh_token) do
      {:ok, response} ->
        Logger.info("Token refresh successful")
        
        conn
        |> put_status(:ok)
        |> json(response)

      {:error, :invalid_token} ->
        Logger.info("Token refresh failed - invalid refresh token")
        
        conn
        |> put_status(:unauthorized)
        |> json(%{error: "Invalid refresh token"})

      {:error, :service_error} ->
        Logger.error("Auth service error during token refresh")
        
        conn
        |> put_status(:internal_server_error)
        |> json(%{error: "Token refresh service temporarily unavailable"})

      {:error, :connection_failed} ->
        Logger.error("Failed to connect to auth service during token refresh")
        
        conn
        |> put_status(:service_unavailable)
        |> json(%{error: "Authentication service unavailable"})
    end
  end

  def refresh_token(conn, _params) do
    conn
    |> put_status(:bad_request)
    |> json(%{error: "Missing refresh_token parameter"})
  end

  @doc """
  Logout user (clear cookies).
  """
  def logout(conn, _params) do
    conn
    |> delete_resp_cookie("access_token")
    |> put_status(:ok)
    |> json(%{message: "Logged out successfully"})
  end

  @doc """
  Validate current token (protected endpoint).
  """
  def validate_token(conn, _params) do
    user = JwtAuth.current_user(conn)
    
    conn
    |> put_status(:ok)
    |> json(%{
      valid: true,
      user: user,
      message: "Token is valid"
    })
  end

  @doc """
  Get current user profile.
  """
  def profile(conn, _params) do
    user = JwtAuth.current_user(conn)
    token = JwtAuth.current_token(conn)
    
    case user do
      %{"user_id" => user_id} ->
        case AuthService.get_user_profile(user_id, token) do
          {:ok, profile} ->
            conn
            |> put_status(:ok)
            |> json(profile)

          {:error, :unauthorized} ->
            conn
            |> put_status(:unauthorized)
            |> json(%{error: "Token expired or invalid"})

          {:error, :user_not_found} ->
            conn
            |> put_status(:not_found)
            |> json(%{error: "User not found"})

          {:error, :service_error} ->
            conn
            |> put_status(:internal_server_error)
            |> json(%{error: "Profile service temporarily unavailable"})

          {:error, :connection_failed} ->
            conn
            |> put_status(:service_unavailable)
            |> json(%{error: "Authentication service unavailable"})
        end

      _ ->
        conn
        |> put_status(:bad_request)
        |> json(%{error: "Invalid user data in token"})
    end
  end
end
