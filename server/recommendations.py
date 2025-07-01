from db import get_products_by_category
from user_interactions import get_user_interactions
import logging

logger = logging.getLogger(__name__)

def get_recommendations(uuid, limit=8):
    """
    Generate personalized recommendations based on user interactions.
    """
    try:
        logger.info(f"Getting recommendations for user {uuid}")
        
        # Get user's recent interactions
        interactions = get_user_interactions(uuid)
        logger.info(f"Found {len(interactions)} interactions for user {uuid}")
        
        if not interactions:
            logger.info(f"No interactions found for user {uuid}, returning popular products")
            # If no interactions, return popular products from electronics category
            popular_products = get_products_by_category("electronics", limit=limit)
            logger.info(f"Returning {len(popular_products)} popular products")
            return popular_products
        
        # Extract categories and products from interactions
        categories = {}
        product_ids = set()
        
        for interaction in interactions:
            if interaction.get('type') == 'search':
                category = interaction.get('category')
                if category:
                    categories[category] = categories.get(category, 0) + 1
            elif interaction.get('type') == 'click':
                product_ids.add(interaction.get('product_id'))
        
        logger.info(f"Found categories: {categories}")
        logger.info(f"Found product_ids: {product_ids}")
        
        # Get products from most frequent categories
        recommended_products = []
        for category, _ in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            products = get_products_by_category(category, limit=limit)
            recommended_products.extend(products)
            logger.info(f"Added {len(products)} products from category {category}")
            
            if len(recommended_products) >= limit:
                break
        
        # If we don't have enough recommendations, add popular products
        if len(recommended_products) < limit:
            popular_products = get_products_by_category("electronics", limit=limit - len(recommended_products))
            recommended_products.extend(popular_products)
            logger.info(f"Added {len(popular_products)} popular products to reach limit")
        
        # Remove duplicates and limit to requested number
        seen_ids = set()
        unique_products = []
        for product in recommended_products:
            if product['_id'] not in seen_ids and product['_id'] not in product_ids:
                seen_ids.add(product['_id'])
                unique_products.append(product)
            if len(unique_products) >= limit:
                break
        
        logger.info(f"Returning {len(unique_products)} unique recommendations")
        return unique_products[:limit]
    
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        # Return popular products as fallback
        popular_products = get_products_by_category("electronics", limit=limit)
        logger.info(f"Returning {len(popular_products)} popular products as fallback")
        return popular_products 