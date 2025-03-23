# Import Groq class from groq library for API interactions
from groq import Groq
# Import Config class from utils.config module for configuration management
from utils.config import Config

class GroqHandler:
    """Class to handle interactions with the Groq API for text analysis."""
    
    def __init__(self):
        """Initialize GroqHandler with validated configuration and API client."""
        # Validate configuration settings
        Config.validate()
        # Create Groq client instance with API key from Config
        self.client = Groq(api_key=Config.GROQ_API_KEY)

    def analyze_text(self, prompt, text, model="gemma2-9b-it", max_tokens=2000):
        """Analyze text using the Groq API with specified prompt and parameters.
        
        Args:
            prompt (str): The instruction or question to guide the analysis
            text (str): The text to analyze
            model (str): The Groq model to use (default: "gemma2-9b-it")
            max_tokens (int): Maximum number of tokens in response (default: 2000)
            
        Returns:
            str: The analyzed text response from the Groq API
        """
        # Send request to Groq API with combined prompt and text
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt + "\n\n" + text}],
            model=model,
            max_tokens=max_tokens
        )
        # Return the stripped content from the first response choice
        return response.choices[0].message.content.strip()