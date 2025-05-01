from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    Application configuration settings that are loaded from environment variables.

    Default values are provided for settings, which will be used if they are not specified in the .env file.
    """
    # List of allowed origins for CORS (Cross-Origin Resource Sharing)
    allowed_origins: str = "http://localhost,http://127.0.0.1"
    
    # Path to the pre-trained model file used by the application
    model_path: str = "/fastapi-ml-stack/app/models/regression_model.pkl"

    class Config:
        """
        Configuration class for Pydantic settings to specify the environment file.
        """
        # Path to the .env file that contains sensitive credentials or configurations
        env_file = ".env"  
        
        # Specify the encoding of the .env file
        env_file_encoding = 'utf-8'

# Instantiate the Settings class to load configuration values
settings: Settings = Settings()
