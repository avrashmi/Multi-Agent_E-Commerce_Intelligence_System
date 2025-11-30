"""
Agent 2: Sentiment Analysis Agent
==================================

Purpose:
    Analyzes customer reviews to extract sentiment, pros, and cons.

Techniques:
    - Loop Agent: Processes multiple reviews
    - Batch Processing: Groups reviews to reduce API calls
    - Memory System: Caches results to avoid re-processing

How it works:
    1. Gets all reviews for a product
    2. Checks memory cache first
    3. Batches reviews (3 at a time) to save API calls
    4. Sends batch to Gemini for sentiment analysis
    5. Parses sentiment, pros, and cons
    6. Calculates aggregate statistics
    7. Stores in memory for future queries
    8. Returns comprehensive summary

Why batching:
    - 9 reviews = 3 API calls instead of 9
    - Reduces rate limit issues by 66%
    - Faster overall processing
    - More efficient API usage

Memory system:
    - Once analyzed, results are cached
    - Future queries use cached data (instant)
    - No repeated API calls for same product

Logic:
    Batch → API Call → Parse → Aggregate → Cache → Return
"""

from typing import List, Dict, Any
from utils.api_helper import call_gemini
from utils.config import Config


class SentimentAgent:
    """
    Agent 2: Sentiment Analysis using Loop + Batch + Memory
    """
    
    def __init__(self, reviews: List[Dict]):
        """
        Initialize sentiment analysis agent.
        
        Args:
            reviews (List[Dict]): List of review dictionaries
        """
        self.reviews = reviews
        self.memory = {}  # Cache for analyzed products
        print("✅ Agent 2: Sentiment Analysis (Loop + Batch + Memory)")
    
    def analyze_reviews(self, product_id: str) -> Dict[str, Any]:
        """
        Analyze all reviews for a product using batch processing.
        
        Process:
        1. Check memory cache
        2. Get all reviews for product
        3. Batch reviews (3 per API call)
        4. Analyze each batch with Gemini
        5. Parse results
        6. Calculate statistics
        7. Cache results
        8. Return summary
        
        Args:
            product_id (str): Product ID to analyze
        
        Returns:
            Dict: Review analysis summary with sentiment, pros, cons
        
        Example:
            >>> agent = SentimentAgent(reviews)
            >>> result = agent.analyze_reviews("P001")
            >>> print(result['positive_percent'])
            85.5
        """
        
        # Check memory first (instant retrieval)
        if product_id in self.memory:
            print(f"💾 Agent 2: Retrieved from memory: {product_id}")
            return self.memory[product_id]
        
        # Get reviews for this product
        product_reviews = [
            r for r in self.reviews 
            if r.get('product_id') == int(product_id)
        ]
        
        # No reviews case
        if not product_reviews:
            return {
                "total_reviews": 0,
                "avg_rating": 0,
                "positive_percent": 0,
                "negative_percent": 0,
                "neutral_percent": 0,
                "sentiment": "No reviews",
                "pros": [],
                "cons": []
            }
        
        print(f"\n💬 Agent 2: Analyzing the total count of{len(product_reviews)} reviews for product_id{product_id}")
        
        # Initialize aggregators
        sentiments = []
        pros = []
        cons = []
        ratings = []
        
        # Batch processing (loop agent technique)
        batch_size = Config.SENTIMENT_BATCH_SIZE
        
        for i in range(0, len(product_reviews), batch_size):
            batch = product_reviews[i:i+batch_size]
            
            # Process this batch
            batch_result = self._analyze_batch(batch)
            
            # Aggregate results
            sentiments.extend(batch_result['sentiments'])
            pros.extend(batch_result['pros'])
            cons.extend(batch_result['cons'])
            ratings.extend(batch_result['ratings'])
        
        # Calculate final statistics
        result = self._calculate_statistics(
            sentiments, pros, cons, ratings, len(product_reviews)
        )
        
        # Store in memory (cache)
        self.memory[product_id] = result
        
        print(f"✅ Agent 2: Sentiment = {result['sentiment']} ({result['positive_percent']}% positive)")
        
        return result
    
    def _analyze_batch(self, batch: List[Dict]) -> Dict[str, List]:
        """
        Analyze a batch of reviews using Gemini API.
        
        Args:
            batch (List[Dict]): Batch of review dictionaries
        
        Returns:
            Dict: Parsed sentiments, pros, cons, ratings
        """
        
        # Create batch prompt
        batch_text = "\n\n".join([
            f"Review {j+1}:\n"
            f"Text: \"{review['review_text']}\"\n"
            f"Rating: {review['rating']}/5"
            for j, review in enumerate(batch)
        ])
        
        prompt = f"""Analyze these customer reviews. For EACH review, provide:
1. Sentiment: positive OR negative OR neutral
2. Pro: one positive point (or "none")
3. Con: one negative point (or "none")

{batch_text}

Format your response EXACTLY like this for each review:
Review 1:
Sentiment: positive
Pro: great performance
Con: none

Review 2:
Sentiment: negative
Pro: none
Con: expensive

Do this for all {len(batch)} reviews."""
        
        # Call Gemini API
        response = call_gemini(prompt, temperature=0.3)
        
        # Parse response
        sentiments = []
        pros = []
        cons = []
        ratings = []
        
        if response:
            # Parse the structured response
            parsed = self._parse_batch_response(response, len(batch))
            sentiments = parsed['sentiments']
            pros = parsed['pros']
            cons = parsed['cons']
        
        # Add ratings and fallback sentiments
        for review in batch:
            rating = review['rating']
            ratings.append(rating)
            
            # Fallback: if API didn't provide sentiment, use rating
            if len(sentiments) < len(ratings):
                if rating >= 4:
                    sentiments.append("positive")
                elif rating <= 2:
                    sentiments.append("negative")
                else:
                    sentiments.append("neutral")
        
        return {
            'sentiments': sentiments,
            'pros': pros,
            'cons': cons,
            'ratings': ratings
        }
    
    def _parse_batch_response(self, response: str, expected_count: int) -> Dict[str, List]:
        """
        Parse Gemini's structured response.
        
        Args:
            response (str): API response text
            expected_count (int): Number of reviews in batch
        
        Returns:
            Dict: Parsed sentiments, pros, cons
        """
        sentiments = []
        pros = []
        cons = []
        
        lines = response.lower().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Parse sentiment
            if 'sentiment:' in line:
                if 'positive' in line:
                    sentiments.append("positive")
                elif 'negative' in line:
                    sentiments.append("negative")
                elif 'neutral' in line:
                    sentiments.append("neutral")
            
            # Parse pros
            elif 'pro:' in line:
                parts = line.split('pro:', 1)
                if len(parts) > 1:
                    pro_text = parts[1].strip()
                    if pro_text and 'none' not in pro_text:
                        pros.append(pro_text)
            
            # Parse cons
            elif 'con:' in line:
                parts = line.split('con:', 1)
                if len(parts) > 1:
                    con_text = parts[1].strip()
                    if con_text and 'none' not in con_text:
                        cons.append(con_text)
        
        return {
            'sentiments': sentiments,
            'pros': pros,
            'cons': cons
        }
    
    def _calculate_statistics(
        self, 
        sentiments: List[str], 
        pros: List[str], 
        cons: List[str], 
        ratings: List[int],
        total_reviews: int
    ) -> Dict[str, Any]:
        """
        Calculate aggregate statistics from parsed reviews.
        
        Args:
            sentiments: List of sentiment labels
            pros: List of positive points
            cons: List of negative points
            ratings: List of rating values
            total_reviews: Total number of reviews
        
        Returns:
            Dict: Aggregate statistics
        """
        
        # Count sentiments
        total = len(sentiments)
        positive = sentiments.count("positive")
        negative = sentiments.count("negative")
        neutral = sentiments.count("neutral")
        
        # Calculate percentages
        pos_pct = round((positive / total) * 100, 1) if total > 0 else 0
        neg_pct = round((negative / total) * 100, 1) if total > 0 else 0
        neu_pct = round((neutral / total) * 100, 1) if total > 0 else 0
        
        # Overall sentiment
        if positive > negative and positive > neutral:
            overall = "Positive"
        elif negative > positive and negative > neutral:
            overall = "Negative"
        else:
            overall = "Mixed"
        
        # Average rating
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        return {
            "total_reviews": total_reviews,
            "avg_rating": round(avg_rating, 1),
            "positive_percent": pos_pct,
            "negative_percent": neg_pct,
            "neutral_percent": neu_pct,
            "sentiment": overall,
            "pros": pros[:3],  # Top 3 pros
            "cons": cons[:3]   # Top 3 cons
        }
    
    def get_reviews_for_product(self, product_id: str) -> List[Dict]:
        """
        Get all reviews for a specific product.
        
        Args:
            product_id (str): Product ID
        
        Returns:
            List[Dict]: List of reviews
        """
        return [r for r in self.reviews if r.get('product_id') == int(product_id)]
    
    def clear_memory(self):
        """Clear the memory cache."""
        self.memory = {}
        print("🔄 Agent 2: Memory cleared")
    
    def get_memory_stats(self) -> Dict:
        """
        Get memory statistics.
        
        Returns:
            Dict: Memory usage statistics
        """
        return {
            "cached_products": len(self.memory),
            "product_ids": list(self.memory.keys())
        }


# ============================================
# Testing
# ============================================

if __name__ == "__main__":
    print("Testing Sentiment Analysis Agent...\n")
    
    # Sample reviews
    test_reviews = [
        {"product_id": "P001", "review_text": "Amazing product!", "rating": 5},
        {"product_id": "P001", "review_text": "Good but expensive", "rating": 4},
        {"product_id": "P001", "review_text": "Love it!", "rating": 5},
    ]
    
    # Initialize agent
    agent = SentimentAgent(test_reviews)
    
    # Note: This test requires API setup
    print("Note: Full testing requires API configuration")
    print(f"Reviews loaded: {len(test_reviews)}")
    print(f"Memory stats: {agent.get_memory_stats()}")