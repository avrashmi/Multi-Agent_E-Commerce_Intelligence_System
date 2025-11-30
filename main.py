"""
Multi-Agent E-Commerce System - Main Orchestrator
==================================================

This is the main entry point that coordinates all 4 agents:
1. Product Retrieval Agent (Search)
2. Sentiment Analysis Agent (Review Analysis)
3. Q/A Agent (Answer Questions)
4. Recommendation Agent (Suggest Alternatives)

Workflow:
    User Query
        ↓
    Agent 1: Find relevant products
        ↓
    Agent 2: Analyze reviews
        ↓
    Agent 3: Generate answer
        ↓
    Agent 4: Check for alternatives
        ↓
    Final Response

Usage:
    python main.py
"""

from typing import Dict, Any
from agents import (
    ProductRetrievalAgent,
    SentimentAgent,
    QAAgent,
    RecommendationAgent
)
#from .utils import Config, load_data, display_data_summary
from utils.config import Config
from utils.data_loader import load_data, display_data_summary


class MultiAgentSystem:
    """
    Multi-Agent Orchestrator
    
    Coordinates all 4 agents to process user queries in sequence.
    """
    
    def __init__(self, products, reviews):
        """
        Initialize the multi-agent system.
        
        Args:
            products: List of product dictionaries
            reviews: List of review dictionaries
        """
        print("\n" + "="*60)
        print("🚀 INITIALIZING MULTI-AGENT SYSTEM")
        print("="*60 + "\n")
        
        # Initialize all agents
        self.agent1 = ProductRetrievalAgent(products)
        self.agent2 = SentimentAgent(reviews)
        self.agent3 = QAAgent()
        self.agent4 = RecommendationAgent(products)
        
        self.products = products
        self.reviews = reviews
        
        print("\n" + "="*60)
        print("✅ ALL AGENTS INITIALIZED")
        print("="*60 + "\n")
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """
        Process user query through all agents sequentially.
        
        Sequential Workflow:
        1. Agent 1: Search for relevant products
        2. Agent 2: Analyze product reviews
        3. Agent 3: Generate intelligent answer
        4. Agent 4: Check for better alternatives
        5. Compile and return final result
        
        Args:
            user_query (str): User's question or search query
        
        Returns:
            Dict: Complete result with product, sentiment, answer, recommendation
        """
        
        print("\n" + "="*60)
        print(f"📝 PROCESSING QUERY: {user_query}")
        print("="*60)
        
        try:
            # Step 1: Agent 1 - Find relevant products
            products = self.agent1.retrieve_products(user_query, top_k=1)
            
            if not products:
                return {
                    "error": "No products found",
                    "query": user_query
                }
            
            top_product = products[0]
            
            # Step 2: Agent 2 - Analyze sentiment
            sentiment = self.agent2.analyze_reviews(top_product['product_id'])
            
            # Step 3: Agent 3 - Generate answer
            answer = self.agent3.answer_question(user_query, top_product, sentiment)
            
            # Step 4: Agent 4 - Get recommendation
            recommendation = self.agent4.recommend_alternative(
                top_product,
                sentiment,
                self.products
            )
            
            # Compile final result
            result = {
                "query": user_query,
                "product": {
                    "id": top_product['product_id'],
                    "name": top_product['title'],
                    "description": top_product['description'],
                    "price": top_product['price'],
                    "category": top_product['category'],
                    "stock": top_product.get('stock', 0),
                    "stock_status": top_product.get('stock_status', 'Unknown'),
                    "relevance_score": top_product.get('relevance_score', 0)
                },
                "sentiment_analysis": sentiment,
                "answer": answer,
                "recommendation": recommendation
            }
            
            return result
        
        except Exception as e:
            print(f"\n❌ Error processing query: {str(e)}")
            return {
                "error": str(e),
                "query": user_query
            }
    
    def display_result(self, result: Dict):
        """
        Display results in a formatted, user-friendly way.
        
        Args:
            result (Dict): Result from process_query
        """
        
        if "error" in result:
            print(f"\n❌ Error: {result['error']}")
            return
        
        print("\n" + "="*60)
        print("📊 FINAL RESULT")
        print("="*60)
        
        # Product Information
        product = result['product']
        print(f"\n🎯 Product: {product['name']}")
        print(f"📁 Category: {product['category']}")
        print(f"💰 Price: ${product['price']}")
        print(f"📦 Stock: {product['stock_status']} ({product['stock']} units)")
        print(f"🎲 Relevance Score: {product['relevance_score']:.1f}")
        
        # Review Analysis
        sentiment = result['sentiment_analysis']
        print(f"\n📊 Review Analysis:")
        print(f"   ⭐ {sentiment['total_reviews']} reviews | {sentiment['avg_rating']}/5 stars")
        print(f"   📈 {sentiment['positive_percent']}% positive")
        print(f"   📉 {sentiment['negative_percent']}% negative")
        print(f"   🎯 Overall: {sentiment['sentiment']}")
        
        if sentiment['pros']:
            print(f"\n   ✅ Pros:")
            for pro in sentiment['pros']:
                print(f"      • {pro}")
        
        if sentiment['cons']:
            print(f"\n   ⚠️ Cons:")
            for con in sentiment['cons']:
                print(f"      • {con}")
        
        # Answer
        print(f"\n💬 Answer:")
        print(f"   {result['answer']}")
        
        # Recommendation
        rec = result['recommendation']
        print(f"\n{rec['message']}")
        
        if rec['needs_alternative'] and rec.get('product'):
            alt = rec['product']
            print(f"   Alternative: {alt['title']} (${alt['price']})")
        
        print("\n" + "="*60 + "\n")
    
    def get_system_stats(self) -> Dict:
        """Get statistics about the system."""
        return {
            "products": len(self.products),
            "reviews": len(self.reviews),
            "agent1_stats": self.agent1.get_stats(),
            "agent2_memory": self.agent2.get_memory_stats(),
            "agent4_stats": self.agent4.get_stats()
        }


def main():
    """Main execution function."""
    
    print("\n" + "="*60)
    print("  MULTI-AGENT E-COMMERCE SYSTEM")
    print("  Powered by 4 Specialized AI Agents")
    print("="*60)
    
    # Step 1: Initialize configuration and API
    print("\n📋 Step 1: Initializing configuration...")
    if not Config.setup_api():
        print("\n❌ Setup failed. Please check your API key.")
        return
    
    # Step 2: Load data
    print("\n📋 Step 2: Loading data...")
    products, reviews = load_data(use_sample=True)
    
    if not products:
        print("❌ No products loaded. Exiting.")
        return
    
    display_data_summary(products, reviews)
    
    # Step 3: Initialize multi-agent system
    print("\n📋 Step 3: Initializing agents...")
    system = MultiAgentSystem(products, reviews)
    
    # Step 4: Run test queries
    print("\n📋 Step 4: Running test queries...")
    
    '''test_queries = [
        "Is this laptop good for video editing?",
        "I need a phone for gaming",
        "What's a good budget laptop for office work?",
    ]'''

    test_queries = [
        "Are these earbuds great for noise cancellation?",
        "Does this laptop sleeve protect the laptop well?",
        "Is this smartwatch accurate and reliable?",
    ]


    """
product_id	title	Positive Prompt	Mixed Prompt	Negative Prompt
1	Wireless Earbuds	“Are these earbuds great for noise cancellation?”	“Do these earbuds work well but have minor issues?”	“Do these earbuds have poor sound or fit?”
2	Smartwatch Pro	“Is this smartwatch accurate and reliable?”	“Is the smartwatch good but battery drains fast?”	“Does this smartwatch have poor battery life?”
3	Laptop Sleeve 15	“Does this laptop sleeve protect the laptop well?”	“Is the laptop sleeve okay but stitching or fit is average?”	“Is the sleeve poorly made or doesn’t fit?”
4	Mechanical Keyboard	“Is this keyboard comfortable and responsive?”	“Is the keyboard good but some keys stop working?”	“Is the keyboard too noisy or low quality?
"""
    
    for query in test_queries:
        result = system.process_query(query)
        system.display_result(result)
        
        # Small delay between queries
        import time
        time.sleep(2)
    
    # Step 5: Display system stats
    print("\n📊 SYSTEM STATISTICS")
    print("="*60)
    stats = system.get_system_stats()
    print(f"Products: {stats['products']}")
    print(f"Reviews: {stats['reviews']}")
    print(f"Agent 2 Memory: {stats['agent2_memory']['cached_products']} products cached")
    print("="*60)
    
    # Step 6: Interactive mode
    print("\n✅ System ready for interactive use!")
    print("You can now use the system programmatically:")
    print("  result = system.process_query('your question')")
    print("  system.display_result(result)")
    print("\nOr run specific test:")
    print("  python main.py")


def interactive_mode():
    """
    Interactive mode for asking questions.
    
    Usage:
        from main import interactive_mode
        interactive_mode()
    """
    
    # Initialize
    Config.setup_api()
    products, reviews = load_data(use_sample=True)
    system = MultiAgentSystem(products, reviews)
    
    print("\n" + "="*60)
    print("🎮 INTERACTIVE MODE")
    print("="*60)
    print("Type your questions (or 'quit' to exit)")
    print("="*60 + "\n")
    
    while True:
        try:
            query = input("\n💬 Your question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not query:
                continue
            
            result = system.process_query(query)
            system.display_result(result)
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()