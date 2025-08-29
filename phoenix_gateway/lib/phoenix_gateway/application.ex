defmodule PhoenixGateway.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      PhoenixGatewayWeb.Telemetry,
      PhoenixGateway.Repo,
      {DNSCluster, query: Application.get_env(:phoenix_gateway, :dns_cluster_query) || :ignore},
      {Phoenix.PubSub, name: PhoenixGateway.PubSub},
      # Start the Finch HTTP client for sending emails
      {Finch, name: PhoenixGateway.Finch},
      # Start a worker by calling: PhoenixGateway.Worker.start_link(arg)
      # {PhoenixGateway.Worker, arg},
      # Start to serve requests, typically the last entry
      PhoenixGatewayWeb.Endpoint
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: PhoenixGateway.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  @impl true
  def config_change(changed, _new, removed) do
    PhoenixGatewayWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
