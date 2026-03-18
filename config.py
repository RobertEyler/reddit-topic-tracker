"""
Configuration Management Module
Handles loading and validating environment variable configurations
"""

import os
from dotenv import load_dotenv


class Config:
    """Configuration class for managing application settings"""
    
    def __init__(self):
        """Initialize configuration by loading settings from environment variables"""
        # Load .env file
        load_dotenv()
        
        # Reddit API credentials
        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.user_agent = os.getenv('REDDIT_USER_AGENT')
        
        # Validate required configuration
        self._validate()
    
    def _validate(self):
        """Validate that all required configuration settings are present"""
        missing = []
        
        if not self.client_id:
            missing.append('REDDIT_CLIENT_ID')
        if not self.client_secret:
            missing.append('REDDIT_CLIENT_SECRET')
        if not self.user_agent:
            missing.append('REDDIT_USER_AGENT')
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                f"Please create a .env file and set these variables. See .env.example for reference."
            )
    
    def __repr__(self):
        """Return string representation of configuration (hiding sensitive information)"""
        return (
            f"Config(client_id={'*' * 8}, "
            f"client_secret={'*' * 8}, "
            f"user_agent={self.user_agent})"
        )


# Create global configuration instance
def get_config():
    """Get configuration instance"""
    return Config()
