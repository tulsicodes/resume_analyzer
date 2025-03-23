# Import json module for JSON file parsing
import json
# Import os module for operating system interactions
import os

class PromptLoader:
    """Class to load and manage prompt templates from a JSON file."""
    
    def __init__(self, prompts_file):
        """Initialize PromptLoader with a prompts file path.
        
        Args:
            prompts_file (str): Path to the JSON file containing prompt templates
        """
        # Store the prompts file path
        self.prompts_file = prompts_file
        # Load prompts during initialization
        self.prompts = self._load_prompts()

    def _load_prompts(self):
        """Load prompt templates from the JSON file.
        
        Returns:
            dict: Dictionary of prompt templates loaded from file
        """
        # Open and read the JSON file with UTF-8 encoding
        with open(self.prompts_file, "r", encoding="utf-8") as f:
            # Parse JSON content into a dictionary
            prompts = json.load(f)
        # Return the loaded prompts
        return prompts

    def get_prompt(self, prompt_key, **kwargs):
        """Retrieve and format a specific prompt template.
        
        Args:
            prompt_key (str): Key to identify the desired prompt in the JSON
            **kwargs: Keyword arguments to format the prompt template
            
        Returns:
            str: Formatted prompt string
        """
        # Get the template string from prompts dictionary
        template = self.prompts[prompt_key]["template"]
        # Format the template with provided keyword arguments
        return template.format(**kwargs)