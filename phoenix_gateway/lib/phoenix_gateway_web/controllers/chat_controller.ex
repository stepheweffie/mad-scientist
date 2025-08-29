defmodule PhoenixGatewayWeb.ChatController do
  use PhoenixGatewayWeb, :controller

  alias PhoenixGateway.Services.{AuthService, ChatService}
  alias PhoenixGatewayWeb.Plugs.JwtAuth

  require Logger

  @doc """
  Send a chat message and get AI response.
  """
  def send_message(conn, %{"message" => message} = params) do
    user = JwtAuth.current_user(conn)
    token = JwtAuth.current_token(conn)
    
    user_context = build_user_context(user, params)
    
    case ChatService.send_message(message, user_context, token) do
      {:ok, response} ->
        Logger.info("Chat message sent successfully", user_id: user["user_id"])
        
        conn
        |> put_status(:ok)
        |> json(response)

      {:error, :unauthorized} ->
        Logger.info("Chat message failed - unauthorized", user_id: user["user_id"])
        
        conn
        |> put_status(:unauthorized)
        |> json(%{error: "Session expired, please login again"})

      {:error, :rate_limited} ->
        Logger.info("Chat message failed - rate limited", user_id: user["user_id"])
        
        conn
        |> put_status(:too_many_requests)
        |> json(%{error: "Rate limit exceeded, please wait before sending another message"})

      {:error, :service_error} ->
        Logger.error("Chat service error", user_id: user["user_id"])
        
        conn
        |> put_status(:internal_server_error)
        |> json(%{error: "Chat service temporarily unavailable"})

      {:error, :connection_failed} ->
        Logger.error("Failed to connect to chat service", user_id: user["user_id"])
        
        conn
        |> put_status(:service_unavailable)
        |> json(%{error: "Chat service unavailable"})
    end
  end

  def send_message(conn, _params) do
    conn
    |> put_status(:bad_request)
    |> json(%{error: "Missing required 'message' parameter"})
  end

  @doc """
  Get chat history for the current user.
  """
  def get_history(conn, params) do
    user = JwtAuth.current_user(conn)
    token = JwtAuth.current_token(conn)
    
    case user do
      %{"user_id" => user_id} ->
        # Extract query parameters for pagination/filtering
        opts = extract_history_options(params)
        
        case ChatService.get_chat_history(user_id, token, opts) do
          {:ok, history} ->
            Logger.info("Chat history retrieved successfully", user_id: user_id)
            
            conn
            |> put_status(:ok)
            |> json(history)

          {:error, :unauthorized} ->
            Logger.info("Chat history failed - unauthorized", user_id: user_id)
            
            conn
            |> put_status(:unauthorized)
            |> json(%{error: "Session expired, please login again"})

          {:error, :user_not_found} ->
            Logger.info("Chat history failed - user not found", user_id: user_id)
            
            conn
            |> put_status(:not_found)
            |> json(%{error: "User not found"})

          {:error, :service_error} ->
            Logger.error("Chat service error during history retrieval", user_id: user_id)
            
            conn
            |> put_status(:internal_server_error)
            |> json(%{error: "Chat service temporarily unavailable"})

          {:error, :connection_failed} ->
            Logger.error("Failed to connect to chat service for history", user_id: user_id)
            
            conn
            |> put_status(:service_unavailable)
            |> json(%{error: "Chat service unavailable"})
        end

      _ ->
        conn
        |> put_status(:bad_request)
        |> json(%{error: "Invalid user data in token"})
    end
  end

  @doc """
  Generate avatar for the current user.
  """
  def generate_avatar(conn, %{"preferences" => preferences} = _params) do
    user = JwtAuth.current_user(conn)
    token = JwtAuth.current_token(conn)
    
    case user do
      %{"user_id" => user_id} ->
        case ChatService.generate_avatar(user_id, preferences, token) do
          {:ok, avatar_data} ->
            Logger.info("Avatar generated successfully", user_id: user_id)
            
            conn
            |> put_status(:ok)
            |> json(avatar_data)

          {:error, :unauthorized} ->
            conn
            |> put_status(:unauthorized)
            |> json(%{error: "Session expired, please login again"})

          {:error, {:validation_error, errors}} ->
            conn
            |> put_status(:bad_request)
            |> json(%{error: "Invalid preferences", details: errors})

          {:error, :service_error} ->
            Logger.error("Chat service error during avatar generation", user_id: user_id)
            
            conn
            |> put_status(:internal_server_error)
            |> json(%{error: "Avatar service temporarily unavailable"})

          {:error, :connection_failed} ->
            Logger.error("Failed to connect to chat service for avatar", user_id: user_id)
            
            conn
            |> put_status(:service_unavailable)
            |> json(%{error: "Avatar service unavailable"})
        end

      _ ->
        conn
        |> put_status(:bad_request)
        |> json(%{error: "Invalid user data in token"})
    end
  end

  def generate_avatar(conn, _params) do
    conn
    |> put_status(:bad_request)
    |> json(%{error: "Missing required 'preferences' parameter"})
  end

  @doc """
  Get user's avatar.
  """
  def get_avatar(conn, _params) do
    user = JwtAuth.current_user(conn)
    token = JwtAuth.current_token(conn)
    
    case user do
      %{"user_id" => user_id} ->
        case ChatService.get_avatar(user_id, token) do
          {:ok, avatar_data} ->
            conn
            |> put_status(:ok)
            |> json(avatar_data)

          {:error, :unauthorized} ->
            conn
            |> put_status(:unauthorized)
            |> json(%{error: "Session expired, please login again"})

          {:error, :avatar_not_found} ->
            conn
            |> put_status(:not_found)
            |> json(%{error: "Avatar not found, please generate one first"})

          {:error, :service_error} ->
            Logger.error("Chat service error during avatar retrieval", user_id: user_id)
            
            conn
            |> put_status(:internal_server_error)
            |> json(%{error: "Avatar service temporarily unavailable"})

          {:error, :connection_failed} ->
            Logger.error("Failed to connect to chat service for avatar", user_id: user_id)
            
            conn
            |> put_status(:service_unavailable)
            |> json(%{error: "Avatar service unavailable"})
        end

      _ ->
        conn
        |> put_status(:bad_request)
        |> json(%{error: "Invalid user data in token"})
    end
  end

  @doc """
  Combined endpoint that fetches user profile and chat history.
  """
  def dashboard(conn, params) do
    user = JwtAuth.current_user(conn)
    token = JwtAuth.current_token(conn)
    
    case user do
      %{"user_id" => user_id} ->
        # Concurrently fetch profile and chat history
        profile_task = Task.async(fn -> 
          AuthService.get_user_profile(user_id, token) 
        end)
        
        history_opts = extract_history_options(params)
        history_task = Task.async(fn -> 
          ChatService.get_chat_history(user_id, token, history_opts) 
        end)
        
        avatar_task = Task.async(fn -> 
          ChatService.get_avatar(user_id, token) 
        end)
        
        profile_result = Task.await(profile_task, 5000)
        history_result = Task.await(history_task, 5000)
        avatar_result = Task.await(avatar_task, 5000)
        
        dashboard_data = %{
          profile: case profile_result do
            {:ok, data} -> data
            {:error, _} -> nil
          end,
          chat_history: case history_result do
            {:ok, data} -> data
            {:error, _} -> []
          end,
          avatar: case avatar_result do
            {:ok, data} -> data
            {:error, _} -> nil
          end,
          meta: %{
            profile_available: match?({:ok, _}, profile_result),
            history_available: match?({:ok, _}, history_result),
            avatar_available: match?({:ok, _}, avatar_result)
          }
        }
        
        conn
        |> put_status(:ok)
        |> json(dashboard_data)

      _ ->
        conn
        |> put_status(:bad_request)
        |> json(%{error: "Invalid user data in token"})
    end
  end

  # Private helper functions

  defp build_user_context(user, params) do
    base_context = %{
      user_id: user["user_id"],
      username: user["username"] || user["email"],
      timestamp: DateTime.utc_now() |> DateTime.to_iso8601()
    }
    
    # Add optional context parameters
    params
    |> Map.take(["context", "conversation_id", "thread_id"])
    |> Enum.reduce(base_context, fn {key, value}, acc ->
      Map.put(acc, String.to_atom(key), value)
    end)
  end

  defp extract_history_options(params) do
    params
    |> Map.take(["limit", "offset", "start_date", "end_date", "conversation_id"])
    |> Enum.map(fn {key, value} -> {String.to_atom(key), value} end)
  end
end
