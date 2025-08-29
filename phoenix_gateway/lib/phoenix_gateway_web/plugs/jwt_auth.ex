defmodule PhoenixGatewayWeb.Plugs.JwtAuth do
  @moduledoc """
  Plug for JWT authentication in the Phoenix gateway.
  Validates JWT tokens and extracts user information for downstream service calls.
  """

  import Plug.Conn
  import Phoenix.Controller
  
  alias PhoenixGateway.Services.AuthService
  
  require Logger

  def init(opts), do: opts

  def call(conn, _opts) do
    case extract_token(conn) do
      {:ok, token} -> 
        validate_and_assign_user(conn, token)
      {:error, :no_token} ->
        unauthorized_response(conn)
    end
  end

  @doc """
  Extracts JWT token from Authorization header or cookies.
  """
  defp extract_token(conn) do
    case get_req_header(conn, "authorization") do
      ["Bearer " <> token] -> 
        {:ok, token}
      [] -> 
        extract_token_from_cookie(conn)
      _ -> 
        {:error, :no_token}
    end
  end

  defp extract_token_from_cookie(conn) do
    case Map.get(conn.req_cookies, "access_token") do
      nil -> {:error, :no_token}
      token -> {:ok, token}
    end
  end

  @doc """
  Validates token with the auth service and assigns user data to conn.
  """
  defp validate_and_assign_user(conn, token) do
    case AuthService.validate_token(token) do
      {:ok, user_data} ->
        conn
        |> assign(:current_user, user_data)
        |> assign(:auth_token, token)
      
      {:error, :unauthorized} ->
        Logger.info("JWT validation failed - unauthorized")
        unauthorized_response(conn)
      
      {:error, :connection_failed} ->
        Logger.error("Failed to connect to auth service for token validation")
        service_error_response(conn)
      
      {:error, :service_error} ->
        Logger.error("Auth service error during token validation")
        service_error_response(conn)
    end
  end

  @doc """
  Optional authentication - doesn't halt on missing/invalid tokens.
  """
  def optional_auth(conn, _opts) do
    case extract_token(conn) do
      {:ok, token} -> 
        case AuthService.validate_token(token) do
          {:ok, user_data} ->
            conn
            |> assign(:current_user, user_data)
            |> assign(:auth_token, token)
          {:error, _reason} ->
            conn
            |> assign(:current_user, nil)
            |> assign(:auth_token, nil)
        end
      {:error, :no_token} ->
        conn
        |> assign(:current_user, nil)
        |> assign(:auth_token, nil)
    end
  end

  @doc """
  Checks if user has specific role or permission.
  """
  def require_role(conn, %{role: required_role}) do
    case conn.assigns[:current_user] do
      %{"role" => user_role} when user_role == required_role ->
        conn
      %{"roles" => user_roles} when is_list(user_roles) ->
        if required_role in user_roles do
          conn
        else
          forbidden_response(conn)
        end
      _ ->
        forbidden_response(conn)
    end
  end

  def require_role(conn, _opts), do: conn

  # Response helpers
  defp unauthorized_response(conn) do
    conn
    |> put_status(:unauthorized)
    |> json(%{
      error: "Unauthorized", 
      message: "Valid authentication required"
    })
    |> halt()
  end

  defp forbidden_response(conn) do
    conn
    |> put_status(:forbidden)
    |> json(%{
      error: "Forbidden", 
      message: "Insufficient permissions"
    })
    |> halt()
  end

  defp service_error_response(conn) do
    conn
    |> put_status(:service_unavailable)
    |> json(%{
      error: "Service Unavailable", 
      message: "Authentication service temporarily unavailable"
    })
    |> halt()
  end

  @doc """
  Helper to get current user from conn assigns.
  """
  def current_user(conn) do
    conn.assigns[:current_user]
  end

  @doc """
  Helper to get current auth token from conn assigns.
  """
  def current_token(conn) do
    conn.assigns[:auth_token]
  end

  @doc """
  Helper to check if user is authenticated.
  """
  def authenticated?(conn) do
    not is_nil(conn.assigns[:current_user])
  end
end
