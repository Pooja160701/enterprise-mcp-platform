from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "Enterprise MCP Platform"

    API_VERSION: str = "v1"

    API_HOST: str = "0.0.0.0"

    API_PORT: int = 8000

    OPENAI_API_KEY: str = ""

    POSTGRES_USER: str = "postgres"

    POSTGRES_PASSWORD: str = "postgres"

    POSTGRES_DB: str = "enterprise_mcp"

    REDIS_HOST: str = "redis"

    REDIS_PORT: int = 6379

    JWT_SECRET: str = "secret"

    class Config:
        env_file = ".env"


settings = Settings()