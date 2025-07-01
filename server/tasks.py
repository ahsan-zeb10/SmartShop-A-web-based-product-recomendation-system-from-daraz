##tasks.py
from celery_config import app
from scraper import scrape_daraz
from db import add_products, products_collection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAJOR_CATEGORIES = [
    "phone",          # For mobile phones
    "laptop",         # For laptops
    "tablet",         # For tablets
    "smartwatch",     # For smartwatches
    "headphones",     # For headphones and earphones
    "camera",         # For cameras
    "television",     # For TVs
    "refrigerator",   # For refrigerators
    "washing machine" # For washing machines
]

@app.task
def scrape_search_query(query: str, max_products: int = 5):
    logger.info(f"🔍 Scraping query: {query}")
    try:
        products = scrape_daraz(query, max_products=max_products)
        if products:
            for product in products:
                product["category"] = query
            add_products(products)
            logger.info(f"✅ Added {len(products)} products for '{query}'")
        return {"success": True, "products_count": len(products)}
    except Exception as e:
        logger.error(f"❌ Failed to scrape {query}: {e}")
        return {"success": False, "error": str(e)}

@app.task
def scrape_major_categories():
    logger.info("🔄 Running scheduled scraping task...")
    
    # Clear existing data
    deleted_count = products_collection.delete_many({}).deleted_count
    logger.info(f"🗑️ Deleted {deleted_count} old products from the database.")

    # Scrape each category
    for query in MAJOR_CATEGORIES:
        logger.info(f"🔍 Scraping category: {query}")
        try:
            products = scrape_daraz(query, max_products=25)
            for product in products:
                product["category"] = query
            add_products(products)
            logger.info(f"✅ Added {len(products)} products for '{query}'")
        except Exception as e:
            logger.error(f"❌ Failed to scrape {query}: {e}")



# from celery_config import app
# from scraper import scrape_daraz, scrape_product_reviews
# from db import add_products, add_reviews, get_recent_product_ids, products_collection
# from user_interactions import compute_recommendations_for_user
# from bson import ObjectId
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# MAJOR_CATEGORIES = [
#     "phone", "laptop", "tablet", "smartwatch", "headphones",
#     "camera", "television", "refrigerator", "washing machine", "perfume"
# ]

# @app.task
# def scrape_search_query(query: str, max_products: int = 5):
#     logger.info(f"🔍 Scraping query: {query}")
#     try:
#         products = scrape_daraz(query, max_products=max_products)
#         if products:
#             for product in products:
#                 product["category"] = query
#             add_products(products)
#             logger.info(f"✅ Added {len(products)} products for '{query}'")
#         return {"success": True, "products_count": len(products)}
#     except Exception as e:
#         logger.error(f"❌ Failed to scrape {query}: {e}")
#         return {"success": False, "error": str(e)}

# @app.task
# def scrape_major_categories():
#     logger.info("🔄 Running scheduled scraping task...")
#     for query in MAJOR_CATEGORIES:
#         logger.info(f"🔍 Scraping category: {query}")
#         try:
#             products = scrape_daraz(query, max_products=25)
#             existing_links = {p["link"] for p in products_collection.find({"category": query}, {"link": 1})}
#             new_products = [p for p in products if p["link"] not in existing_links]
#             if new_products:
#                 for product in new_products:
#                     product["category"] = query
#                 add_products(new_products)
#                 logger.info(f"✅ Added {len(new_products)} new products for '{query}'")
#             else:
#                 logger.info(f"ℹ️ No new products for '{query}'")
#         except Exception as e:
#             logger.error(f"❌ Failed to scrape {query}: {e}")

# @app.task
# def scrape_product_reviews_task(max_products: int = 10):
#     logger.info("🔄 Running review scraping task...")
#     try:
#         product_ids = get_recent_product_ids(limit=max_products)
#         results = []
#         driver = None
#         for product_id in product_ids:
#             try:
#                 if not driver:
#                     from scraper import create_driver
#                     driver = create_driver()
#                 product = products_collection.find_one({"_id": ObjectId(product_id)}, {"link": 1})
#                 if not product:
#                     continue
#                 reviews = scrape_product_reviews(driver, product["link"])
#                 add_reviews(product_id, reviews)
#                 results.append({"product_id": product_id, "reviews_count": len(reviews)})
#                 logger.info(f"✅ Scraped {len(reviews)} reviews for product {product_id}")
#             except Exception as e:
#                 results.append({"product_id": product_id, "error": str(e)})
#                 logger.error(f"❌ Failed to scrape reviews for {product_id}: {e}")
#         if driver:
#             driver.quit()
#         return {"success": True, "results": results}
#     except Exception as e:
#         logger.error(f"❌ Review scraping task failed: {e}")
#         return {"success": False, "error": str(e)}

# @app.task
# def compute_recommendations():
#     logger.info("🔄 Computing recommendations...")
#     try:
#         uuids = interactions_collection.distinct("uuid")
#         for uuid in uuids:
#             compute_recommendations_for_user(uuid)
#         logger.info(f"✅ Computed recommendations for {len(uuids)} users")
#     except Exception as e:
#         logger.error(f"❌ Failed to compute recommendations: {e}")