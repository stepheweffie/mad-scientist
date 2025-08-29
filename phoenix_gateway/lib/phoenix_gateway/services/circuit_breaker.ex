defmodule PhoenixGateway.Services.CircuitBreaker do
  @moduledoc """
  Circuit breaker implementation for resilient service communication.
  Uses the Fuse library to implement the circuit breaker pattern.
  """

  require Logger

  @default_options [
    fuse_strategy: {:standard, 5, 10_000},  # 5 failures in 10 seconds
    fuse_refresh: 60_000,                   # Reset after 60 seconds
    retry: true
  ]

  @doc """
  Execute a function with circuit breaker protection.
  """
  def call(service_name, fun, opts \\ []) do
    fuse_name = String.to_atom("#{service_name}_circuit")
    options = Keyword.merge(@default_options, opts)
    
    # Install fuse if it doesn't exist
    case :fuse.circuit_state(fuse_name) do
      {:error, :not_found} ->
        install_fuse(fuse_name, options)
      _ ->
        :ok
    end
    
    case :fuse.ask(fuse_name, :sync) do
      :ok ->
        try do
          case fun.() do
            {:ok, result} -> 
              {:ok, result}
            {:error, reason} = error -> 
              handle_service_error(fuse_name, reason)
              error
            other -> 
              other
          end
        rescue
          e ->
            Logger.error("Circuit breaker caught exception for #{service_name}: #{inspect(e)}")
            :fuse.melt(fuse_name)
            {:error, :service_exception}
        end
        
      :blown ->
        Logger.warning("Circuit breaker is open for #{service_name}")
        {:error, :circuit_breaker_open}
        
      {:error, :not_found} ->
        Logger.error("Circuit breaker not found for #{service_name}")
        {:error, :circuit_breaker_not_found}
    end
  end

  @doc """
  Check the current state of a circuit breaker.
  """
  def circuit_state(service_name) do
    fuse_name = String.to_atom("#{service_name}_circuit")
    :fuse.circuit_state(fuse_name)
  end

  @doc """
  Manually reset a circuit breaker.
  """
  def reset(service_name) do
    fuse_name = String.to_atom("#{service_name}_circuit")
    :fuse.reset(fuse_name)
  end

  @doc """
  Get circuit breaker statistics.
  """
  def stats(service_name) do
    fuse_name = String.to_atom("#{service_name}_circuit")
    
    case :fuse.circuit_state(fuse_name) do
      {:error, :not_found} ->
        %{
          service: service_name,
          state: :not_found,
          error: "Circuit breaker not initialized"
        }
      state ->
        %{
          service: service_name,
          state: state,
          timestamp: DateTime.utc_now() |> DateTime.to_iso8601()
        }
    end
  end

  # Private helper functions

  defp install_fuse(fuse_name, options) do
    strategy = Keyword.get(options, :fuse_strategy)
    refresh = Keyword.get(options, :fuse_refresh)
    
    case :fuse.install(fuse_name, {strategy, refresh}) do
      :ok ->
        Logger.info("Circuit breaker installed: #{fuse_name}")
        :ok
      {:error, :already_installed} ->
        :ok
      error ->
        Logger.error("Failed to install circuit breaker #{fuse_name}: #{inspect(error)}")
        error
    end
  end

  defp handle_service_error(fuse_name, reason) do
    case reason do
      :connection_failed ->
        Logger.warning("Service connection failed, melting fuse: #{fuse_name}")
        :fuse.melt(fuse_name)
      
      :service_error ->
        Logger.warning("Service error, melting fuse: #{fuse_name}")
        :fuse.melt(fuse_name)
      
      :timeout ->
        Logger.warning("Service timeout, melting fuse: #{fuse_name}")
        :fuse.melt(fuse_name)
      
      _ ->
        # Don't melt the fuse for business logic errors like unauthorized, validation_error, etc.
        :ok
    end
  end
end
