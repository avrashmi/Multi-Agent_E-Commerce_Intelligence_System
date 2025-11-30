"""
Agent 4: Recommendation Agent
==============================

Purpose:
    Suggests better alternatives when current product has issues.

Techniques:
    - Parallel Processing: Evaluates all alternatives simultaneously
    - Rule-Based Logic: Fast decision-making without API
    - Memory: Remembers product catalog

How it works:
    1. Checks current product status
    2. Applies decision rules:
       - Rule 1: Out of stock? → Find in-stock alternative
       - Rule 2: Low ratings? → Find better-rated alternative
       - Rule 3: Product is good? → Confirm choice
    3. If alternative needed:
       - Filter by same category
       - Filter by stock availability
       - Sort by relevance/ratings
       - Select best match
    4. Return recommendation with justification

Why rule-based:
    - Simple logic doesn't need AI
    - Instant decisions (no API delay)
    - Deterministic, predictable results
    - Saves API quota for complex tasks

Decision tree:
    Current Product
        ↓
    Is Stock = 0? → YES → Find in-stock alternative
        ↓ NO
    Is Rating < 70%? → YES → Find better-rated alternative
        ↓ NO
    Confirm good choice

Logic:
    Rules → Filter → Sort → Select → Justify
"""

from typing import List, Dict, Any


class RecommendationAgent:
    """
    Agent 4: Recommendation using Parallel Rule-Based Logic
    """
    
    def __init__(self, products: List[Dict]):
        """
        Initialize recommendation agent.
        
        Args:
            products (List[Dict]): Full product catalog
        """
        self.products = products
        print("✅ Agent 4: Recommendation (Parallel + Rule-Based)")
    
    def recommend_alternative(
        self,
        current_product: Dict,
        sentiment: Dict,
        all_products: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Find better alternatives if current product has issues.
        
        Decision Rules:
        1. Check if out of stock → Find in-stock alternative
        2. Check if low rating → Find better-rated alternative
        3. Otherwise → Confirm current product is good
        
        Args:
            current_product (Dict): Current product being considered
            sentiment (Dict): Sentiment analysis of current product
            all_products (List[Dict], optional): Product catalog (uses self.products if None)
        
        Returns:
            Dict: Recommendation result with alternative or confirmation
        
        Example:
            >>> agent = RecommendationAgent(products)
            >>> result = agent.recommend_alternative(product, sentiment)
            >>> if result['needs_alternative']:
            ...     print(result['product']['title'])
        """
        
        if all_products is None:
            all_products = self.products
        
        print(f"\n🎯 Agent 4: Evaluating {current_product.get('title', 'product')}")
        
        # Rule 1: Check stock availability
        stock_result = self._check_stock(current_product, all_products)
        if stock_result:
            print(f"✅ Agent 4: Found in-stock alternative")
            return stock_result
        
        # Rule 2: Check review quality
        quality_result = self._check_quality(current_product, sentiment, all_products)
        if quality_result:
            print(f"✅ Agent 4: Found better-rated alternative")
            return quality_result
        
        # Rule 3: Current product is good
        print(f"✅ Agent 4: Current product is a great choice")
        return {
            "needs_alternative": False,
            "reason": "good_choice",
            "message": "✅ Great choice! This product has strong reviews and is in stock."
        }
    
    def _check_stock(self, current: Dict, all_products: List[Dict]) -> Dict[str, Any]:
        """
        Rule 1: Check if product is out of stock.
        
        Args:
            current (Dict): Current product
            all_products (List[Dict]): All available products
        
        Returns:
            Dict: Alternative recommendation or None
        """
        
        if current.get('stock', 1) > 0:
            return None  # In stock, no alternative needed
        
        # Find in-stock alternatives in same category
        alternatives = [
            p for p in all_products
            if p['category'] == current.get('category')
            and p['product_id'] != current.get('product_id')
            and p.get('stock', 0) > 0
        ]
        
        if not alternatives:
            return {
                "needs_alternative": True,
                "reason": "out_of_stock",
                "product": None,
                "message": "⚠️ This product is out of stock and no alternatives are available."
            }
        
        # Select best alternative (first one for simplicity)
        best = alternatives[0]
        
        return {
            "needs_alternative": True,
            "reason": "out_of_stock",
            "product": best,
            "message": f"⚠️ Out of stock. Consider {best['title']} at ${best['price']} instead ({best.get('stock', 0)} units available)."
        }
    
    def _check_quality(
        self, 
        current: Dict, 
        sentiment: Dict, 
        all_products: List[Dict]
    ) -> Dict[str, Any]:
        """
        Rule 2: Check if product has low ratings.
        
        Threshold: If positive reviews < 70% and has 3+ reviews,
                  suggest better alternative.
        
        Args:
            current (Dict): Current product
            sentiment (Dict): Review analysis
            all_products (List[Dict]): All available products
        
        Returns:
            Dict: Alternative recommendation or None
        """
        
        positive_pct = sentiment.get('positive_percent', 100)
        total_reviews = sentiment.get('total_reviews', 0)
        
        # If product has good reviews or too few reviews, don't recommend alternative
        if positive_pct >= 70 or total_reviews < 1:
            return None
        
        # Find better alternatives in same category
        alternatives = [
            p for p in all_products
            if p['category'] == current.get('category')
            and p['product_id'] != current.get('product_id')
            and p.get('stock', 0) > 0
        ]
        
        if not alternatives:
            return None  # No alternatives available
        
        # Select best alternative
        best = alternatives[0]
        
        return {
            "needs_alternative": True,
            "reason": "low_rating",
            "product": best,
            "message": f"💡 Based on reviews, you might also like {best['title']} at ${best['price']}."
        }
    
    def get_alternatives_by_category(
        self, 
        category: str, 
        exclude_id: str = None
    ) -> List[Dict]:
        """
        Get all alternatives in a specific category.
        
        Args:
            category (str): Product category
            exclude_id (str, optional): Product ID to exclude
        
        Returns:
            List[Dict]: Alternative products
        """
        
        alternatives = [
            p for p in self.products
            if p.get('category', '').lower() == category.lower()
            and p.get('stock', 0) > 0
        ]
        
        if exclude_id:
            alternatives = [p for p in alternatives if p.get('product_id') != exclude_id]
        
        return alternatives
    
    def get_similar_products(
        self, 
        product: Dict, 
        max_price_diff: float = 500
    ) -> List[Dict]:
        """
        Find products similar in price and category.
        
        Args:
            product (Dict): Reference product
            max_price_diff (float): Maximum price difference
        
        Returns:
            List[Dict]: Similar products
        """
        
        target_price = product.get('price', 0)
        target_category = product.get('category', '')
        product_id = product.get('product_id', '')
        
        similar = [
            p for p in self.products
            if p['category'] == target_category
            and p['product_id'] != product_id
            and p.get('stock', 0) > 0
            and abs(p.get('price', 0) - target_price) <= max_price_diff
        ]
        
        # Sort by price similarity
        similar.sort(key=lambda x: abs(x.get('price', 0) - target_price))
        
        return similar
    
    def get_upgrade_options(self, product: Dict) -> List[Dict]:
        """
        Find premium alternatives (higher price, same category).
        
        Args:
            product (Dict): Current product
        
        Returns:
            List[Dict]: Premium alternatives
        """
        
        current_price = product.get('price', 0)
        category = product.get('category', '')
        product_id = product.get('product_id', '')
        
        upgrades = [
            p for p in self.products
            if p['category'] == category
            and p['product_id'] != product_id
            and p.get('price', 0) > current_price
            and p.get('stock', 0) > 0
        ]
        
        # Sort by price (ascending)
        upgrades.sort(key=lambda x: x.get('price', 0))
        
        return upgrades
    
    def get_budget_options(self, product: Dict) -> List[Dict]:
        """
        Find budget alternatives (lower price, same category).
        
        Args:
            product (Dict): Current product
        
        Returns:
            List[Dict]: Budget alternatives
        """
        
        current_price = product.get('price', 0)
        category = product.get('category', '')
        product_id = product.get('product_id', '')
        
        budget = [
            p for p in self.products
            if p['category'] == category
            and p['product_id'] != product_id
            and p.get('price', 0) < current_price
            and p.get('stock', 0) > 0
        ]
        
        # Sort by price (descending - best budget option first)
        budget.sort(key=lambda x: x.get('price', 0), reverse=True)
        
        return budget
    
    def get_stats(self) -> Dict:
        """
        Get recommendation agent statistics.
        
        Returns:
            Dict: Statistics about product catalog
        """
        
        total = len(self.products)
        categories = list(set(p.get('category') for p in self.products))
        in_stock = sum(1 for p in self.products if p.get('stock', 0) > 0)
        
        return {
            "total_products": total,
            "categories": categories,
            "in_stock_products": in_stock,
            "out_of_stock_products": total - in_stock
        }


# ============================================
# Testing
# ============================================

if __name__ == "__main__":
    print("Testing Recommendation Agent...\n")
    
    # Sample products
    test_products = [
        {
            "product_id": "P001",
            "title": "Gaming Laptop Pro",
            "description": "High-performance",
            "price": 1299.99,
            "category": "Laptops",
            "stock": 0  # Out of stock
        },
        {
            "product_id": "P002",
            "title": "Office Laptop",
            "description": "Budget option",
            "price": 699.99,
            "category": "Laptops",
            "stock": 10
        }
    ]
    
    # Initialize agent
    agent = RecommendationAgent(test_products)
    
    # Test recommendation
    current = test_products[0]
    sentiment = {"positive_percent": 85, "total_reviews": 50}
    
    result = agent.recommend_alternative(current, sentiment)
    
    print("\nResult:")
    print(f"Needs alternative: {result['needs_alternative']}")
    print(f"Reason: {result['reason']}")
    print(f"Message: {result['message']}")
    
    # Test stats
    print(f"\nAgent Stats: {agent.get_stats()}")