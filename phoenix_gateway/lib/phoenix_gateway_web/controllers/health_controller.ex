defmodule PhoenixGatewayWeb.HealthController do
  use PhoenixGatewayWeb, :controller

  alias PhoenixGateway.Services.{AuthService, ChatService}

  require Logger

  @doc """
  Health check endpoint that verifies the status of all services.
  """
  def health_check(conn, _params) do
    start_time = System.monotonic_time()
    
    # Check individual services
    auth_status = check_auth_service()
    chat_status = check_chat_service()
    
    end_time = System.monotonic_time()
    response_time_ms = System.convert_time_unit(end_time - start_time, :native, :millisecond)
    
    overall_status = determine_overall_status([auth_status, chat_status])
    
    health_data = %{
      status: overall_status,
      timestamp: DateTime.utc_now() |> DateTime.to_iso8601(),
      response_time_ms: response_time_ms,
      services: %{
        phoenix_gateway: %{
          status: "healthy",
          version: Application.spec(:phoenix_gateway, :vsn) |> to_string()
        },
        auth_service: auth_status,
        chat_service: chat_status
      },
      system_info: %{
        elixir_version: System.version(),
        otp_version: System.otp_release(),
        phoenix_version: Application.spec(:phoenix, :vsn) |> to_string()
      }
    }
    
    status_code = case overall_status do
      "healthy" -> 200
      "degraded" -> 200  # Still responding but some services down
      "unhealthy" -> 503
    end
    
    conn
    |> put_status(status_code)
    |> json(health_data)
  end

  # Private helper functions

  defp check_auth_service do
    case AuthService.validate_token("dummy_token_for_health_check") do
      {:ok, _} -> 
        %{status: "healthy", message: "Auth service responding"}
      {:error, :unauthorized} -> 
        %{status: "healthy", message: "Auth service responding (expected unauthorized)"}
      {:error, :connection_failed} -> 
        %{status: "unhealthy", message: "Cannot connect to auth service"}
      {:error, :service_error} -> 
        %{status: "degraded", message: "Auth service error"}
    end
  rescue
    e -> 
      Logger.error("Health check auth service error: #{inspect(e)}")
      %{status: "unhealthy", message: "Auth service health check failed"}
  end

  defp check_chat_service do
    case ChatService.health_check() do
      {:ok, _} -> 
        %{status: "healthy", message: "Chat service responding"}
      {:error, :connection_failed} -> 
        %{status: "unhealthy", message: "Cannot connect to chat service"}
      {:error, :unhealthy} -> 
        %{status: "degraded", message: "Chat service reports unhealthy"}
    end
  rescue
    e -> 
      Logger.error("Health check chat service error: #{inspect(e)}")
      %{status: "unhealthy", message: "Chat service health check failed"}
  end

  defp determine_overall_status(service_statuses) do
    statuses = Enum.map(service_statuses, &Map.get(&1, :status))
    
    cond do
      Enum.all?(statuses, &(&1 == "healthy")) -> "healthy"
      Enum.any?(statuses, &(&1 == "unhealthy")) -> "unhealthy"
      true -> "degraded"
    end
  end
end
