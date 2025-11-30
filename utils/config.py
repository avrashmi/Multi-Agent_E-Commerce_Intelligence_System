"""
Configuration Management
========================
Handles API setup, model selection, and system settings.

This file manages:
- API key configuration
- Model selection (auto-detects best free model)
- Rate limiting settings
- Global configuration
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Global configuration class for the multi-agent system.
    
    This class handles:
    1. API authentication
    2. Model selection (finds best free tier model)
    3. Rate limiting configuration
    4. File paths
    """
    
    # ============================================
    # API Configuration
    # ============================================
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_api_key_here")
    MODEL_NAME = None  # Will be auto-detected
    
    # ============================================
    # Rate Limiting (Free Tier Optimization)
    # ============================================
    
    # Tracks number of API calls made
    API_CALLS_MADE = 0
    
    # Free tier allows ~15 requests per minute
    MAX_CALLS_PER_MINUTE = 15
    
    # Delay between API calls (4 seconds = 15 calls/minute)
    CALL_DELAY = 4
    
    # Auto-retry delay when rate limit is hit
    RATE_LIMIT_RETRY_DELAY = 60
    
    # ============================================
    # Data Paths
    # ============================================
    
    PRODUCTS_FILE = "data/products.csv"
    REVIEWS_FILE = "data/reviews.csv"
    INVENTORY_FILE = "data/inventory.csv"
    
    # ============================================
    # Agent Settings
    # ============================================
    
    # How many reviews to process per API call (batching)
    SENTIMENT_BATCH_SIZE = 3
    
    # Maximum tokens in API response
    MAX_OUTPUT_TOKENS = 300
    
    # Temperature for creative responses (0-1)
    TEMPERATURE = 0.7
    
    # ============================================
    # Methods
    # ============================================
    
    @classmethod
    def setup_api(cls) -> bool:
        """
        Initialize Gemini API and auto-select best model.
        
        Process:
        1. Validate API key
        2. Configure Gemini API
        3. List available models
        4. Select best free-tier model
        5. Return success status
        
        Returns:
            bool: True if setup successful, False otherwise
        """
        
        # Check if API key is set
        if cls.GEMINI_API_KEY == "your_api_key_here" or not cls.GEMINI_API_KEY:
            print("❌ GEMINI_API_KEY not set!")
            print("Please set it in one of these ways:")
            print("  1. Create .env file with: GEMINI_API_KEY=your_key")
            print("  2. Set environment variable: export GEMINI_API_KEY=your_key")
            print("\nGet your key from: https://aistudio.google.com/app/apikey")
            return False
        
        try:
            # Configure Gemini API
            genai.configure(api_key=cls.GEMINI_API_KEY)
            print("✅ API Key configured")
            
            # Find available models
            print("\n🔍 Detecting available models...\n")
            working_models = []
            
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    model_name = model.name.replace('models/', '')
                    print(f"   ✓ {model_name}")
                    working_models.append(model_name)
            
            if not working_models:
                print("❌ No models found. Check your API key permissions.")
                return False
            
            # Select best free-tier model
            cls.MODEL_NAME = cls._select_best_model(working_models)
            
            print(f"\n✅ Selected model: {cls.MODEL_NAME}")
            
            # Show rate limit info
            cls._show_rate_limit_info()
            
            return True
            
        except Exception as e:
            print(f"❌ API setup failed: {str(e)}")
            return False
    
    @classmethod
    def _select_best_model(cls, available_models: list) -> str:
        """
        Select the best model for free tier usage.
        
        Priority:
        1. gemini-1.5-flash-8b (best for free tier)
        2. gemini-1.5-flash
        3. gemini-1.0-pro
        4. Any non-preview model
        5. First available model
        
        Args:
            available_models: List of available model names
            
        Returns:
            str: Selected model name
        """
        
        # Priority list (best to worst for free tier)
        free_tier_priority = [
            'gemini-1.5-flash-8b',
            'gemini-1.5-flash',
            'gemini-1.0-pro',
        ]
        
        # Try priority models first
        for preferred in free_tier_priority:
            if preferred in available_models:
                return preferred
        
        # Avoid preview models (they have stricter limits)
        for model in available_models:
            if 'preview' not in model.lower() and 'pro' not in model.lower():
                return model
        
        # Last resort: use first available
        return available_models[0]
    
    @classmethod
    def _show_rate_limit_info(cls):
        """Display rate limit information for the selected model."""
        
        model_lower = cls.MODEL_NAME.lower()
        
        if 'flash-8b' in model_lower or 'flash' in model_lower:
            print("💡 Using Flash model - Great for free tier!")
            print(f"   Rate limit: ~{cls.MAX_CALLS_PER_MINUTE} requests/minute")
            print(f"   Delay between calls: {cls.CALL_DELAY} seconds")
        elif 'preview' in model_lower:
            print("⚠️ Preview model detected - Stricter rate limits")
            print("   Consider switching to gemini-1.5-flash if available")
        else:
            print(f"   Rate limit: ~{cls.MAX_CALLS_PER_MINUTE} requests/minute")
    
    @classmethod
    def reset_api_counter(cls):
        """Reset API call counter (useful for testing)."""
        cls.API_CALLS_MADE = 0
        print("🔄 API call counter reset")
    
    @classmethod
    def get_stats(cls) -> dict:
        """
        Get current configuration statistics.
        
        Returns:
            dict: Configuration statistics
        """
        return {
            "model": cls.MODEL_NAME,
            "api_calls_made": cls.API_CALLS_MADE,
            "max_calls_per_minute": cls.MAX_CALLS_PER_MINUTE,
            "call_delay": cls.CALL_DELAY,
            "batch_size": cls.SENTIMENT_BATCH_SIZE
        }
    
    @classmethod
    def display_config(cls):
        """Display current configuration."""
        print("\n" + "="*60)
        print("SYSTEM CONFIGURATION")
        print("="*60)
        print(f"Model: {cls.MODEL_NAME}")
        print(f"API Calls Made: {cls.API_CALLS_MADE}")
        print(f"Rate Limit: {cls.MAX_CALLS_PER_MINUTE} calls/minute")
        print(f"Call Delay: {cls.CALL_DELAY} seconds")
        print(f"Batch Size: {cls.SENTIMENT_BATCH_SIZE} reviews/call")
        print("="*60 + "\n")


# ============================================
# Auto-initialize on import (optional)
# ============================================

def initialize():
    """
    Initialize configuration.
    Call this at the start of your application.
    """
    success = Config.setup_api()
    if success:
        print("\n✅ Configuration initialized successfully!\n")
    else:
        print("\n❌ Configuration failed. Please check your API key.\n")
    return success


if __name__ == "__main__":
    # Test configuration when run directly
    print("Testing Configuration...\n")
    initialize()
    Config.display_config()