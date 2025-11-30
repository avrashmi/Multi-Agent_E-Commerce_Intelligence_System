"""
Complete System Test
====================

Tests all components of the multi-agent system.

Run this after setting up to verify everything works.
"""

def test_phase1_utils():
    """Test Phase 1: Utils"""
    print("\n" + "="*60)
    print("🧪 TESTING PHASE 1: UTILS")
    print("="*60)
    
    try:
        from utils.config import Config, initialize
        from utils.api_helper import test_api_connection, get_api_stats
        from utils.data_loader import load_data, display_data_summary
        
        # Test 1: Configuration
        print("\n1️⃣ Testing Configuration...")
        if initialize():
            print("   ✅ Config initialized")
            Config.display_config()
        else:
            print("   ❌ Config failed")
            return False
        
        # Test 2: API Connection
        print("\n2️⃣ Testing API Connection...")
        if test_api_connection():
            print("   ✅ API working")
        else:
            print("   ❌ API failed")
            return False
        
        # Test 3: Data Loading
        print("\n3️⃣ Testing Data Loading...")
        products, reviews = load_data(use_sample=True)
        if products and reviews:
            print("   ✅ Data loaded")
            display_data_summary(products, reviews)
        else:
            print("   ❌ Data loading failed")
            return False
        
        print("\n✅ PHASE 1 PASSED")
        return True
    
    except Exception as e:
        print(f"\n❌ PHASE 1 FAILED: {str(e)}")
        return False


def test_phase2_agents():
    """Test Phase 2: Individual Agents"""
    print("\n" + "="*60)
    print("🧪 TESTING PHASE 2: AGENTS")
    print("="*60)
    
    try:
        from agents import (
            ProductRetrievalAgent,
            SentimentAgent,
            QAAgent,
            RecommendationAgent
        )
        from utils.data_loader import load_data
        
        # Load data
        products, reviews = load_data(use_sample=True)
        
        # Test Agent 1
        print("\n1️⃣ Testing Agent 1: Product Retrieval...")
        agent1 = ProductRetrievalAgent(products)
        results = agent1.retrieve_products("laptop gaming", top_k=2)
        if results:
            print(f"   ✅ Found {len(results)} products")
            print(f"   Top: {results[0]['title']}")
        else:
            print("   ❌ No products found")
            return False
        
        # Test Agent 2
        print("\n2️⃣ Testing Agent 2: Sentiment Analysis...")
        agent2 = SentimentAgent(reviews)
        sentiment = agent2.analyze_reviews(results[0]['product_id'])
        if sentiment:
            print(f"   ✅ Sentiment: {sentiment['sentiment']}")
            print(f"   Reviews: {sentiment['total_reviews']}")
        else:
            print("   ❌ Sentiment analysis failed")
            return False
        
        # Test Agent 3
        print("\n3️⃣ Testing Agent 3: Q/A...")
        agent3 = QAAgent()
        answer = agent3.answer_question(
            "Is this good?",
            results[0],
            sentiment
        )
        if answer:
            print(f"   ✅ Answer generated")
            print(f"   Preview: {answer[:100]}...")
        else:
            print("   ❌ Q/A failed")
            return False
        
        # Test Agent 4
        print("\n4️⃣ Testing Agent 4: Recommendation...")
        agent4 = RecommendationAgent(products)
        rec = agent4.recommend_alternative(results[0], sentiment, products)
        if rec:
            print(f"   ✅ Recommendation: {rec['message'][:50]}...")
        else:
            print("   ❌ Recommendation failed")
            return False
        
        print("\n✅ PHASE 2 PASSED")
        return True
    
    except Exception as e:
        print(f"\n❌ PHASE 2 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_phase3_integration():
    """Test Phase 3: Complete System Integration"""
    print("\n" + "="*60)
    print("🧪 TESTING PHASE 3: INTEGRATION")
    print("="*60)
    
    try:
        from main import MultiAgentSystem
        from utils.data_loader import load_data

        
        
        # Load data
        products, reviews = load_data(use_sample=True)
        
        # Initialize system
        print("\n1️⃣ Initializing Multi-Agent System...")
        system = MultiAgentSystem(products, reviews)
        print("   ✅ System initialized")
        
        # Test query processing
        print("\n2️⃣ Testing Query Processing...")
        test_query = "Is this laptop good for gaming?"
        result = system.process_query(test_query)
        
        if "error" in result:
            print(f"   ❌ Query failed: {result['error']}")
            return False
        
        print("   ✅ Query processed successfully")
        
        # Display result
        print("\n3️⃣ Displaying Result...")
        system.display_result(result)
        
        # Test stats
        print("\n4️⃣ Testing System Stats...")
        stats = system.get_system_stats()
        print(f"   Products: {stats['products']}")
        print(f"   Reviews: {stats['reviews']}")
        print(f"   ✅ Stats retrieved")
        
        print("\n✅ PHASE 3 PASSED")
        return True
    
    except Exception as e:
        print(f"\n❌ PHASE 3 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests in sequence."""
    print("\n" + "="*60)
    print("🚀 RUNNING COMPLETE SYSTEM TEST")
    print("="*60)
    
    results = {
        "Phase 1 (Utils)": False,
        "Phase 2 (Agents)": False,
        "Phase 3 (Integration)": False
    }
    
    # Run tests
    results["Phase 1 (Utils)"] = test_phase1_utils()
    
    if results["Phase 1 (Utils)"]:
        results["Phase 2 (Agents)"] = test_phase2_agents()
    
    if results["Phase 2 (Agents)"]:
        results["Phase 3 (Integration)"] = test_phase3_integration()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for phase, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{phase}: {status}")
    
    all_passed = all(results.values())
    
    print("="*60)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("Your multi-agent system is ready to use!")
    else:
        print("\n⚠️ SOME TESTS FAILED")
        print("Please check the errors above and fix issues.")
    
    print("\n" + "="*60)
    
    return all_passed


if __name__ == "__main__":
    run_all_tests()



''' Output
============================================================
🚀 RUNNING COMPLETE SYSTEM TEST
============================================================

============================================================
🧪 TESTING PHASE 1: UTILS
============================================================

1️⃣ Testing Configuration...
✅ API Key configured

🔍 Detecting available models...

   ✓ gemini-2.5-pro-preview-03-25
   ✓ gemini-2.5-flash
   ✓ gemini-2.5-pro-preview-05-06
   ✓ gemini-2.5-pro-preview-06-05
   ✓ gemini-2.5-pro
   ✓ gemini-2.0-flash-exp
   ✓ gemini-2.0-flash
   ✓ gemini-2.0-flash-001
   ✓ gemini-2.0-flash-exp-image-generation
   ✓ gemini-2.0-flash-lite-001
   ✓ gemini-2.0-flash-lite
   ✓ gemini-2.0-flash-lite-preview-02-05
   ✓ gemini-2.0-flash-lite-preview
   ✓ gemini-2.0-pro-exp
   ✓ gemini-2.0-pro-exp-02-05
   ✓ gemini-exp-1206
   ✓ gemini-2.0-flash-thinking-exp-01-21
   ✓ gemini-2.0-flash-thinking-exp
   ✓ gemini-2.0-flash-thinking-exp-1219
   ✓ gemini-2.5-flash-preview-tts
   ✓ gemini-2.5-pro-preview-tts
   ✓ learnlm-2.0-flash-experimental
   ✓ gemma-3-1b-it
   ✓ gemma-3-4b-it
   ✓ gemma-3-12b-it
   ✓ gemma-3-27b-it
   ✓ gemma-3n-e4b-it
   ✓ gemma-3n-e2b-it
   ✓ gemini-flash-latest
   ✓ gemini-flash-lite-latest
   ✓ gemini-pro-latest
   ✓ gemini-2.5-flash-lite
   ✓ gemini-2.5-flash-image-preview
   ✓ gemini-2.5-flash-image
   ✓ gemini-2.5-flash-preview-09-2025
   ✓ gemini-2.5-flash-lite-preview-09-2025
   ✓ gemini-3-pro-preview
   ✓ gemini-3-pro-image-preview
   ✓ nano-banana-pro-preview
   ✓ gemini-robotics-er-1.5-preview
   ✓ gemini-2.5-computer-use-preview-10-2025

✅ Selected model: gemini-2.5-flash
💡 Using Flash model - Great for free tier!
   Rate limit: ~15 requests/minute
   Delay between calls: 4 seconds

✅ Configuration initialized successfully!

   ✅ Config initialized

============================================================
SYSTEM CONFIGURATION
============================================================
Model: gemini-2.5-flash
API Calls Made: 0
Rate Limit: 15 calls/minute
Call Delay: 4 seconds
Batch Size: 3 reviews/call
============================================================


2️⃣ Testing API Connection...
🧪 Testing API connection...
✅ API Test Result: API is working!
   ✅ API working

3️⃣ Testing Data Loading...
📦 Using sample data...
✅ Generated 6 sample products and 20 sample reviews
   ✅ Data loaded

============================================================
DATA SUMMARY
============================================================
Total Products: 6
Categories: 3 (Cameras, Laptops, Phones)
In Stock: 5
Out of Stock: 1
Total Stock Units: 90

Total Reviews: 20
Products with Reviews: 6
Average Rating: 4.2/5
============================================================


✅ PHASE 1 PASSED

============================================================
🧪 TESTING PHASE 2: AGENTS
============================================================
📦 Using sample data...
✅ Generated 6 sample products and 20 sample reviews

1️⃣ Testing Agent 1: Product Retrieval...
✅ Agent 1: Product Retrieval (Offline - Parallel Processing)

🔍 Agent 1: Searching for 'laptop gaming'
✅ Agent 1: Found 2 relevant products
   Top match: Gaming Laptop Pro 15 (score: 3.0)
   ✅ Found 2 products
   Top: Gaming Laptop Pro 15

2️⃣ Testing Agent 2: Sentiment Analysis...
✅ Agent 2: Sentiment Analysis (Loop + Batch + Memory)

💬 Agent 2: Analyzing 4 reviews for P001

⚠️ API Error: list index out of range
✅ Agent 2: Sentiment = Positive (100.0% positive)
   ✅ Sentiment: Positive
   Reviews: 4

3️⃣ Testing Agent 3: Q/A...
✅ Agent 3: Q/A (Sequential - depends on Agent 1 & 2)

🤔 Agent 3: Generating answer for 'Is this good?...'

⚠️ API Error: list index out of range
✅ Agent 3: Answer generated
   ✅ Answer generated
   Preview: Based on 4 customer reviews (100.0% positive, 4.5/5 stars), Gaming Laptop Pro 15 is well-received. I...

4️⃣ Testing Agent 4: Recommendation...
✅ Agent 4: Recommendation (Parallel + Rule-Based)

🎯 Agent 4: Evaluating Gaming Laptop Pro 15
✅ Agent 4: Current product is a great choice
   ✅ Recommendation: ✅ Great choice! This product has strong reviews an...

✅ PHASE 2 PASSED

============================================================
🧪 TESTING PHASE 3: INTEGRATION
============================================================
📦 Using sample data...
✅ Generated 6 sample products and 20 sample reviews

1️⃣ Initializing Multi-Agent System...

============================================================
🚀 INITIALIZING MULTI-AGENT SYSTEM
============================================================

✅ Agent 1: Product Retrieval (Offline - Parallel Processing)
✅ Agent 2: Sentiment Analysis (Loop + Batch + Memory)
✅ Agent 3: Q/A (Sequential - depends on Agent 1 & 2)
✅ Agent 4: Recommendation (Parallel + Rule-Based)

============================================================
✅ ALL AGENTS INITIALIZED
============================================================

   ✅ System initialized

2️⃣ Testing Query Processing...

============================================================
📝 PROCESSING QUERY: Is this laptop good for gaming?
============================================================

🔍 Agent 1: Searching for 'Is this laptop good for gaming?'
✅ Agent 1: Found 1 relevant products
   Top match: Gaming Laptop Pro 15 (score: 1.5)

💬 Agent 2: Analyzing 4 reviews for P001

⚠️ API Error: list index out of range

⚠️ API Error: list index out of range
✅ Agent 2: Sentiment = Positive (100.0% positive)

🤔 Agent 3: Generating answer for 'Is this laptop good for gaming?...'

⚠️ API Error: list index out of range
✅ Agent 3: Answer generated

🎯 Agent 4: Evaluating Gaming Laptop Pro 15
✅ Agent 4: Current product is a great choice
   ✅ Query processed successfully

3️⃣ Displaying Result...

============================================================
📊 FINAL RESULT
============================================================

🎯 Product: Gaming Laptop Pro 15
📁 Category: Laptops
💰 Price: $1299.99
📦 Stock: In Stock (15 units)
🎲 Relevance Score: 1.5

📊 Review Analysis:
   ⭐ 4 reviews | 4.5/5 stars
   📈 100.0% positive
   📉 0.0% negative
   🎯 Overall: Positive

💬 Answer:
   Based on 4 customer reviews (100.0% positive, 4.5/5 stars), Gaming Laptop Pro 15 is well-received. It's priced at $1299.99.

✅ Great choice! This product has strong reviews and is in stock.

============================================================


4️⃣ Testing System Stats...
   Products: 6
   Reviews: 20
   ✅ Stats retrieved

✅ PHASE 3 PASSED

============================================================
📊 TEST SUMMARY
============================================================
Phase 1 (Utils): ✅ PASSED
Phase 2 (Agents): ✅ PASSED
Phase 3 (Integration): ✅ PASSED
============================================================

🎉 ALL TESTS PASSED!
Your multi-agent system is ready to use!

'''