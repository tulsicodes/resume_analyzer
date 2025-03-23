class ResumeAnalyzer:
    """Class to analyze resume text using Groq API and prompt templates."""
    
    def __init__(self, groq_handler, prompt_loader):
        """Initialize ResumeAnalyzer with Groq handler and prompt loader.
        
        Args:
            groq_handler: Instance of GroqHandler for API interactions
            prompt_loader: Instance of PromptLoader for prompt management
        """
        # Store Groq handler instance
        self.grok = groq_handler
        # Store prompt loader instance
        self.prompt_loader = prompt_loader

    def analyze_resume(self, text, designation, experience, domain):
        """Analyze resume text based on specified parameters.
        
        Args:
            text (str): Resume text to analyze
            designation (str): Target job designation
            experience (str): Expected experience level
            domain (str): Industry or domain context
            
        Returns:
            str: Analysis result from Groq API
        """
        # Get formatted prompt using prompt loader
        prompt = self.prompt_loader.get_prompt(
            "resume_analysis",
            designation=designation,
            experience=experience,
            domain=domain
        )
        # Analyze text using Groq handler with prompt and text
        result = self.grok.analyze_text(prompt, text, max_tokens=1500)
        # Return the analysis result
        return result