from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from scraper import scrape_daraz
from db import add_products, products_collection, parse_category, add_user_interaction, get_user_recommendations
from tasks import scrape_search_query, scrape_product_reviews_task
from celery.result import AsyncResult
import logging
from bson import ObjectId
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InteractionData(BaseModel):
    type: str
    query: str | None = None
    product_id: str | None = None

@app.get("/api/search")
async def search_products(
    query: str = Query(..., description="Search term for Daraz products"),
    page: int = Query(1, ge=1, description="Page number to fetch"),
    limit: int = Query(20, ge=1, le=100, description="Number of products per page"),
    min_price: float = Query(None, description="Minimum price filter"),
    max_price: float = Query(None, description="Maximum price filter"),
    min_rating: float = Query(None, description="Minimum star rating"),
    min_reviews: int = Query(None, description="Minimum number of reviews")
):
    """API endpoint to search products on Daraz with filters and pagination."""
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty.")
    
    logger.info(f"Received search query: {query}, page: {page}, limit: {limit}, min_price: {min_price}, max_price: {max_price}, min_rating: {min_rating}, min_reviews: {min_reviews}")
    
    try:
        category = parse_category(query)
        logger.info(f"Parsed category: {category}")
        
        skip = (page - 1) * limit
        
        filter_query = {"category": category}
        if query:
            filter_query["title"] = {"$regex": query, "$options": "i"}
        if min_price is not None:
            filter_query["price"] = filter_query.get("price", {})
            filter_query["price"]["$gte"] = min_price
        if max_price is not None:
            filter_query["price"] = filter_query.get("price", {})
            filter_query["price"]["$lte"] = max_price
        if min_rating is not None:
            filter_query["stars"] = {"$gte": min_rating}
        if min_reviews is not None:
            filter_query["review_count"] = {"$gte": min_reviews}
        
        db_products = list(products_collection.find(filter_query).skip(skip).limit(limit))
        db_products = [{**p, "_id": str(p["_id"])} for p in db_products]
        
        if len(db_products) >= 4:
            logger.info(f"Returning {len(db_products)} products from database")
            return {"success": True, "data": db_products, "page": page, "limit": limit}
        
        logger.info("Initiating async scraping for products")
        task = scrape_search_query.delay(query, max_products=limit)
        return {"success": True, "message": "Scraping initiated.", "task_id": task.id}
    
    except Exception as e:
        logger.error(f"Error during API request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/api/search/status/{task_id}")
async def get_search_status(task_id: str):
    """Check status of a search scraping task."""
    try:
        task_result = AsyncResult(task_id)
        if task_result.ready():
            if task_result.successful():
                return {"success": True, "status": "completed", "data": task_result.result}
            else:
                return {"success": False, "status": "failed", "message": str(task_result.result)}
        return {"success": True, "status": "processing", "message": "Scraping in progress..."}
    except Exception as e:
        logger.error(f"Error checking task status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reviews")
async def trigger_review_scrape(
    product_id: str = Query(..., description="Product ID to scrape reviews for")
):
    """Trigger review scraping for a product."""
    try:
        product = products_collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        task = scrape_product_reviews_task.delay(max_products=1)
        return {"success": True, "message": "Review scraping initiated.", "task_id": task.id}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product ID")
    except Exception as e:
        logger.error(f"Error initiating review scrape: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reviews/status/{task_id}")
async def get_review_status(task_id: str):
    """Check status of a review scraping task."""
    try:
        task_result = AsyncResult(task_id)
        if task_result.ready():
            if task_result.successful():
                return {"success": True, "status": "completed", "data": task_result.result}
            else:
                return {"success": False, "status": "failed", "message": str(task_result.result)}
        return {"success": True, "status": "processing", "message": "Review scraping in progress..."}
    except Exception as e:
        logger.error(f"Error checking review task status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/compare")
async def compare_products(
    product_ids: str = Query(..., description="Comma-separated product IDs to compare")
):
    """Compare products by price, rating, and sentiment."""
    try:
        ids = [ObjectId(pid.strip()) for pid in product_ids.split(",")]
        products = list(products_collection.find({"_id": {"$in": ids}}))
        if not products:
            raise HTTPException(status_code=404, detail="No products found")
        
        comparison = [
            {
                "id": str(p["_id"]),
                "title": p["title"],
                "price": p["price"],
                "stars": p["stars"],
                "review_count": p["review_count"],
                "sentiment_score": p["sentiment_score"],
                "image_url": p["image_url"]
            } for p in products
        ]
        return {"success": True, "data": comparison}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid product IDs")
    except Exception as e:
        logger.error(f"Error comparing products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/interaction")
async def record_interaction(uuid: str, interaction: InteractionData):
    """Record a user interaction (search or click)."""
    try:
        add_user_interaction(uuid, interaction.type, interaction.dict(exclude_none=True))
        return {"success": True, "message": "Interaction recorded"}
    except Exception as e:
        logger.error(f"Error recording interaction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recommendations")
async def get_recommendations(uuid: str = Query(..., description="User UUID for recommendations")):
    """Fetch personalized product recommendations."""
    try:
        recommendations = get_user_recommendations(uuid, limit=10)
        return {"success": True, "data": recommendations}
    except Exception as e:
        logger.error(f"Error fetching recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def parse_price(price: str) -> float:
    """Convert price string to numeric value."""
    try:
        price = price.replace('Rs.', '').replace(',', '').strip()
        return float(price)
    except ValueError:
        return 0.0