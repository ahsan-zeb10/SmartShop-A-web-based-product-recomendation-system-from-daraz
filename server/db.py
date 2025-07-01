from bson import ObjectId
from pymongo import MongoClient, UpdateOne
import time
from scraper import scrape_daraz
import logging
logger = logging.getLogger(__name__)
# Connect to MongoDB
client = MongoClient("mongodb+srv://ahsan:ahsan123@cluster0.qzuyctn.mongodb.net/")
db = client["FYP"]
products_collection = db["products"]
products_collection.create_index("link")
products_collection.create_index("category")

def add_products(products: list):
    """Add or update multiple products in the database using bulk write."""
    operations = [
        UpdateOne(
            {"link": p["link"]},
            {"$set": {
                "title": p["title"],
                "price": p["price"],
                "image_url": p["image_url"],
                "category": p["category"],
                "stars": p["stars"],
                "review_count": p["review_count"],
                "reviews": p["reviews"],
                "sentiment_score": p["sentiment_score"],
                "average_rating": p["average_rating"],
                "positive_reviews": p["positive_reviews"],
                "updated_at": time.time()
            }},
            upsert=True
        ) for p in products
    ]
    if operations:
        products_collection.bulk_write(operations)

def get_product_by_id(product_id: str):
    """
    Fetch a product by its MongoDB _id from the products collection.
    Args:
        product_id (str): The product's unique ID as a string.
    Returns:
        dict: The product data or None if not found.
    """
    try:
        # Ensure product_id is a valid ObjectId format
        product_id_object = ObjectId(product_id)
        
        # Query the products collection for the product with the given _id
        product = products_collection.find_one({"_id": product_id_object})
        
        if product:
            # Convert the _id to string for easier handling in the API response
            product["_id"] = str(product["_id"])
            return product
        
        # If product is not found, log and return None
        else:
            logger.warning(f"Product with ID {product_id} not found.")
            return None

    except Exception as e:
        logger.error(f"Error fetching product by ID {product_id}: {str(e)}")
        return None


def get_products_by_category(category: str, query: str = None, limit: int = 20) -> list:
    """Retrieve products by category, prioritizing exact matches if query is provided."""
    if query:
        # First try to find exact matches in the title
        exact_matches = products_collection.find({
            "category": category,
            "title": {"$regex": f"^{query}$", "$options": "i"}
        }).limit(limit)
        
        exact_matches_list = list(exact_matches)
        if exact_matches_list:
            return [{**p, "_id": str(p["_id"])} for p in exact_matches_list]
        
        # If no exact matches, try partial matches
        partial_matches = products_collection.find({
            "category": category,
            "title": {"$regex": query, "$options": "i"}
        }).limit(limit)
        
        partial_matches_list = list(partial_matches)
        if partial_matches_list:
            return [{**p, "_id": str(p["_id"])} for p in partial_matches_list]
    
    # If no matches found or no query provided, return all products in category
    products = products_collection.find({"category": category}).limit(limit)
    return [{**p, "_id": str(p["_id"])} for p in products]

# def get_products_by_category(category: str, query: str = None, limit: int = 20) -> list:
#     """Retrieve products by category, prioritizing exact matches if query is provided."""
    
#     # First, try fetching products from the database
#     products = list(products_collection.find({"category": category}).limit(limit))
    
#     # If products exist in the DB, return them
#     if products:
#         return [{**p, "_id": str(p["_id"])} for p in products]
    
#     # If no products found in the DB, scrape from Daraz and add them to the DB
#     logger.info(f"No products found in DB for category '{category}', scraping from Daraz...")
#     products = scrape_and_store_products_by_category(category, limit)
#     return products

# def scrape_and_store_products_by_category(category: str, limit: int) -> list:
#     """Scrape products from Daraz for a given category and store them in the DB."""
#     # Call the scraper function to get the products for the category
#     products = scrape_daraz(category, max_products=limit)
    
#     # Add the scraped products to the database
#     if products:
#         add_products(products)
#         logger.info(f"Added {len(products)} products to DB for category '{category}'")
    
#     return products

def get_products_by_query(query: str, limit: int = 20) -> list:
    """Search products by matching query string in title (case-insensitive)."""
    products = products_collection.find(
        {"title": {"$regex": query, "$options": "i"}}
    ).limit(limit)
    return [{**p, "_id": str(p["_id"])} for p in products]

def parse_category(query: str) -> str:
    """Dynamically determine category based on search query."""
    query = query.lower()
    
    # Map search terms to specific categories
    category_mapping = {
        "phone": ["phone", "phones", "mobile", "mobiles", "smartphone", "smartphones"],
        "laptop": ["laptop", "laptops", "notebook", "notebooks"],
        "tablet": ["tablet", "tablets", "ipad"],
        "smartwatch": ["smartwatch", "smartwatches", "watch", "watches"],
        "headphones": ["headphone", "headphones", "earphone", "earphones", "earbuds"],
        "camera": ["camera", "cameras", "dslr", "mirrorless"],
        "television": ["tv", "television", "televisions", "smart tv"],
        "refrigerator": ["fridge", "refrigerator", "refrigerators"],
        "washing machine": ["washing machine", "washing machines", "washer"]
    }
    
    # Check if query matches any category keywords
    for category, keywords in category_mapping.items():
        if any(keyword in query for keyword in keywords):
            return category
    
    # If no match found, return the query itself
    return query



