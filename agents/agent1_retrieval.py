"""
Agent 1: Product Retrieval Agent
=================================

Purpose:
    Finds the most relevant products based on user query.

Technique:
    - Parallel Processing: Evaluates all products simultaneously
    - Keyword Matching: Uses text analysis (no API calls needed)
    - Relevance Scoring: Ranks products by match quality

How it works:
    1. Takes user query (e.g., "laptop for video editing")
    2. Extracts keywords from query
    3. Calculates relevance score for each product
    4. Ranks products by relevance
    5. Returns top matches with stock information

Why no API:
    - Faster (instant results)
    - No rate limits
    - Saves API quota for more complex tasks
    - Deterministic results

Logic:
    Score = keyword_matches + title_boost + category_relevance
"""

from typing import List, Dict


class ProductRetrievalAgent:
    """
    Agent 1: Product Retrieval using Parallel Keyword Matching
    """
    
    def __init__(self, products: List[Dict]):
        """
        Initialize the product retrieval agent.
        
        Args:
            products (List[Dict]): List of product dictionaries
        """
        self.products = products
        print("✅ Agent 1: Product Retrieval (Offline - Parallel Processing)")
    
    def calculate_relevance(self, query: str, product: Dict) -> float:
        """
        Calculate relevance score between query and product.
        
        Scoring Logic:
        - Each keyword match in description: +1.0
        - Each keyword match in title: +1.5 (more important)
        - Exact query in title: +3.0 (very relevant)
        - Category match: +0.5
        
        Args:
            query (str): User search query
            product (Dict): Product information
        
        Returns:
            float: Relevance score (higher = more relevant)
        
        Example:
            >>> score = calculate_relevance("gaming laptop", product)
            >>> print(score)  # e.g., 4.5
        """
        query_lower = query.lower()
        
        # Prepare product text
        title = product.get('title', '').lower()
        description = product.get('description', '').lower()
        category = product.get('category', '').lower()
        
        # Combined text for searching
        full_text = f"{title} {description} {category}"
        
        score = 0.0
        
        # Extract keywords (words longer than 3 characters)
        query_words = [w for w in query_lower.split() if len(w) > 3]
        
        # Score keyword matches
        for word in query_words:
            # Match in title (weighted higher)
            if word in title:
                score += 1.5
            
            # Match in description
            elif word in description:
                score += 1.0
            
            # Match in category
            elif word in category:
                score += 0.5
        
        # Boost for exact phrase match in title
        if query_lower in title:
            score += 3.0
        
        # Boost for exact phrase match in description
        elif query_lower in description:
            score += 1.5
        
        return score
    
    def retrieve_products(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve top-k most relevant products (Parallel Processing).
        
        Process:
        1. Score all products in parallel
        2. Sort by relevance score
        3. Select top K products
        4. Add stock status information
        5. Return results
        
        Args:
            query (str): User search query
            top_k (int): Number of products to return (default: 3)
        
        Returns:
            List[Dict]: Top K relevant products with scores
        
        Example:
            >>> agent = ProductRetrievalAgent(products)
            >>> results = agent.retrieve_products("gaming laptop", top_k=3)
            >>> print(results[0]['title'])
            'Gaming Laptop Pro 15'
        """
        print(f"\n🔍 Agent 1: Searching for '{query}'")
        
        # Parallel processing: score all products
        scored_products = []
        for product in self.products:
            score = self.calculate_relevance(query, product)
            
            # Create enriched product dict
            scored_products.append({
                **product,  # Original product data
                "relevance_score": score,
                "matched_query": query
            })
        
        # Sort by relevance (highest first)
        scored_products.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Take top K
        top_products = scored_products[:top_k]
        
        # Add stock status
        for product in top_products:
            stock = product.get('stock', 0)
            product['stock_status'] = "In Stock" if stock > 0 else "Out of Stock"
        
        print(f"✅ Agent 1: Found {len(top_products)} relevant products")
        
        # Show top match
        if top_products:
            top = top_products[0]
            print(f"   Top match: {top['title']} (score: {top['relevance_score']:.1f})")
        
        return top_products
    
    def get_product_by_id(self, product_id: str) -> Dict:
        """
        Get a specific product by ID.
        
        Args:
            product_id (str): Product ID
        
        Returns:
            Dict: Product information or None
        """
        for product in self.products:
            if product.get('product_id') == product_id:
                return product
        return None
    
    def get_products_by_category(self, category: str) -> List[Dict]:
        """
        Get all products in a specific category.
        
        Args:
            category (str): Category name
        
        Returns:
            List[Dict]: Products in category
        """
        category_lower = category.lower()
        return [
            p for p in self.products 
            if p.get('category', '').lower() == category_lower
        ]
    
    def get_stats(self) -> Dict:
        """
        Get agent statistics.
        
        Returns:
            Dict: Statistics about products
        """
        total = len(self.products)
        categories = set(p.get('category') for p in self.products)
        in_stock = sum(1 for p in self.products if p.get('stock', 0) > 0)
        
        return {
            "total_products": total,
            "categories": list(categories),
            "in_stock": in_stock,
            "out_of_stock": total - in_stock
        }


# ============================================
# Testing
# ============================================

if __name__ == "__main__":
    # Test the agent
    print("Testing Product Retrieval Agent...\n")
    
    # Sample products
    test_products = [
        {
            "product_id": "P001",
            "title": "Gaming Laptop Pro",
            "description": "High-performance laptop for gaming and video editing",
            "price": 1299.99,
            "category": "Laptops",
            "stock": 15
        },
        {
            "product_id": "P002",
            "title": "Office Laptop",
            "description": "Budget laptop for office work",
            "price": 449.99,
            "category": "Laptops",
            "stock": 25
        }
    ]
    
    # Initialize agent
    agent = ProductRetrievalAgent(test_products)
    
    # Test search
    results = agent.retrieve_products("gaming laptop", top_k=2)
    
    print("\nResults:")
    for r in results:
        print(f"- {r['title']} (score: {r['relevance_score']})")
    
    # Test stats
    print("\nAgent Stats:")
    print(agent.get_stats())