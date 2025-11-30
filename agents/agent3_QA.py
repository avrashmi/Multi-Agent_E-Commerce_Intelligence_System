"""
Agent 3: Question Answering Agent
==================================

Purpose:
    Provides intelligent answers to customer questions about products.

Technique:
    - Sequential Agent: Depends on Agent 1 and Agent 2
    - AI Reasoning: Uses Gemini to synthesize comprehensive answers
    - Context Integration: Combines product data + review insights

How it works:
    1. Receives user question
    2. Gets product details (from Agent 1)
    3. Gets review analysis (from Agent 2)
    4. Creates comprehensive prompt with all context
    5. Sends to Gemini for intelligent reasoning
    6. Returns helpful, honest answer

Why sequential:
    - Cannot answer without product data (needs Agent 1)
    - Cannot answer without review insights (needs Agent 2)
    - Builds on previous agents' work
    - Creates contextual, well-informed responses

Example flow:
    User: "Is this good for video editing?"
    → Agent 1 finds: Gaming Laptop Pro
    → Agent 2 says: 85% positive, "great performance"
    → Agent 3 answers: "Yes, based on 156 reviews (85% positive)..."

Logic:
    Question + Product + Sentiment → AI Synthesis → Intelligent Answer
"""

from typing import Dict, Any
from utils.api_helper import call_gemini


class QAAgent:
    """
    Agent 3: Question Answering using Sequential AI Reasoning
    """
    
    def __init__(self):
        """Initialize Q/A agent."""
        print("✅ Agent 3: Q/A (Sequential - depends on Agent 1 & 2)")
    
    def answer_question(
        self, 
        query: str, 
        product: Dict, 
        sentiment: Dict
    ) -> str:
        """
        Generate intelligent answer to user question.
        
        Process (Sequential):
        1. Receive question from user
        2. Receive product data from Agent 1
        3. Receive sentiment data from Agent 2
        4. Compile comprehensive context
        5. Create detailed prompt for Gemini
        6. Get AI-generated answer
        7. Apply fallback if API fails
        8. Return helpful response
        
        Args:
            query (str): User's question
            product (Dict): Product information from Agent 1
            sentiment (Dict): Review analysis from Agent 2
        
        Returns:
            str: Intelligent, contextual answer
        
        Example:
            >>> agent = QAAgent()
            >>> answer = agent.answer_question(
            ...     "Is this laptop good for gaming?",
            ...     product_data,
            ...     sentiment_data
            ... )
            >>> print(answer)
            "Yes, based on 156 reviews (85% positive)..."
        """
        
        print(f"\n🤔 Agent 3: Generating answer for '{query[:50]}...'")
        
        # Prepare context from previous agents
        context = self._prepare_context(product, sentiment)
        
        # Create comprehensive prompt
        prompt = self._create_prompt(query, context)
        
        # Get answer from Gemini
        answer = call_gemini(prompt, temperature=0.7)
        
        # Fallback if API fails
        if not answer:
            answer = self._generate_fallback_answer(query, product, sentiment)
        
        print(f"✅ Agent 3: Answer generated")
        
        return answer
    
    def _prepare_context(self, product: Dict, sentiment: Dict) -> Dict[str, Any]:
        """
        Prepare context from product and sentiment data.
        
        Args:
            product (Dict): Product information
            sentiment (Dict): Sentiment analysis
        
        Returns:
            Dict: Organized context for prompting
        """
        
        # Product context
        product_info = {
            'name': product.get('title', 'Unknown'),
            'description': product.get('description', 'No description'),
            'price': product.get('price', 0),
            'category': product.get('category', 'General'),
            'stock': product.get('stock', 0),
            'stock_status': product.get('stock_status', 'Unknown')
        }
        
        # Sentiment context
        sentiment_info = {
            'total_reviews': sentiment.get('total_reviews', 0),
            'avg_rating': sentiment.get('avg_rating', 0),
            'positive_percent': sentiment.get('positive_percent', 0),
            'negative_percent': sentiment.get('negative_percent', 0),
            'overall_sentiment': sentiment.get('sentiment', 'Unknown'),
            'pros': sentiment.get('pros', []),
            'cons': sentiment.get('cons', [])
        }
        
        return {
            'product': product_info,
            'sentiment': sentiment_info
        }
    
    def _create_prompt(self, query: str, context: Dict) -> str:
        """
        Create comprehensive prompt for Gemini.
        
        Args:
            query (str): User question
            context (Dict): Compiled context
        
        Returns:
            str: Detailed prompt for AI
        """
        
        product = context['product']
        sentiment = context['sentiment']
        
        # Format pros and cons
        pros_text = ', '.join(sentiment['pros']) if sentiment['pros'] else 'Not mentioned in reviews'
        cons_text = ', '.join(sentiment['cons']) if sentiment['cons'] else 'Not mentioned in reviews'
        
        # Stock information
        stock_info = f"{product['stock']} units available" if product['stock'] > 0 else "Currently out of stock"
        
        prompt = f"""You are an expert e-commerce assistant helping customers make informed decisions.

**Customer Question:** {query}

**Product Information:**
- Name: {product['name']}
- Description: {product['description']}
- Price: ${product['price']}
- Category: {product['category']}
- Stock: {stock_info}

**Customer Review Analysis:**
- Total Reviews: {sentiment['total_reviews']}
- Average Rating: {sentiment['avg_rating']}/5 stars
- Overall Sentiment: {sentiment['overall_sentiment']}
- Positive Reviews: {sentiment['positive_percent']}%
- Negative Reviews: {sentiment['negative_percent']}%
- Common Pros: {pros_text}
- Common Cons: {cons_text}

**Instructions:**
1. Answer the customer's question directly and honestly
2. Use the review data to support your answer
3. Mention both strengths AND weaknesses if relevant
4. Keep your answer concise (2-3 sentences)
5. Be helpful and build trust with accurate information

**Your Answer:**"""
        
        return prompt
    
    def _generate_fallback_answer(
        self, 
        query: str, 
        product: Dict, 
        sentiment: Dict
    ) -> str:
        """
        Generate fallback answer if API fails.
        
        Args:
            query (str): User question
            product (Dict): Product data
            sentiment (Dict): Sentiment data
        
        Returns:
            str: Basic fallback answer
        """
        
        name = product.get('title', 'this product')
        reviews = sentiment.get('total_reviews', 0)
        positive = sentiment.get('positive_percent', 0)
        price = product.get('price', 0)
        rating = sentiment.get('avg_rating', 0)
        
        # Generate basic answer
        if reviews > 0:
            if positive >= 70:
                quality = "well-received"
            elif positive >= 50:
                quality = "generally positive"
            else:
                quality = "mixed"
            
            answer = f"Based on {reviews} customer reviews ({positive}% positive, {rating}/5 stars), {name} is {quality}. It's priced at ${price}."
        else:
            answer = f"{name} is priced at ${price}. However, there are no customer reviews available yet."
        
        # Add stock warning if needed
        if product.get('stock', 0) == 0:
            answer += " Note: This item is currently out of stock."
        
        return answer
    
    def answer_comparison(
        self, 
        product1: Dict, 
        sentiment1: Dict,
        product2: Dict,
        sentiment2: Dict
    ) -> str:
        """
        Compare two products and provide recommendation.
        
        Args:
            product1 (Dict): First product data
            sentiment1 (Dict): First product sentiment
            product2 (Dict): Second product data
            sentiment2 (Dict): Second product sentiment
        
        Returns:
            str: Comparison and recommendation
        """
        
        prompt = f"""Compare these two products and recommend which one is better:

**Product 1: {product1.get('title')}**
- Price: ${product1.get('price')}
- Reviews: {sentiment1.get('total_reviews')} ({sentiment1.get('positive_percent')}% positive)
- Rating: {sentiment1.get('avg_rating')}/5
- Pros: {', '.join(sentiment1.get('pros', []))}
- Cons: {', '.join(sentiment1.get('cons', []))}

**Product 2: {product2.get('title')}**
- Price: ${product2.get('price')}
- Reviews: {sentiment2.get('total_reviews')} ({sentiment2.get('positive_percent')}% positive)
- Rating: {sentiment2.get('avg_rating')}/5
- Pros: {', '.join(sentiment2.get('pros', []))}
- Cons: {', '.join(sentiment2.get('cons', []))}

Provide a brief comparison (2-3 sentences) and recommend which one to choose."""
        
        answer = call_gemini(prompt, temperature=0.7)
        
        if not answer:
            # Fallback comparison
            if sentiment1.get('positive_percent', 0) > sentiment2.get('positive_percent', 0):
                answer = f"{product1.get('title')} has better reviews ({sentiment1.get('positive_percent')}% positive vs {sentiment2.get('positive_percent')}%)."
            else:
                answer = f"{product2.get('title')} has better reviews ({sentiment2.get('positive_percent')}% positive vs {sentiment1.get('positive_percent')}%)."
        
        return answer


# ============================================
# Testing
# ============================================

if __name__ == "__main__":
    print("Testing Q/A Agent...\n")
    
    # Sample data
    test_product = {
        "title": "Gaming Laptop Pro",
        "description": "High-performance laptop",
        "price": 1299.99,
        "category": "Laptops",
        "stock": 15
    }
    
    test_sentiment = {
        "total_reviews": 156,
        "avg_rating": 4.5,
        "positive_percent": 85,
        "negative_percent": 10,
        "sentiment": "Positive",
        "pros": ["great performance", "fast"],
        "cons": ["gets hot"]
    }
    
    # Initialize agent
    agent = QAAgent()
    
    print("Note: Full testing requires API configuration")
    print("Agent initialized and ready")