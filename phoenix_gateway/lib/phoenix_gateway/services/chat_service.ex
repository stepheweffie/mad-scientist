defmodule PhoenixGateway.Services.ChatService do
  @moduledoc """
  Service for communicating with the FastAPI chat service.
  """

  require Logger

  @base_url Application.compile_env(:phoenix_gateway, :chat_service_url, "http://chat-service:8000")

  @doc """
  Sends a chat message to the FastAPI service and gets AI response.
  """
  def send_message(message, user_context, token) do
    headers = [{"Authorization", "Bearer #{token}"}]
    
    payload = %{
      message: message,
      user_context: user_context,
      timestamp: DateTime.utc_now() |> DateTime.to_iso8601()
    }

    case Req.post("#{@base_url}/chat", json: payload, headers: headers) do
      {:ok, %{status: 200, body: body}} ->
        {:ok, body}
      {:ok, %{status: 401}} ->
        {:error, :unauthorized}
      {:ok, %{status: 429}} ->
        {:error, :rate_limited}
      {:ok, %{status: status, body: body}} ->
        Logger.warning("Chat service returned status #{status}: #{inspect(body)}")
        {:error, :service_error}
      {:error, reason} ->
        Logger.error("Failed to connect to chat service: #{inspect(reason)}")
        {:error, :connection_failed}
    end
  end

  @doc """
  Gets chat history for a user from the FastAPI service.
  """
  def get_chat_history(user_id, token, opts \\ []) do
    headers = [{"Authorization", "Bearer #{token}"}]
    
    query_params = Enum.into(opts, %{})
    
    case Req.get("#{@base_url}/chat/history/#{user_id}", 
                 headers: headers, 
                 params: query_params) do
      {:ok, %{status: 200, body: body}} ->
        {:ok, body}
      {:ok, %{status: 401}} ->
        {:error, :unauthorized}
      {:ok, %{status: 404}} ->
        {:error, :user_not_found}
      {:ok, %{status: status, body: body}} ->
        Logger.warning("Chat service returned status #{status}: #{inspect(body)}")
        {:error, :service_error}
      {:error, reason} ->
        Logger.error("Failed to connect to chat service: #{inspect(reason)}")
        {:error, :connection_failed}
    end
  end

  @doc """
  Generates an avatar for a user via the FastAPI service.
  """
  def generate_avatar(user_id, preferences, token) do
    headers = [{"Authorization", "Bearer #{token}"}]
    
    payload = %{
      user_id: user_id,
      preferences: preferences
    }

    case Req.post("#{@base_url}/avatar/generate", json: payload, headers: headers) do
      {:ok, %{status: 200, body: body}} ->
        {:ok, body}
      {:ok, %{status: 401}} ->
        {:error, :unauthorized}
      {:ok, %{status: 400, body: body}} ->
        {:error, {:validation_error, body}}
      {:ok, %{status: status, body: body}} ->
        Logger.warning("Chat service returned status #{status}: #{inspect(body)}")
        {:error, :service_error}
      {:error, reason} ->
        Logger.error("Failed to connect to chat service: #{inspect(reason)}")
        {:error, :connection_failed}
    end
  end

  @doc """
  Gets user's avatar from the FastAPI service.
  """
  def get_avatar(user_id, token) do
    headers = [{"Authorization", "Bearer #{token}"}]
    
    case Req.get("#{@base_url}/avatar/#{user_id}", headers: headers) do
      {:ok, %{status: 200, body: body}} ->
        {:ok, body}
      {:ok, %{status: 401}} ->
        {:error, :unauthorized}
      {:ok, %{status: 404}} ->
        {:error, :avatar_not_found}
      {:ok, %{status: status, body: body}} ->
        Logger.warning("Chat service returned status #{status}: #{inspect(body)}")
        {:error, :service_error}
      {:error, reason} ->
        Logger.error("Failed to connect to chat service: #{inspect(reason)}")
        {:error, :connection_failed}
    end
  end

  @doc """
  Health check for the FastAPI chat service.
  """
  def health_check do
    case Req.get("#{@base_url}/health") do
      {:ok, %{status: 200, body: body}} ->
        {:ok, body}
      {:ok, %{status: status}} ->
        Logger.warning("Chat service health check returned status #{status}")
        {:error, :unhealthy}
      {:error, reason} ->
        Logger.error("Failed to connect to chat service: #{inspect(reason)}")
        {:error, :connection_failed}
    end
  end
end
