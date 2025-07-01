# from fastapi import FastAPI, Query, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from scraper import scrape_daraz
# from db import add_products, get_products_by_category, parse_category
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Initialize FastAPI app
# app = FastAPI()

# # Enable CORS for frontend access
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/api/products")
# async def get_products(category: str = Query(..., description="Category to fetch products for")):
#     """API endpoint to get products by category."""
#     try:
#         logger.info(f"Fetching products for category: {category}")
#         products = get_products_by_category(category)
        
#         if not products:
#             logger.info(f"No products found in database for category: {category}")
#             # If no products in database, scrape them
#             scraped_products = scrape_daraz(category, max_products=5)
#             if not scraped_products:
#                 return JSONResponse(
#                     status_code=404,
#                     content={"success": False, "message": "No products found."}
#                 )
            
#             for product in scraped_products:
#                 product["category"] = category
            
#             add_products(scraped_products)
#             return {"success": True, "data": scraped_products}
        
#         return {"success": True, "data": products}
    
#     except Exception as e:
#         logger.error(f"Error fetching products: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# @app.get("/api/search")
# async def search_products(
#     query: str = Query(..., description="Search term for Daraz products"),
#     page: int = Query(1, ge=1, description="Page number to fetch")
# ):
#     """API endpoint to search products on Daraz."""
#     if not query.strip():
#         raise HTTPException(status_code=400, detail="Query parameter cannot be empty.")
    
#     logger.info(f"Received search query: {query}, page: {page}")
    
#     try:
#         category = parse_category(query)
#         logger.info(f"Parsed category: {category}")
        
#         # First check database with the actual query
#         db_products = get_products_by_category(category, query=query, limit=20)
        
#         if len(db_products) >= 4:
#             logger.info(f"Returning {len(db_products)} products from database")
#             return {"success": True, "data": db_products}
        
#         logger.info("Scraping Daraz for products")
#         scraped_products = scrape_daraz(query, max_products=5)
#         if not scraped_products:
#             logger.warning("No products found during scraping")
#             return JSONResponse(
#                 status_code=404,
#                 content={"success": False, "message": "No products found."}
#             )
        
#         for product in scraped_products:
#             product["category"] = category
#             logger.debug(f"Product to store: {product}")
        
#         add_products(scraped_products)
#         logger.info(f"Stored {len(scraped_products)} products in database")
        
#         logger.info("Returning scraped products")
#         return {"success": True, "data": scraped_products}
    
#     except Exception as e:
#         logger.error(f"Error during API request: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=5000) 



from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from db import add_products, get_products_by_category, get_product_by_id  # Ensure proper import from db
import logging
from scraper import scrape_daraz
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

# Simple category parsing function (mock implementation)
def parse_category(query: str):
    """
    A basic function to parse categories. This is just a mock version.
    It assumes that the entire query is a category, but you can extend it as needed.
    """
    return query.strip()

# Recommendation endpoint with proper registration
@app.get("/api/recommendation")
async def get_recommendations(
    categories: str = Query("", alias="categories"), 
    productIds: str = Query("", alias="productIds")
):
    """API endpoint to get product recommendations"""
    try:
        # Validate parameters
        if not categories and not productIds:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Missing parameters"}
            )
        
        # Parse parameters
        category_list = [c.strip() for c in categories.split(",") if c.strip()] if categories else []
        product_id_list = [pid.strip() for pid in productIds.split(",") if pid.strip()] if productIds else []
        
        logger.info(f"Fetching recommendations: categories={category_list}, productIds={product_id_list}")
        
        # Fetch products
        related_products = []
        seen_ids = set()

        # Fetch by categories
        if category_list:
            for category in category_list:
                products = get_products_by_category(category)  # Only fetch products by category
                for product in products:
                    if product["_id"] not in seen_ids:
                        seen_ids.add(product["_id"])
                        related_products.append(product)

        # Fetch by product IDs
        if product_id_list:
            for product_id in product_id_list:
                # Use a different function to get products by ID
                product = get_product_by_id(product_id)  # Fetch product by ID
                if product and product["_id"] not in seen_ids:
                    seen_ids.add(product["_id"])
                    related_products.append(product)

        return {"success": True, "data": related_products}
    
    except Exception as e:
        logger.error(f"Recommendation error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Internal server error: {str(e)}"}
        )

# Search endpoint
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
        category = parse_category(query)
        logger.info(f"Parsed category: {category}")
        
        # First check database with the actual query
        db_products = get_products_by_category(category, query=query, limit=20)
        
        if len(db_products) >= 4:
            logger.info(f"Returning {len(db_products)} products from database")
            return {"success": True, "data": db_products}
        
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
            logger.debug(f"Product to store: {product}")
        
        add_products(scraped_products)
        logger.info(f"Stored {len(scraped_products)} products in database")
        
        logger.info("Returning scraped products")
        return {"success": True, "data": scraped_products}
    
    except Exception as e:
        logger.error(f"Error during API request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
