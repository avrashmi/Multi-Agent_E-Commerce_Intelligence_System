from utils.config import initialize
from utils.api_helper import test_api_connection
from utils.data_loader import load_data, display_data_summary

# Test configuration
print("Testing Phase 1: Utils\n")

# 1. Initialize config
initialize()

# 2. Test API
test_api_connection()

# 3. Load data
products, reviews = load_data(use_sample=True)
display_data_summary(products, reviews)

print("\n✅ Phase 1 test complete!")