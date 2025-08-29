defmodule PhoenixGateway.Services.AuthService do
  @moduledoc """
  Service for communicating with the Flask authentication service.
  """

  alias PhoenixGateway.Services.CircuitBreaker
  
  require Logger

  @base_url Application.compile_env(:phoenix_gateway, :auth_service_url, "http://auth-service:5000")
  @service_name "auth_service"

  @doc """
  Validates a JWT token by calling the Flask auth service.
  """
  def validate_token(token) do
    CircuitBreaker.call(@service_name, fn ->
      headers = [{"Authorization", "Bearer #{token}"}]
      
      case Req.get("#{@base_url}/validate", headers: headers) do
        {:ok, %{status: 200, body: body}} ->
          {:ok, body}
        {:ok, %{status: 401}} ->
          {:error, :unauthorized}
        {:ok, %{status: status}} ->
          Logger.warning("Auth service returned status #{status}")
          {:error, :service_error}
        {:error, reason} ->
          Logger.error("Failed to connect to auth service: #{inspect(reason)}")
          {:error, :connection_failed}
      end
    end)
  end

  @doc """
  Registers a new user via the Flask auth service.
  """
  def register_user(user_params) do
    case Req.post("#{@base_url}/register", json: user_params) do
      {:ok, %{status: 201, body: body}} ->
        {:ok, body}
      {:ok, %{status: 400, body: body}} ->
        {:error, {:validation_error, body}}
      {:ok, %{status: 409, body: body}} ->
        {:error, {:user_exists, body}}
      {:ok, %{status: status, body: body}} ->
        Logger.warning("Auth service returned status #{status}: #{inspect(body)}")
        {:error, :service_error}
      {:error, reason} ->
        Logger.error("Failed to connect to auth service: #{inspect(reason)}")
        {:error, :connection_failed}
    end
  end

  @doc """
  Authenticates a user via the Flask auth service.
  """
  def login_user(credentials) do
    case Req.post("#{@base_url}/login", json: credentials) do
      {:ok, %{status: 200, body: body}} ->
        {:ok, body}
      {:ok, %{status: 401}} ->
        {:error, :invalid_credentials}
      {:ok, %{status: status, body: body}} ->
        Logger.warning("Auth service returned status #{status}: #{inspect(body)}")
        {:error, :service_error}
      {:error, reason} ->
        Logger.error("Failed to connect to auth service: #{inspect(reason)}")
        {:error, :connection_failed}
    end
  end

  @doc """
  Refreshes a JWT token via the Flask auth service.
  """
  def refresh_token(refresh_token) do
    case Req.post("#{@base_url}/refresh", json: %{refresh_token: refresh_token}) do
      {:ok, %{status: 200, body: body}} ->
        {:ok, body}
      {:ok, %{status: 401}} ->
        {:error, :invalid_token}
      {:ok, %{status: status, body: body}} ->
        Logger.warning("Auth service returned status #{status}: #{inspect(body)}")
        {:error, :service_error}
      {:error, reason} ->
        Logger.error("Failed to connect to auth service: #{inspect(reason)}")
        {:error, :connection_failed}
    end
  end

  @doc """
  Gets user profile from the Flask auth service.
  """
  def get_user_profile(user_id, token) do
    headers = [{"Authorization", "Bearer #{token}"}]
    
    case Req.get("#{@base_url}/user/#{user_id}", headers: headers) do
      {:ok, %{status: 200, body: body}} ->
        {:ok, body}
      {:ok, %{status: 401}} ->
        {:error, :unauthorized}
      {:ok, %{status: 404}} ->
        {:error, :user_not_found}
      {:ok, %{status: status, body: body}} ->
        Logger.warning("Auth service returned status #{status}: #{inspect(body)}")
        {:error, :service_error}
      {:error, reason} ->
        Logger.error("Failed to connect to auth service: #{inspect(reason)}")
        {:error, :connection_failed}
    end
  end
end
