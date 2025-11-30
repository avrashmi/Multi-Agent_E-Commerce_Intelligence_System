"""
API Helper
==========
Safe wrapper for Gemini API calls with rate limiting and error handling.

This module provides:
- Rate-limited API calls
- Automatic retry on rate limit
- Error handling
- Progress indicators
"""

import time
import google.generativeai as genai
from .config import Config


def call_gemini(prompt: str, temperature: float = None, max_tokens: int = None) -> str:
    """
    Safe wrapper for Gemini API calls with rate limiting.
    
    Features:
    - Automatic rate limiting (respects free tier limits)
    - Auto-retry on 429 errors
    - Error handling with fallbacks
    - Progress indicators
    
    Process:
    1. Wait if needed (rate limiting)
    2. Call Gemini API
    3. Handle errors (429, 404, etc.)
    4. Return response or empty string
    
    Args:
        prompt (str): The prompt to send to Gemini
        temperature (float, optional): Creativity level (0-1). 
                                      Defaults to Config.TEMPERATURE
        max_tokens (int, optional): Maximum response tokens.
                                   Defaults to Config.MAX_OUTPUT_TOKENS
    
    Returns:
        str: Response from Gemini, or empty string on error
    
    Example:
        >>> response = call_gemini("Explain quantum physics in one sentence")
        >>> print(response)
        "Quantum physics describes the behavior of matter and energy..."
    """
    
    # Use defaults from Config if not specified
    if temperature is None:
        temperature = Config.TEMPERATURE
    
    if max_tokens is None:
        max_tokens = Config.MAX_OUTPUT_TOKENS
    
    try:
        # ============================================
        # Rate Limiting
        # ============================================
        
        if Config.API_CALLS_MADE > 0:
            # Show progress indicator
            print(f"⏳ Rate limit delay ({Config.CALL_DELAY}s)...", end='\r')
            time.sleep(Config.CALL_DELAY)
            # Clear the line
            print(" " * 50, end='\r')
        
        # ============================================
        # Make API Call
        # ============================================
        
        model = genai.GenerativeModel(Config.MODEL_NAME)
        
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': temperature,
                'max_output_tokens': max_tokens,
            }
        )
        
        # Increment counter
        Config.API_CALLS_MADE += 1
        
        # Return response text
        return response.text.strip()
    
    except Exception as e:
        error_msg = str(e)
        
        # ============================================
        # Error Handling
        # ============================================
        
        # Handle 429: Rate Limit Exceeded
        if '429' in error_msg:
            print(f"\n⚠️ Rate limit hit! Waiting {Config.RATE_LIMIT_RETRY_DELAY}s...")
            time.sleep(Config.RATE_LIMIT_RETRY_DELAY)
            Config.API_CALLS_MADE = 0
            
            # Retry once
            try:
                print("🔄 Retrying API call...")
                response = model.generate_content(
                    prompt,
                    generation_config={
                        'temperature': temperature,
                        'max_output_tokens': max_tokens,
                    }
                )
                print("✅ Retry successful")
                return response.text.strip()
            except Exception as retry_error:
                print(f"❌ Retry failed: {str(retry_error)[:100]}")
                return ""
        
        # Handle 404: Model Not Found
        elif '404' in error_msg:
            print(f"\n❌ Model '{Config.MODEL_NAME}' not found!")
            print("Please run Config.setup_api() to refresh model list")
            return ""
        
        # Handle 403: Permission Denied
        elif '403' in error_msg:
            print(f"\n❌ API key permission denied!")
            print("Check your API key at: https://aistudio.google.com/app/apikey")
            return ""
        
        # Handle other errors
        else:
            print(f"\n⚠️ API Error: {error_msg[:100]}")
            return ""


def call_gemini_batch(prompts: list, temperature: float = None) -> list:
    """
    Call Gemini API for multiple prompts (with rate limiting).
    
    Useful for processing multiple items while respecting rate limits.
    
    Args:
        prompts (list): List of prompts to process
        temperature (float, optional): Creativity level
    
    Returns:
        list: List of responses (same order as prompts)
    
    Example:
        >>> prompts = ["Explain AI", "Explain ML", "Explain DL"]
        >>> responses = call_gemini_batch(prompts)
        >>> for prompt, response in zip(prompts, responses):
        ...     print(f"Q: {prompt}\nA: {response}\n")
    """
    
    responses = []
    total = len(prompts)
    
    print(f"\n🔄 Processing {total} prompts...")
    
    for i, prompt in enumerate(prompts, 1):
        print(f"   [{i}/{total}] Processing...", end='\r')
        response = call_gemini(prompt, temperature=temperature)
        responses.append(response)
    
    print(f"✅ Completed {total} API calls" + " " * 20)
    
    return responses


def test_api_connection() -> bool:
    """
    Test if API connection is working.
    
    Returns:
        bool: True if API is working, False otherwise
    
    Example:
        >>> if test_api_connection():
        ...     print("API is ready!")
    """
    
    print("🧪 Testing API connection...")
    
    test_prompt = "Say 'API is working!' and nothing else."
    response = call_gemini(test_prompt, temperature=0.1)
    
    if response:
        print(f"✅ API Test Result: {response}")
        return True
    else:
        print("❌ API test failed")
        print("Please check:")
        print("  1. API key is correct")
        print("  2. API key has quota remaining")
        print("  3. Model is available")
        return False


def get_api_stats() -> dict:
    """
    Get current API usage statistics.
    
    Returns:
        dict: API statistics including calls made, rate limit, etc.
    
    Example:
        >>> stats = get_api_stats()
        >>> print(f"API calls made: {stats['calls_made']}")
    """
    
    stats = Config.get_stats()
    
    # Add estimated time remaining until rate limit reset
    calls_remaining = Config.MAX_CALLS_PER_MINUTE - Config.API_CALLS_MADE
    estimated_time = calls_remaining * Config.CALL_DELAY
    
    stats['calls_remaining'] = calls_remaining
    stats['estimated_time_to_limit'] = f"{estimated_time}s"
    
    return stats


def display_api_stats():
    """
    Display formatted API usage statistics.
    
    Example:
        >>> display_api_stats()
        API STATISTICS
        ====================
        Calls Made: 5
        Calls Remaining: 10
        ...
    """
    
    stats = get_api_stats()
    
    print("\n" + "="*50)
    print("API STATISTICS")
    print("="*50)
    print(f"Model: {stats['model']}")
    print(f"Calls Made: {stats['api_calls_made']}")
    print(f"Calls Remaining: {stats['calls_remaining']}")
    print(f"Rate Limit: {stats['max_calls_per_minute']} calls/minute")
    print(f"Delay Between Calls: {stats['call_delay']}s")
    print(f"Time to Limit: {stats['estimated_time_to_limit']}")
    print("="*50 + "\n")


def reset_api_stats():
    """
    Reset API call counter.
    
    Useful for testing or when starting a new session.
    
    Example:
        >>> reset_api_stats()
        🔄 API statistics reset
    """
    
    Config.reset_api_counter()


# ============================================
# Utility Functions
# ============================================

def safe_api_call(prompt: str, fallback: str = "", **kwargs) -> str:
    """
    Make API call with guaranteed fallback.
    
    If API fails, returns fallback value instead of empty string.
    
    Args:
        prompt (str): Prompt to send
        fallback (str): Value to return if API fails
        **kwargs: Additional arguments for call_gemini
    
    Returns:
        str: API response or fallback value
    
    Example:
        >>> response = safe_api_call(
        ...     "Explain AI",
        ...     fallback="AI is artificial intelligence."
        ... )
    """
    
    response = call_gemini(prompt, **kwargs)
    
    if not response:
        return fallback
    
    return response


def wait_for_rate_limit():
    """
    Manually wait for rate limit to reset.
    
    Use this if you need to make many calls and want to ensure
    you don't hit the rate limit.
    
    Example:
        >>> for i in range(20):
        ...     if i % 10 == 0:
        ...         wait_for_rate_limit()
        ...     call_gemini("Process item")
    """
    
    print(f"\n⏸️ Waiting {Config.RATE_LIMIT_RETRY_DELAY}s for rate limit reset...")
    time.sleep(Config.RATE_LIMIT_RETRY_DELAY)
    Config.API_CALLS_MADE = 0
    print("✅ Rate limit reset complete\n")


# ============================================
# Testing
# ============================================

if __name__ == "__main__":
    # Test the API helper
    print("Testing API Helper Module...\n")
    
    # Import config
    from config import initialize
    
    # Initialize
    if initialize():
        # Test API
        test_api_connection()
        
        # Show stats
        display_api_stats()
        
        # Test a simple call
        print("\n🧪 Testing simple API call...")
        response = call_gemini("What is 2+2? Answer with just the number.")
        print(f"Response: {response}")
        
        # Show updated stats
        display_api_stats()