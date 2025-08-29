defmodule PhoenixGateway.Repo do
  use Ecto.Repo,
    otp_app: :phoenix_gateway,
    adapter: Ecto.Adapters.Postgres
end
