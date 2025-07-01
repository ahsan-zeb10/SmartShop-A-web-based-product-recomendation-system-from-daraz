from flask import Flask, request, jsonify
from flask_cors import CORS
from tasks import scrape_search_query
from celery.result import AsyncResult
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from scraper import scrape_daraz
from db import add_products, get_products_by_category, parse_category
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

@app.get("/api/search")
async def search_products(
    query: str = Query(..., description="Search term for Daraz products"),
    page: int = Query(1, ge=1, description="Page number to fetch")
):
    """API endpoint to search products on Daraz."""
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty.")
    
    logger.info(f"Received search query: {query}, page: {page}")
    
    try:
        # Start the scraping task asynchronously
        task = scrape_search_query.delay(query)
        
        # Check if we have existing products in the database
        category = parse_category(query)
        db_products = get_products_by_category(category, query=query, limit=20)
        
        if len(db_products) >= 4:
            logger.info(f"Returning {len(db_products)} products from database")
            return {
                "success": True,
                "data": db_products,
                "task_id": task.id,
                "message": "Scraping initiated in background"
            }
        
        # If not enough products in DB, scrape immediately
        logger.info("Scraping Daraz for products")
        scraped_products = scrape_daraz(query, max_products=5)
        if not scraped_products:
            logger.warning("No products found during scraping")
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "No products found."}
            )
        
        for product in scraped_products:
            product["category"] = category
        
        add_products(scraped_products)
        logger.info(f"Stored {len(scraped_products)} products in database")
        
        return {
            "success": True,
            "data": scraped_products,
            "task_id": task.id,
            "message": "Scraping initiated in background"
        }
    
    except Exception as e:
        logger.error(f"Error during API request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/api/search/status/{task_id}")
async def get_search_status(task_id: str):
    """Get the status of a search task."""
    try:
        task_result = AsyncResult(task_id)
        if task_result.ready():
            if task_result.successful():
                return {
                    "success": True,
                    "status": "completed",
                    "data": task_result.result
                }
            else:
                return {
                    "success": False,
                    "status": "failed",
                    "message": str(task_result.result)
                }
        else:
            return {
                "success": True,
                "status": "processing",
                "message": "Scraping in progress..."
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products")
async def get_products(category: str = Query(..., description="Category to fetch products for")):
    """API endpoint to get products by category."""
    try:
        logger.info(f"Fetching products for category: {category}")
        products = get_products_by_category(category)
        
        if not products:
            logger.info(f"No products found in database for category: {category}")
            # If no products in database, scrape them
            scraped_products = scrape_daraz(category, max_products=5)
            if not scraped_products:
                return JSONResponse(
                    status_code=404,
                    content={"success": False, "message": "No products found."}
                )
            
            for product in scraped_products:
                product["category"] = category
            
            add_products(scraped_products)
            return {"success": True, "data": scraped_products}
        
        return {"success": True, "data": products}
    
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)