# Import os module for operating system interactions and environment variables
import os
# Import load_dotenv function to load environment variables from .env file
from dotenv import load_dotenv

# Load environment variables from .env file into the application's environment
load_dotenv()

class Config:
    """Configuration class to manage application settings and environment variables."""
    
    # Class variable to store GROQ API key from environment
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    @staticmethod
    def validate():
        """Validate that required configuration values are properly set.
        
        Raises:
            ValueError: If GROQ_API_KEY is not set in environment variables
        """
        # Check if GROQ_API_KEY is unset or empty
        if not Config.GROQ_API_KEY:
            # Raise an error if the key is missing
            raise ValueError("GROQ_API_KEY is not set in the .env file")