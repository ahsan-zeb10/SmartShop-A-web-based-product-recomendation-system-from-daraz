# from db import interactions_collection, recommendations_collection, products_collection
# from bson import ObjectId
# import logging
# import time
# from typing import List, Optional

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def record_interaction(
#     uuid: str,
#     action: str,
#     query: Optional[str] = None,
#     product_id: Optional[str] = None,
#     category: Optional[str] = None
# ) -> None:
#     """Record a user interaction (search, click, view)."""
#     try:
#         interaction = {
#             "uuid": uuid,
#             "action": action,
#             "timestamp": time.time()
#         }
#         if query:
#             interaction["query"] = query
#         if product_id:
#             interaction["product_id"] = ObjectId(product_id)
#         if category:
#             interaction["category"] = category
#         interactions_collection.insert_one(interaction)
#         logger.debug(f"Recorded interaction: {action} for UUID {uuid}")
#     except Exception as e:
#         logger.error(f"Error recording interaction: {str(e)}")
#         raise

# def get_user_interactions(uuid: str, limit: int = 100) -> List[dict]:
#     """Retrieve recent interactions for a user."""
#     try:
#         interactions = interactions_collection.find({"uuid": uuid}).sort("timestamp", -1).limit(limit)
#         return list(interactions)
#     except Exception as e:
#         logger.error(f"Error fetching interactions for UUID {uuid}: {str(e)}")
#         return []

# def compute_recommendations_for_user(uuid: str) -> List[str]:
#     """Compute recommendations for a user based on interactions."""
#     try:
#         interactions = get_user_interactions(uuid)
#         if not interactions:
#             logger.info(f"No interactions found for UUID {uuid}")
#             return []
        
#         # Score categories based on interaction type
#         category_scores = {}
#         for interaction in interactions:
#             category = interaction.get("category")
#             if not category:
#                 continue
#             action = interaction["action"]
#             score = 3 if action == "click" else 2 if action == "view" else 1  # Click > View > Search
#             category_scores[category] = category_scores.get(category, 0) + score
        
#         # Get top 3 categories
#         top_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)[:3]
#         top_categories = [cat[0] for cat in top_categories]
        
#         # Fetch products from top categories with high sentiment
#         product_ids = []
#         for category in top_categories:
#             products = products_collection.find(
#                 {"category": category, "sentiment_score": {"$gte": 0.5}}
#             ).sort("sentiment_score", -1).limit(5)
#             product_ids.extend([str(p["_id"]) for p in products])
        
#         if product_ids:
#             recommendations_collection.update_one(
#                 {"uuid": uuid},
#                 {"$set": {
#                     "product_ids": [ObjectId(pid) for pid in product_ids],
#                     "updated_at": time.time()
#                 }},
#                 upsert=True
#             )
#             logger.info(f"Saved {len(product_ids)} recommendations for UUID {uuid}")
#         return product_ids
#     except Exception as e:
#         logger.error(f"Error computing recommendations for UUID {uuid}: {str(e)}")
#         return []

# def get_recommendations(uuid: str) -> List[dict]:
#     """Retrieve recommended products for a user."""
#     try:
#         rec = recommendations_collection.find_one({"uuid": uuid})
#         if not rec:
#             return []
#         products = products_collection.find({"_id": {"$in": rec["product_ids"]}})
#         return [{**p, "_id": str(p["_id"])} for p in products]
#     except Exception as e:
#         logger.error(f"Error fetching recommendations for UUID {uuid}: {str(e)}")
#         return []