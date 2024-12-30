import logging
from dotenv import load_dotenv
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings

# Load environment variables from the .env file
load_dotenv(".env")

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("config_errors.log"),  # Logs to a file
        logging.StreamHandler(),  # Logs to the console
    ],
)

logger = logging.getLogger(__name__)


# Define AppConfig class for configuration management
class AppConfig(BaseSettings):
    wikipedia_access_token: str = Field(..., env="WIKIPEDIA_ACCESS_TOKEN")
    wikipedia_api_url: str = Field(..., env="WIKIPEDIA_API_URL")
    wikipedia_user_agent: str = Field(..., env="WIKIPEDIA_USER_AGENT")
    postgres_db: str = Field(..., env="POSTGRES_DB")
    postgres_host: str = Field(..., env="POSTGRES_HOST")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
    postgres_port: int = Field(..., env="POSTGRES_PORT")
    postgres_user: str = Field(..., env="POSTGRES_USER")
    postgres_url: str = Field(..., env="POSTGRES_URL")
    tmdb_api_key: str = Field(..., env="TMDB_API_KEY")
    tmdb_api_url: str = Field(..., env="TMDB_API_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def postgres_url(self) -> str:
        return (
            f"postgres://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


try:
    config = AppConfig()
except ValidationError as e:
    # Log each error with detailed information
    for error in e.errors():
        logger.warning(
            "Configuration validation failed. "
            f"Field: {error['loc'][0]}, "
            f"Error: {error['msg']}, "
            f"Value: {error.get('ctx', {}).get('given', 'N/A')}"
        )
    # Re-raise the exception to stop execution if critical
    raise
