"""
Data Loader
===========
Handles loading and processing of product, review, and inventory data.

This module provides:
- CSV file loading
- Data validation
- Sample data generation
- Data merging (products + inventory)
"""

import csv
import os
import pandas as pd
from typing import List, Dict, Tuple
from .config import Config


def load_data(use_sample: bool = False) -> Tuple[List[Dict], List[Dict]]:
    """
    Load product and review data from CSV files or use sample data.
    
    Process:
    1. Check if CSV files exist
    2. Load products, reviews, inventory
    3. Merge inventory with products
    4. Validate data
    5. Return as list of dictionaries
    
    Args:
        use_sample (bool): If True, use sample data instead of CSV files
    
    Returns:
        Tuple[List[Dict], List[Dict]]: (products, reviews)
    
    Example:
        >>> products, reviews = load_data()
        >>> print(f"Loaded {len(products)} products")
    """
    
    if use_sample:
        print("📦 Using sample data...")
        return get_sample_data()
    
    try:
        # Check if files exist
        files_exist = all([
            os.path.exists(Config.PRODUCTS_FILE),
            os.path.exists(Config.REVIEWS_FILE)
        ])
        
        if not files_exist:
            print("⚠️ CSV files not found. Using sample data...")
            return get_sample_data()
        
        # Load CSV files
        print("📂 Loading data from CSV files...")
        
        products_df = pd.read_csv(Config.PRODUCTS_FILE)
        reviews_df = pd.read_csv(Config.REVIEWS_FILE)
        
        # Load inventory if available
        if os.path.exists(Config.INVENTORY_FILE):
            inventory_df = pd.read_csv(Config.INVENTORY_FILE)
            
            # Merge inventory with products
            products_df = products_df.merge(
                inventory_df, 
                on='product_id', 
                how='left'
            )
            
            # Rename stock column if needed
            if 'stock_quantity' in products_df.columns:
                products_df['stock'] = products_df['stock_quantity'].fillna(0).astype(int)
                products_df = products_df.drop('stock_quantity', axis=1)
            
            print("✅ Merged inventory data")
        else:
            print("⚠️ Inventory file not found. Setting default stock=0")
            products_df['stock'] = 0
        
        # Validate data
        products_df = validate_products(products_df)
        reviews_df = validate_reviews(reviews_df)
        
        # Convert to list of dictionaries
        products = products_df.to_dict('records')
        reviews = reviews_df.to_dict('records')
        
        print(f"✅ Loaded {len(products)} products and {len(reviews)} reviews")
        
        return products, reviews
    
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        print("📦 Falling back to sample data...")
        return get_sample_data()


def validate_products(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and clean product data.
    
    Checks:
    - Required columns exist
    - Data types are correct
    - No missing critical data
    
    Args:
        df (pd.DataFrame): Product dataframe
    
    Returns:
        pd.DataFrame: Validated dataframe
    """
    
    required_columns = ['product_id', 'title', 'description', 'price', 'category']
    
    # Check required columns
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Ensure correct data types
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['product_id'] = df['product_id'].astype(str)
    
    # Fill missing stock with 0
    if 'stock' not in df.columns:
        df['stock'] = 0
    else:
        df['stock'] = pd.to_numeric(df['stock'], errors='coerce').fillna(0).astype(int)
    
    # Remove rows with missing critical data
    df = df.dropna(subset=['product_id', 'title', 'price'])
    
    print(f"✅ Validated {len(df)} products")
    
    return df


def validate_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and clean review data.
    
    Checks:
    - Required columns exist
    - Ratings are valid (1-5)
    - Reviews have text
    
    Args:
        df (pd.DataFrame): Review dataframe
    
    Returns:
        pd.DataFrame: Validated dataframe
    """
    
    required_columns = ['product_id', 'review_text', 'rating']
    
    # Check required columns
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Ensure correct data types
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['product_id'] = df['product_id'].astype(str)
    
    # Filter valid ratings (1-5)
    df = df[df['rating'].between(1, 5)]
    
    # Remove empty reviews
    df = df[df['review_text'].notna()]
    df = df[df['review_text'].str.strip() != '']
    
    print(f"✅ Validated {len(df)} reviews")
    
    return df


'''def get_sample_data() -> Tuple[List[Dict], List[Dict]]:
    """
    Generate sample data for testing.
    
    Returns:
        Tuple[List[Dict], List[Dict]]: (products, reviews)
    
    Example:
        >>> products, reviews = get_sample_data()
        >>> print(products[0]['title'])
        'Gaming Laptop Pro 15'
    """
    
    products = [
        {
            "product_id": "P001",
            "title": "Gaming Laptop Pro 15",
            "description": "High-performance laptop with RTX 4060, 16GB RAM, perfect for gaming and video editing",
            "price": 1299.99,
            "category": "Laptops",
            "stock": 15
        },
        {
            "product_id": "P002",
            "title": "Budget Office Laptop",
            "description": "Affordable laptop for basic tasks, web browsing, and office work",
            "price": 449.99,
            "category": "Laptops",
            "stock": 25
        },
        {
            "product_id": "P003",
            "title": "Gaming Phone X1",
            "description": "Flagship phone with Snapdragon 8 Gen 3, 120Hz display, excellent for mobile gaming",
            "price": 899.99,
            "category": "Phones",
            "stock": 30
        },
        {
            "product_id": "P004",
            "title": "Professional Video Camera",
            "description": "4K video camera with advanced stabilization, perfect for content creators",
            "price": 1599.99,
            "category": "Cameras",
            "stock": 8
        },
        {
            "product_id": "P005",
            "title": "MacBook Pro M3",
            "description": "Professional laptop with M3 chip, excellent for video editing and creative work",
            "price": 1999.99,
            "category": "Laptops",
            "stock": 12
        },
        {
            "product_id": "P006",
            "title": "Budget Smartphone",
            "description": "Affordable smartphone for everyday use, decent camera and battery life",
            "price": 299.99,
            "category": "Phones",
            "stock": 0  # Out of stock
        }
    ]
    
    reviews = [
        # Gaming Laptop Pro 15 (P001) - Positive reviews
        {"product_id": "P001", "review_text": "Amazing laptop! Runs all games smoothly. Great for video editing too.", "rating": 5},
        {"product_id": "P001", "review_text": "Good performance but gets hot during intensive tasks.", "rating": 4},
        {"product_id": "P001", "review_text": "Best laptop I've owned. Worth every penny!", "rating": 5},
        {"product_id": "P001", "review_text": "A bit expensive but the quality justifies it.", "rating": 4},
        
        # Budget Office Laptop (P002) - Mixed reviews
        {"product_id": "P002", "review_text": "Perfect for basic tasks but slow for gaming or heavy software.", "rating": 3},
        {"product_id": "P002", "review_text": "Great value for money for office work.", "rating": 4},
        {"product_id": "P002", "review_text": "Does what it says. Good budget option.", "rating": 4},
        {"product_id": "P002", "review_text": "Screen quality could be better.", "rating": 3},
        
        # Gaming Phone X1 (P003) - Mostly positive
        {"product_id": "P003", "review_text": "Excellent gaming performance! Screen is stunning.", "rating": 5},
        {"product_id": "P003", "review_text": "Battery drains fast during gaming sessions.", "rating": 3},
        {"product_id": "P003", "review_text": "Best phone for mobile gaming hands down.", "rating": 5},
        {"product_id": "P003", "review_text": "Great display and smooth performance.", "rating": 5},
        
        # Professional Video Camera (P004) - High ratings
        {"product_id": "P004", "review_text": "Professional quality video. Amazing stabilization.", "rating": 5},
        {"product_id": "P004", "review_text": "Pricey but worth it for content creation.", "rating": 4},
        {"product_id": "P004", "review_text": "Best camera I've used for vlogging.", "rating": 5},
        
        # MacBook Pro M3 (P005) - Excellent reviews
        {"product_id": "P005", "review_text": "Incredible performance for video editing. Fast render times.", "rating": 5},
        {"product_id": "P005", "review_text": "Expensive but the M3 chip is a game changer.", "rating": 5},
        {"product_id": "P005", "review_text": "Best laptop for creative professionals.", "rating": 5},
        
        # Budget Smartphone (P006) - Lower ratings, out of stock
        {"product_id": "P006", "review_text": "Decent for the price but camera is mediocre.", "rating": 3},
        {"product_id": "P006", "review_text": "Battery life is poor. Disappointing.", "rating": 2},
    ]
    
    print(f"✅ Generated {len(products)} sample products and {len(reviews)} sample reviews")
    
    return products, reviews'''

'''import csv
from typing import List, Dict, Tuple'''

def get_sample_data(
    products_csv: str = "data/products.csv",
    reviews_csv: str = "data/reviews.csv"
) -> Tuple[List[Dict], List[Dict]]:
    """
    Load product and review data from CSV files inside the data/ folder.

    Returns:
        Tuple[List[Dict], List[Dict]]: (products, reviews)
    """

    products = []
    reviews = []

    # ----- Load products.csv -----
    with open(products_csv, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["product_id"] = str(row["product_id"])
            row["price"] = float(row["price"])
            row["stock"] = int(row["stock"])
            products.append(row)

    # ----- Load reviews.csv -----
    with open(reviews_csv, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["product_id"] = str(row["product_id"])
            row["rating"] = int(row["rating"])
            reviews.append(row)

    print(f"✅ Loaded {len(products)} products and {len(reviews)} reviews.")
    return products, reviews



def save_sample_data_to_csv():
    """
    Save sample data to CSV files for testing.
    
    Creates:
    - data/products.csv
    - data/reviews.csv
    - data/inventory.csv
    
    Example:
        >>> save_sample_data_to_csv()
        ✅ Sample data saved to CSV files
    """
    
    products, reviews = get_sample_data()
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Convert to DataFrames
    products_df = pd.DataFrame(products)
    reviews_df = pd.DataFrame(reviews)
    
    # Split inventory from products
    inventory_df = products_df[['product_id', 'stock']].copy()
    inventory_df = inventory_df.rename(columns={'stock': 'stock_quantity'})
    
    # Remove stock from products (it will be merged later)
    products_df_for_csv = products_df.drop('stock', axis=1)
    
    # Save to CSV
    products_df_for_csv.to_csv('data/products.csv', index=False)
    reviews_df.to_csv('data/reviews.csv', index=False)
    inventory_df.to_csv('data/inventory.csv', index=False)
    
    print("✅ Sample data saved to CSV files:")
    print(f"   - data/products.csv ({len(products)} products)")
    print(f"   - data/reviews.csv ({len(reviews)} reviews)")
    print(f"   - data/inventory.csv ({len(inventory_df)} items)")


def get_data_summary(products: List[Dict], reviews: List[Dict]) -> dict:
    """
    Get summary statistics about the data.
    
    Args:
        products (List[Dict]): Product list
        reviews (List[Dict]): Review list
    
    Returns:
        dict: Summary statistics
    
    Example:
        >>> products, reviews = load_data()
        >>> summary = get_data_summary(products, reviews)
        >>> print(summary['total_products'])
    """
    
    # Product statistics
    total_products = len(products)
    categories = set(p['category'] for p in products)
    total_stock = sum(p.get('stock', 0) for p in products)
    in_stock = sum(1 for p in products if p.get('stock', 0) > 0)
    out_of_stock = total_products - in_stock
    
    # Review statistics
    total_reviews = len(reviews)
    products_with_reviews = len(set(r['product_id'] for r in reviews))
    avg_rating = sum(r['rating'] for r in reviews) / total_reviews if total_reviews > 0 else 0
    
    return {
        "total_products": total_products,
        "total_categories": len(categories),
        "categories": list(categories),
        "total_stock": total_stock,
        "in_stock": in_stock,
        "out_of_stock": out_of_stock,
        "total_reviews": total_reviews,
        "products_with_reviews": products_with_reviews,
        "avg_rating": round(avg_rating, 2)
    }


def display_data_summary(products: List[Dict], reviews: List[Dict]):
    """
    Display formatted data summary.
    
    Example:
        >>> products, reviews = load_data()
        >>> display_data_summary(products, reviews)
    """
    
    summary = get_data_summary(products, reviews)
    
    print("\n" + "="*60)
    print("DATA SUMMARY")
    print("="*60)
    print(f"Total Products: {summary['total_products']}")
    print(f"Categories: {summary['total_categories']} ({', '.join(summary['categories'])})")
    print(f"In Stock: {summary['in_stock']}")
    print(f"Out of Stock: {summary['out_of_stock']}")
    print(f"Total Stock Units: {summary['total_stock']}")
    print(f"\nTotal Reviews: {summary['total_reviews']}")
    print(f"Products with Reviews: {summary['products_with_reviews']}")
    print(f"Average Rating: {summary['avg_rating']}/5")
    print("="*60 + "\n")


# ============================================
# Testing
# ============================================

if __name__ == "__main__":
    print("Testing Data Loader...\n")
    
    # Test loading sample data
    products, reviews = load_data(use_sample=True)
    
    # Display summary
    display_data_summary(products, reviews)
    
    # Test saving to CSV
    print("\n🧪 Testing CSV save...")
    save_sample_data_to_csv()
    
    # Test loading from CSV
    print("\n🧪 Testing CSV load...")
    products, reviews = load_data(use_sample=False)
    display_data_summary(products, reviews)