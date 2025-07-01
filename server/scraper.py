# ##scraper.py
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import logging
# from sentiment import analyze_sentiment_batch
# import time
# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def create_driver():
#     """Initialize and return a Chrome WebDriver with optimized options."""
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--enable-unsafe-swiftshader")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-extensions")
#     options.add_argument("--start-maximized")
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     driver.implicitly_wait(2)
#     logger.info("Driver initialized")
#     return driver

# def scrape_product_reviews(driver, product_url):
#     """Scrape reviews from a product page with proper window management."""
#     main_window = driver.current_window_handle
#     logger.info(f"Main window handle: {main_window}")
    
#     driver.execute_script("window.open('');")
#     new_window = driver.window_handles[-1]
#     driver.switch_to.window(new_window)
#     logger.info(f"Switched to new window: {new_window}")
    
#     driver.get(product_url)
#     logger.info(f"Loading product URL: {product_url}")
    
#     reviews = []
#     scroll_attempts = 0
#     last_review_count = 0
    
#     try:
#         # Dismiss popups if present
#         try:
#             WebDriverWait(driver, 2).until(
#                 EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='close'], .next-dialog-close"))
#             ).click()
#             logger.info("Popup dismissed")
#         except:
#             logger.info("No popup found")
        
#         # Scroll to load reviews
#         while len(reviews) < 5 and scroll_attempts < 3:
#             driver.execute_script("window.scrollBy(0, 500)")
#             logger.info(f"Scrolled down, attempt {scroll_attempts + 1}")
            
#             try:
#                 WebDriverWait(driver, 2).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, ".mod-reviews .item"))
#                 )
#             except:
#                 logger.warning("Review elements not found, moving to next attempt")
#                 scroll_attempts += 1
#                 continue
            
#             review_elements = driver.find_elements(By.CSS_SELECTOR, ".mod-reviews .item")
#             logger.info(f"Found {len(review_elements)} review elements")
            
#             for elem in review_elements:
#                 try:
#                     reviewer_name_elem = elem.find_elements(By.CSS_SELECTOR, ".middle span")
#                     reviewer_name = reviewer_name_elem[0].text.strip() if reviewer_name_elem else "Anonymous"
#                     review_text = elem.find_element(By.CSS_SELECTOR, ".item-content").text.strip()
#                     stars = len(elem.find_elements(By.CSS_SELECTOR, ".starCtn img"))
                    
#                     if "Seller Response" not in review_text and len(reviews) < 5:
#                         reviews.append({
#                             "reviewer": reviewer_name,
#                             "rating": stars,
#                             "review": review_text
#                         })
#                         logger.info(f"Added review: {review_text[:50]}...")
#                 except Exception as e:
#                     logger.warning(f"Skipping invalid review: {str(e)}")
#                     continue
            
#             if len(reviews) == last_review_count:
#                 scroll_attempts += 1
#             else:
#                 last_review_count = len(reviews)
#                 scroll_attempts = 0
#             logger.info(f"Reviews collected: {len(reviews)}, Scroll attempts: {scroll_attempts}")
        
#         # Batch sentiment analysis
#         if reviews:
#             sentiments = analyze_sentiment_batch([r["review"] for r in reviews])
#             for review, sentiment in zip(reviews, sentiments):
#                 review["sentiment"] = float(sentiment)  # Ensure sentiment is a float
#             logger.info(f"Sentiment analysis completed for {len(reviews)} reviews")
    
#     except Exception as e:
#         logger.error(f"Review scraping failed for {product_url}: {str(e)}")
    
#     finally:
#         driver.close()
#         driver.switch_to.window(main_window)
#         logger.info(f"Closed review tab, switched back to main window: {main_window}")
    
#     return reviews[:5]

# # def extract_star_count(product):
# #     """Extract star rating for a product."""
# #     try:
# #         stars_element = product.find_elements(By.CSS_SELECTOR, '.mdmmT._32vUv i')
# #         return len([star for star in stars_element if 'Dy1nx' in star.get_attribute('class')])
# #     except Exception:
# #         return 0
# def extract_star_count(product):
#     """Extract star rating for a product, including fractional stars."""
#     try:
#         # First, try to get the average rating (e.g., 4.5)
#         rating_elem = product.find_element(By.CSS_SELECTOR, ".score .score-average")
#         rating = rating_elem.text.strip()
#         if rating and rating.replace('.', '', 1).isdigit():
#             return float(rating)
        
#         # If the average rating is not found, count the individual star images
#         star_elements = product.find_elements(By.CSS_SELECTOR, ".average .star")
#         filled_stars = len(star_elements)
        
#         # Estimate fractional stars (use width of container to determine)
#         if filled_stars:
#             return filled_stars  # This gives the count of full stars
        
#         return 0.0  # Return 0.0 if no stars are found

#     except Exception as e:
#         logger.error(f"Error extracting star count: {e}")
#         return 0.0



# def extract_review_count(product):
#     """Extract review count for a product."""
#     try:
#         review_count_element = product.find_element(By.CSS_SELECTOR, '.qzqFw')
#         return review_count_element.text.strip().replace("(", "").replace(")", "")
#     except Exception:
#         return "0 reviews"

# def scrape_daraz(query, max_products=5):
#     """Scrape Daraz product listings with reviews and sentiment analysis."""
#     driver = create_driver()
    
#     try:
#         search_url = f"https://www.daraz.pk/catalog/?q={query.replace(' ', '+')}"
#         driver.get(search_url)
#         logger.info(f"Loading search URL: {search_url}")
        
#         try:
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, "Bm3ON"))
#             )
#             logger.info("Search results loaded")
#         except:
#             logger.error("Failed to load search results")
#             return []
        
#         products = []
#         seen_items = set()
#         items = driver.find_elements(By.CLASS_NAME, "Bm3ON")[:max_products]
#         logger.info(f"Found {len(items)} product items")
        
#         for item in items:
#             try:
#                 title = item.find_element(By.CSS_SELECTOR, ".RfADt a").get_attribute("title")
#                 price = item.find_element(By.CSS_SELECTOR, ".ooOxS").text.strip()
#                 link = item.find_element(By.CSS_SELECTOR, ".RfADt a").get_attribute("href")
                
#                 # FIXED: ROBUST IMAGE EXTRACTION
#                 image_url = ""
#                 try:
#                     # First try the standard product image
#                     img = item.find_element(By.CSS_SELECTOR, ".picture-wrapper img")
#                     image_url = img.get_attribute("src") or img.get_attribute("data-src")
#                 except:
#                     try:
#                         # Try sponsored product image structure
#                         img = item.find_element(By.CSS_SELECTOR, ".image img")
#                         image_url = img.get_attribute("src") or img.get_attribute("data-src")
#                     except:
#                         try:
#                             # Try another common pattern
#                             img = item.find_element(By.CSS_SELECTOR, "[class*='image'] img")
#                             image_url = img.get_attribute("src") or img.get_attribute("data-src")
#                         except Exception as img_err:
#                             logger.warning(f"Image extraction failed: {img_err}")
                
#                 # If still no image, log the issue
#                 if not image_url:
#                     logger.warning(f"No image found for product: {title}")
                
#                 # FIXED: Extract actual numeric rating instead of star count
#                 stars = 0.0
#                 try:
#                     # Try to get rating from the new structure
#                     rating_element = item.find_element(By.CSS_SELECTOR, ".rating-ratings")
#                     style = rating_element.get_attribute("style")
                    
#                     # Extract rating from background-position
#                     if "background-position" in style:
#                         # Example: background-position: 0px -14px;
#                         position_y = style.split("background-position:")[1].split(";")[0].strip()
#                         y_value = int(position_y.split()[1].replace("px", ""))
                        
#                         # Calculate rating based on background position
#                         # Each star = 14px, rating = 5 - (position / star_height)
#                         star_height = 14
#                         rating_value = 5 + (y_value / star_height)
#                         stars = round(rating_value, 1)
#                     else:
#                         # Fallback to text content if background position not found
#                         rating_text = rating_element.text.strip()
#                         if rating_text:
#                             stars = float(rating_text)
#                 except Exception as e:
#                     logger.warning(f"Couldn't extract rating: {e}")
#                     try:
#                         # Alternative method: count stars from CSS classes
#                         star_elements = item.find_elements(By.CSS_SELECTOR, ".mdmmT._32vUv i")
#                         full_stars = len([star for star in star_elements if 'Dy1nx' in star.get_attribute('class')])
#                         half_star = 0.5 if any('half' in star.get_attribute('class') for star in star_elements) else 0
#                         stars = full_stars + half_star
#                     except:
#                         stars = 0.0
                
#                 review_count = extract_review_count(item)
                
#                 if (title, price) in seen_items:
#                     logger.info(f"Skipping duplicate product: {title}")
#                     continue
#                 seen_items.add((title, price))
                
#                 logger.info(f"Scraping reviews for product: {title}")
#                 reviews = scrape_product_reviews(driver, link)
                
#                 # Calculate sentiment score for the product
#                 sentiment_score = sum(r["sentiment"] for r in reviews) / len(reviews) if reviews else 0
                
#                 product_data = {
#                     "title": title,
#                     "price": price,
#                     "image_url": image_url,
#                     "link": link,
#                     "stars": stars,
#                     "review_count": review_count,
#                     "reviews": reviews,
#                     "sentiment_score": sentiment_score,
#                     "average_rating": sum(r['rating'] for r in reviews) / len(reviews) if reviews else 0,
#                     "positive_reviews": sum(1 for r in reviews if r['sentiment'] >= 4)
#                 }
#                 products.append(product_data)
#                 logger.info(f"Added product: {title}")
            
#             except Exception as e:
#                 logger.error(f"Error processing product: {str(e)}")
#                 continue
    
#     finally:
#         driver.quit()
#         logger.info("Driver closed")
    
#     return products

# =======================================================================================================
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import logging
# import re
# from sentiment import analyze_sentiment_batch
# import time
# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def create_driver():
#     """Initialize and return a Chrome WebDriver with optimized options."""
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-extensions")
#     options.add_argument("--start-maximized")
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     driver.implicitly_wait(2)
#     logger.info("Driver initialized")
#     return driver

# def scrape_product_reviews(driver, product_url):
#     """Scrape reviews from a product page with proper window management."""
#     main_window = driver.current_window_handle
#     logger.info(f"Main window handle: {main_window}")
    
#     driver.execute_script("window.open('');")
#     new_window = driver.window_handles[-1]
#     driver.switch_to.window(new_window)
#     logger.info(f"Switched to new window: {new_window}")
    
#     driver.get(product_url)
#     logger.info(f"Loading product URL: {product_url}")
    
#     reviews = []
#     scroll_attempts = 0
#     last_review_count = 0
    
#     try:
#         # Dismiss popups if present
#         try:
#             WebDriverWait(driver, 2).until(
#                 EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='close'], .next-dialog-close"))
#             ).click()
#             logger.info("Popup dismissed")
#         except:
#             logger.info("No popup found")
        
#         # Scroll to load reviews
#         while len(reviews) < 5 and scroll_attempts < 3:
#             driver.execute_script("window.scrollBy(0, 500)")
#             logger.info(f"Scrolled down, attempt {scroll_attempts + 1}")
            
#             try:
#                 WebDriverWait(driver, 2).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, ".mod-reviews .item"))
#                 )
#             except:
#                 logger.warning("Review elements not found, moving to next attempt")
#                 scroll_attempts += 1
#                 continue
            
#             review_elements = driver.find_elements(By.CSS_SELECTOR, ".mod-reviews .item")
#             logger.info(f"Found {len(review_elements)} review elements")
            
#             for elem in review_elements:
#                 try:
#                     reviewer_name_elem = elem.find_elements(By.CSS_SELECTOR, ".middle span")
#                     reviewer_name = reviewer_name_elem[0].text.strip() if reviewer_name_elem else "Anonymous"
#                     review_text = elem.find_element(By.CSS_SELECTOR, ".item-content").text.strip()
#                     stars = len(elem.find_elements(By.CSS_SELECTOR, ".starCtn img"))
                    
#                     if "Seller Response" not in review_text and len(reviews) < 5:
#                         reviews.append({
#                             "reviewer": reviewer_name,
#                             "rating": stars,
#                             "review": review_text
#                         })
#                         logger.info(f"Added review: {review_text[:50]}...")
#                 except Exception as e:
#                     logger.warning(f"Skipping invalid review: {str(e)}")
#                     continue
            
#             if len(reviews) == last_review_count:
#                 scroll_attempts += 1
#             else:
#                 last_review_count = len(reviews)
#                 scroll_attempts = 0
#             logger.info(f"Reviews collected: {len(reviews)}, Scroll attempts: {scroll_attempts}")
        
#         # Batch sentiment analysis
#         if reviews:
#             sentiments = analyze_sentiment_batch([r["review"] for r in reviews])
#             for review, sentiment in zip(reviews, sentiments):
#                 review["sentiment"] = float(sentiment)  # Ensure sentiment is a float
#             logger.info(f"Sentiment analysis completed for {len(reviews)} reviews")
    
#     except Exception as e:
#         logger.error(f"Review scraping failed for {product_url}: {str(e)}")
    
#     finally:
#         driver.close()
#         driver.switch_to.window(main_window)
#         logger.info(f"Closed review tab, switched back to main window: {main_window}")
    
#     return reviews[:5]

# def extract_star_count(product):
#     """Extract star rating for a product."""
#     try:
#         stars_element = product.find_elements(By.CSS_SELECTOR, '.mdmmT._32vUv i')
#         return len([star for star in stars_element if 'Dy1nx' in star.get_attribute('class')])
#     except Exception:
#         return 0

# def extract_review_count(product):
#     """Extract review count for a product."""
#     try:
#         review_count_element = product.find_element(By.CSS_SELECTOR, '.qzqFw')
#         return review_count_element.text.strip().replace("(", "").replace(")", "")
#     except Exception:
#         return "0 reviews"
# # def extract_product_image(item):
# #     """
# #     Specialized image extraction for Daraz that:
# #     1. Targets their specific image containers
# #     2. Gets the high-quality version of product images
# #     3. Skips all placeholder and Base64 images
# #     """
# #     # Daraz-specific image selectors in order of preference
# #     daraz_selectors = [
# #         ".gallery-preview-panel__image",  # Primary high-quality image
# #         ".pdp-mod-common-image",          # Common product image
# #         ".image-wrapper img[src*='drz.lazcdn']",  # Direct CDN link
# #         "img[src*='.webp']",              # Any webp image
# #         "img[src*='.jpg']",               # Any jpg image
# #     ]
    
# #     for selector in daraz_selectors:
# #         try:
# #             img = item.find_element(By.CSS_SELECTOR, selector)
            
# #             # Check both src and data-src attributes
# #             for attr in ["src", "data-src"]:
# #                 img_url = img.get_attribute(attr)
                
# #                 # Validate URL is a proper Daraz image
# #                 if (img_url and 
# #                     not img_url.startswith("data:image") and 
# #                     "placeholder" not in img_url.lower() and
# #                     ("drz.lazcdn" in img_url or ".webp" in img_url or ".jpg" in img_url)):
                    
# #                     # Remove any resize parameters to get highest quality
# #                     clean_url = img_url.split('_720x720q80')[0] if '_720x720q80' in img_url else img_url
# #                     logger.info(f"Found Daraz image using {selector}: {clean_url[:50]}...")
# #                     return clean_url
                    
# #         except Exception as e:
# #             logger.debug(f"Selector {selector} failed: {str(e)}")
# #             continue
    
# #     # Fallback to background-image CSS if needed
# #     try:
# #         wrapper = item.find_element(By.CSS_SELECTOR, ".image-wrapper, .gallery-preview-panel__content")
# #         style = wrapper.get_attribute("style")
# #         if style and "background-image" in style:
# #             match = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
# #             if match and "drz.lazcdn" in match.group(1):
# #                 clean_url = match.group(1).split('_720x720q80')[0] if '_720x720q80' in match.group(1) else match.group(1)
# #                 logger.info(f"Found background image: {clean_url[:50]}...")
# #                 return clean_url
# #     except Exception as e:
# #         logger.debug(f"Background image fallback failed: {str(e)}")
    
# #     logger.warning("No valid Daraz image found for product")
# #     return "https://via.placeholder.com/150?text=No+Image"
# def extract_product_image(item):
#     """
#     Robust image extraction for Daraz that handles all cases:
#     - Different image formats (avif, webp, png, jpg)
#     - Dynamic selectors
#     - Base64 images
#     - Quality parameters in URLs
#     """
#     # Prioritized list of selectors based on Daraz's structure
#     selectors = [
#         ".picture-wrapper img",  # Primary selector
#         ".image-wrapper img",     # Alternative wrapper
#         ".gallery-preview-panel__image",  # High-quality images
#         ".pdp-mod-common-image",  # Common product images
#         "img[src*='.avif']",     # Explicit AVIF format
#         "img[src*='.webp']",     # WEBP format
#         "img[src*='.png']",      # PNG format
#         "img[src*='.jpg']",      # JPG format
#     ]
    
#     for selector in selectors:
#         try:
#             img_element = item.find_element(By.CSS_SELECTOR, selector)
            
#             # Check all possible attributes in priority order
#             for attr in ["src", "data-src", "data-srcset", "data-original"]:
#                 img_url = img_element.get_attribute(attr)
                
#                 # Validate and clean the URL
#                 if img_url and not img_url.startswith("data:image"):
#                     # Remove size parameters to get original quality
#                     clean_url = re.sub(r'_\d+x\d+.*?\.', '.', img_url)
                    
#                     # Ensure it's a valid image URL
#                     if any(ext in clean_url for ext in ['.avif', '.webp', '.png', '.jpg', '.jpeg']):
#                         logger.info(f"Found valid image: {clean_url[:60]}...")
#                         return clean_url
#         except:
#             continue
    
#     # Fallback to background image extraction
#     try:
#         wrapper = item.find_element(By.CSS_SELECTOR, ".picture-wrapper, .image-wrapper")
#         style = wrapper.get_attribute("style")
#         if style and "background-image" in style:
#             match = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
#             if match:
#                 bg_url = match.group(1)
#                 clean_url = re.sub(r'_\d+x\d+.*?\.', '.', bg_url)
#                 if any(ext in clean_url for ext in ['.avif', '.webp', '.png', '.jpg', '.jpeg']):
#                     logger.info(f"Found background image: {clean_url[:60]}...")
#                     return clean_url
#     except:
#         pass
    
#     logger.warning("No valid image found, using placeholder")
#     return "https://via.placeholder.com/150?text=No+Image"


# def scrape_daraz(query, max_products=5):
#     """Scrape Daraz product listings with reviews and sentiment analysis."""
#     driver = create_driver()
    
#     try:
#         search_url = f"https://www.daraz.pk/catalog/?q={query.replace(' ', '+')}"
#         driver.get(search_url)
#         logger.info(f"Loading search URL: {search_url}")
        
#         # Wait for product items to be present
#         try:
#             WebDriverWait(driver, 5).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, "Bm3ON"))
#             )
#             logger.info("Search results loaded")
#         except:
#             logger.error("Failed to load search results")
#             return []
        
#         products = []
#         seen_items = set()
#         items = driver.find_elements(By.CLASS_NAME, "Bm3ON")[:max_products]
#         logger.info(f"Found {len(items)} product items")
        
#         for item in items:
#             try:
#                 # Scroll to the product to trigger image loading
#                 driver.execute_script("arguments[0].scrollIntoView();", item)
#                 time.sleep(1)  # Give lazy-loaded images a moment to load
                
#                 # Use the robust image extraction function
#                 image = extract_product_image(item)
                
#                 # Extract other product details
#                 title = item.find_element(By.CSS_SELECTOR, ".RfADt a").get_attribute("title")
#                 price = item.find_element(By.CSS_SELECTOR, ".ooOxS").text.strip()
#                 link = item.find_element(By.CSS_SELECTOR, ".RfADt a").get_attribute("href")
#                 stars = extract_star_count(item)
#                 review_count = extract_review_count(item)
                
#                 # Skip duplicates
#                 if (title, price) in seen_items:
#                     logger.info(f"Skipping duplicate product: {title}")
#                     continue
#                 seen_items.add((title, price))
                
#                 logger.info(f"Scraping reviews for product: {title}")
#                 reviews = scrape_product_reviews(driver, link)
                
#                 # Calculate sentiment score
#                 sentiment_score = sum(r["sentiment"] for r in reviews) / len(reviews) if reviews else 0
                
#                 # Compile product data
#                 product_data = {
#                     "title": title,
#                     "price": price,
#                     "image_url": image,
#                     "link": link,
#                     "stars": stars,
#                     "review_count": review_count,
#                     "reviews": reviews,
#                     "sentiment_score": sentiment_score,
#                     "average_rating": sum(r['rating'] for r in reviews) / len(reviews) if reviews else 0,
#                     "positive_reviews": sum(1 for r in reviews if r['sentiment'] >= 4)
#                 }
#                 products.append(product_data)
#                 logger.info(f"Added product: {title}")
            
#             except Exception as e:
#                 logger.error(f"Error processing product: {str(e)}")
#                 continue
    
#     finally:
#         driver.quit()
#         logger.info("Driver closed")
    
#     return products

# =========================================================================================


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import logging
# import re
# import time
# from sentiment import analyze_sentiment_batch

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def create_driver():
#     """Initialize and return a Chrome WebDriver with optimized options."""
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--enable-unsafe-swiftshader")  # Critical for headless mode
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-extensions")
#     options.add_argument("--start-maximized")
#     options.add_argument("--disable-software-rasterizer")
#     options.add_argument("--disable-setuid-sandbox")
#     options.add_argument("--disable-webgl")  # Disable WebGL to avoid errors
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     driver.implicitly_wait(5)  # Increase implicit wait for stability
#     logger.info("Driver initialized with GPU workarounds")
#     return driver

# def scrape_product_reviews(driver, product_url):
#     """Scrape reviews from a product page with proper window management."""
#     main_window = driver.current_window_handle
#     logger.info(f"Main window handle: {main_window}")
    
#     driver.execute_script("window.open('');")
#     new_window = driver.window_handles[-1]
#     driver.switch_to.window(new_window)
#     logger.info(f"Switched to new window: {new_window}")
    
#     driver.get(product_url)
#     logger.info(f"Loading product URL: {product_url}")
    
#     reviews = []
    
#     try:
#         # Dismiss popups if present
#         try:
#             WebDriverWait(driver, 3).until(
#                 EC.element_to_be_clickable((By.CSS_SELECTOR, "button.next-dialog-close, .mod-lead"))
#             ).click()
#             logger.info("Popup dismissed")
#         except:
#             logger.info("No popup found")
        
#         # Try to find reviews section
#         try:
#             # Wait for reviews section to be present
#             WebDriverWait(driver, 5).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, ".mod-reviews"))
#             )
#             logger.info("Reviews section found")
            
#             # Scroll to reviews section
#             reviews_section = driver.find_element(By.CSS_SELECTOR, ".mod-reviews")
#             driver.execute_script("arguments[0].scrollIntoView();", reviews_section)
#             time.sleep(1)
            
#             # Click "See All Reviews" if exists
#             try:
#                 see_all_button = driver.find_element(By.CSS_SELECTOR, ".pdp-review-container .next-btn.next-btn-normal.next-btn-medium")
#                 see_all_button.click()
#                 logger.info("Clicked 'See All Reviews'")
#                 time.sleep(2)
#             except:
#                 logger.info("No 'See All Reviews' button")
            
#             # Extract reviews
#             review_elements = driver.find_elements(By.CSS_SELECTOR, ".review-item")
#             logger.info(f"Found {len(review_elements)} review elements")
            
#             for elem in review_elements[:5]:  # Limit to 5 reviews
#                 try:
#                     reviewer_name = elem.find_element(By.CSS_SELECTOR, ".reviewer-name").text.strip()
#                     review_text = elem.find_element(By.CSS_SELECTOR, ".review-content").text.strip()
                    
#                     # Extract star rating
#                     star_elements = elem.find_elements(By.CSS_SELECTOR, ".star-full")
#                     stars = len(star_elements)
                    
#                     reviews.append({
#                         "reviewer": reviewer_name,
#                         "rating": stars,
#                         "review": review_text
#                     })
#                 except Exception as e:
#                     logger.warning(f"Skipping invalid review: {str(e)}")
#                     continue
#         except Exception as e:
#             logger.warning(f"No reviews section found for this product: {str(e)}")
        
#         # Batch sentiment analysis
#         if reviews:
#             sentiments = analyze_sentiment_batch([r["review"] for r in reviews])
#             for review, sentiment in zip(reviews, sentiments):
#                 review["sentiment"] = float(sentiment)
#             logger.info(f"Sentiment analysis completed for {len(reviews)} reviews")
    
#     except Exception as e:
#         logger.error(f"Review scraping failed for {product_url}: {str(e)}")
    
#     finally:
#         driver.close()
#         driver.switch_to.window(main_window)
#         logger.info(f"Closed review tab, switched back to main window: {main_window}")
    
#     return reviews

# def extract_star_count(product):
#     """Extract star rating for a product."""
#     try:
#         stars_element = product.find_elements(By.CSS_SELECTOR, '.mdmmT._32vUv i')
#         return len([star for star in stars_element if 'Dy1nx' in star.get_attribute('class')])
#     except Exception:
#         return 0

# def extract_review_count(product):
#     """Extract review count for a product."""
#     try:
#         review_count_element = product.find_element(By.CSS_SELECTOR, '.qzqFw')
#         return review_count_element.text.strip().replace("(", "").replace(")", "")
#     except Exception:
#         return "0 reviews"

# def extract_product_image(item):
#     """
#     Robust image extraction for Daraz that handles all cases:
#     1. Different image formats (avif, webp, png, jpg)
#     2. Dynamic selectors
#     3. Base64 images
#     4. Quality parameters in URLs
#     """
#     # Prioritized list of selectors based on Daraz's structure
#     selectors = [
#         ".picture-wrapper img",  # Primary selector
#         ".image-wrapper img",     # Alternative wrapper
#         ".gallery-preview-panel__image",  # High-quality images
#         ".pdp-mod-common-image",  # Common product images
#         "img[src*='.avif']",     # Explicit AVIF format
#         "img[src*='.webp']",     # WEBP format
#         "img[src*='.png']",      # PNG format
#         "img[src*='.jpg']",      # JPG format
#     ]
    
#     for selector in selectors:
#         try:
#             img_element = item.find_element(By.CSS_SELECTOR, selector)
            
#             # Check all possible attributes in priority order
#             for attr in ["src", "data-src", "data-srcset", "data-original"]:
#                 img_url = img_element.get_attribute(attr)
                
#                 # Validate and clean the URL
#                 if img_url and not img_url.startswith("data:image"):
#                     # Remove size parameters to get original quality
#                     clean_url = re.sub(r'_\d+x\d+.*?\.', '.', img_url)
                    
#                     # Ensure it's a valid image URL
#                     if any(ext in clean_url for ext in ['.avif', '.webp', '.png', '.jpg', '.jpeg']):
#                         logger.info(f"Found valid image: {clean_url[:60]}...")
#                         return clean_url
#         except:
#             continue
    
#     # Fallback to background image extraction
#     try:
#         wrapper = item.find_element(By.CSS_SELECTOR, ".picture-wrapper, .image-wrapper")
#         style = wrapper.get_attribute("style")
#         if style and "background-image" in style:
#             match = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
#             if match:
#                 bg_url = match.group(1)
#                 clean_url = re.sub(r'_\d+x\d+.*?\.', '.', bg_url)
#                 if any(ext in clean_url for ext in ['.avif', '.webp', '.png', '.jpg', '.jpeg']):
#                     logger.info(f"Found background image: {clean_url[:60]}...")
#                     return clean_url
#     except:
#         pass
    
#     logger.warning("No valid image found, using placeholder")
#     return "https://via.placeholder.com/150?text=No+Image"

# def scrape_daraz(query, max_products=5):
#     """Scrape Daraz product listings with reviews and sentiment analysis."""
#     driver = create_driver()
    
#     try:
#         search_url = f"https://www.daraz.pk/catalog/?q={query.replace(' ', '+')}"
#         driver.get(search_url)
#         logger.info(f"Loading search URL: {search_url}")
        
#         # Wait for results to load
#         try:
#             WebDriverWait(driver, 15).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, ".Bm3ON"))
#             )
#             logger.info("Search results loaded")
#         except Exception as e:
#             logger.error(f"Failed to load search results: {str(e)}")
#             return []
        
#         # Scroll to load all images
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(1.5)
        
#         products = []
#         seen_links = set()  # Track unique product links
#         items = driver.find_elements(By.CSS_SELECTOR, ".Bm3ON")
#         logger.info(f"Found {len(items)} product items")
        
#         for index, item in enumerate(items):
#             if len(products) >= max_products:
#                 break
                
#             try:
#                 # Scroll to each item to trigger lazy loading
#                 driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", item)
#                 time.sleep(0.3)
                
#                 link_element = item.find_element(By.CSS_SELECTOR, ".RfADt a")
#                 link = link_element.get_attribute("href")
                
#                 # Skip duplicates using product link
#                 if link in seen_links:
#                     logger.info(f"Skipping duplicate product: {link}")
#                     continue
#                 seen_links.add(link)
                
#                 title = link_element.get_attribute("title")
#                 price = item.find_element(By.CSS_SELECTOR, ".ooOxS").text.strip()
                
#                 # Use the robust image extraction function
#                 image = extract_product_image(item)
                
#                 stars = extract_star_count(item)
#                 review_count = extract_review_count(item)
                
#                 logger.info(f"Processing product {index+1}: {title}")
                
#                 # Scrape reviews
#                 reviews = []
#                 try:
#                     reviews = scrape_product_reviews(driver, link)
#                 except Exception as e:
#                     logger.error(f"Review scraping failed: {str(e)}")
                
#                 # Calculate sentiment score for the product
#                 sentiment_score = sum(r["sentiment"] for r in reviews) / len(reviews) if reviews else 0
                
#                 product_data = {
#                     "title": title,
#                     "price": price,
#                     "image_url": image,
#                     "link": link,
#                     "stars": stars,
#                     "review_count": review_count,
#                     "reviews": reviews,
#                     "sentiment_score": sentiment_score,
#                     "average_rating": sum(r['rating'] for r in reviews) / len(reviews) if reviews else 0,
#                     "positive_reviews": sum(1 for r in reviews if r['sentiment'] >= 4)
#                 }
#                 products.append(product_data)
#                 logger.info(f"Added product: {title}")
            
#             except Exception as e:
#                 logger.error(f"Error processing product: {str(e)}")
#                 continue
    
#     finally:
#         driver.quit()
#         logger.info("Driver closed")
    
#     return products

#  this below is working code for image ok but not for rating

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging
import re
from sentiment import analyze_sentiment_batch
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_driver():
    """Initialize and return a Chrome WebDriver with optimized options."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(2)
    logger.info("Driver initialized")
    return driver

def scrape_product_reviews(driver, product_url):
    """Scrape reviews from a product page with proper window management."""
    main_window = driver.current_window_handle
    logger.info(f"Main window handle: {main_window}")
    
    driver.execute_script("window.open('');")
    new_window = driver.window_handles[-1]
    driver.switch_to.window(new_window)
    logger.info(f"Switched to new window: {new_window}")
    
    driver.get(product_url)
    logger.info(f"Loading product URL: {product_url}")
    
    reviews = []
    scroll_attempts = 0
    last_review_count = 0
    
    try:
        # Dismiss popups if present
        try:
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='close'], .next-dialog-close"))
            ).click()
            logger.info("Popup dismissed")
        except:
            logger.info("No popup found")
        
        # Scroll to load reviews
        while len(reviews) < 5 and scroll_attempts < 3:
            driver.execute_script("window.scrollBy(0, 500)")
            logger.info(f"Scrolled down, attempt {scroll_attempts + 1}")
            
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".mod-reviews .item"))
                )
            except:
                logger.warning("Review elements not found, moving to next attempt")
                scroll_attempts += 1
                continue
            
            review_elements = driver.find_elements(By.CSS_SELECTOR, ".mod-reviews .item")
            logger.info(f"Found {len(review_elements)} review elements")
            
            for elem in review_elements:
                try:
                    reviewer_name_elem = elem.find_elements(By.CSS_SELECTOR, ".middle span")
                    reviewer_name = reviewer_name_elem[0].text.strip() if reviewer_name_elem else "Anonymous"
                    review_text = elem.find_element(By.CSS_SELECTOR, ".item-content").text.strip()
                    stars = len(elem.find_elements(By.CSS_SELECTOR, ".starCtn img"))
                    
                    if "Seller Response" not in review_text and len(reviews) < 5:
                        reviews.append({
                            "reviewer": reviewer_name,
                            "rating": stars,
                            "review": review_text
                        })
                        logger.info(f"Added review: {review_text[:50]}...")
                except Exception as e:
                    logger.warning(f"Skipping invalid review: {str(e)}")
                    continue
            
            if len(reviews) == last_review_count:
                scroll_attempts += 1
            else:
                last_review_count = len(reviews)
                scroll_attempts = 0
            logger.info(f"Reviews collected: {len(reviews)}, Scroll attempts: {scroll_attempts}")
        
        # Batch sentiment analysis
        if reviews:
            sentiments = analyze_sentiment_batch([r["review"] for r in reviews])
            for review, sentiment in zip(reviews, sentiments):
                review["sentiment"] = float(sentiment)  # Ensure sentiment is a float
            logger.info(f"Sentiment analysis completed for {len(reviews)} reviews")
    
    except Exception as e:
        logger.error(f"Review scraping failed for {product_url}: {str(e)}")
    
    finally:
        driver.close()
        driver.switch_to.window(main_window)
        logger.info(f"Closed review tab, switched back to main window: {main_window}")
    
    return reviews[:5]

# def extract_star_count(product):
#     """Extract star rating for a product."""
#     try:
#         stars_element = product.find_elements(By.CSS_SELECTOR, '.mdmmT._32vUv i')
#         return len([star for star in stars_element if 'Dy1nx' in star.get_attribute('class')])
#     except Exception:
#         return 0
def extract_star_count(product):
    """Extract star rating with decimal precision from search results"""
    try:
        # Count full and half stars using the actual classes from Daraz search results
        full_stars = len(product.find_elements(By.CSS_SELECTOR, '.mdmmT._32vUv i.Dy1nx'))  # Full stars
        half_stars = len(product.find_elements(By.CSS_SELECTOR, '.mdmmT._32vUv i.half-star'))  # Half stars
        
        # Calculate rating with decimal precision
        rating = full_stars + (half_stars * 0.5)
        logger.info(f"Extracted rating: {rating} (full: {full_stars}, half: {half_stars})")
        return rating
        
    except Exception as e:
        # Fallback method - try to parse the rating text
        try:
            rating_text = product.find_element(By.CSS_SELECTOR, '.ratings-content').text
            rating = float(rating_text)
            logger.info(f"Extracted rating from text: {rating}")
            return rating
        except:
            logger.error(f"Star count extraction error: {str(e)}")
            return 0.0
# def extract_rating(driver):
#     """
#     Extract the product's average rating from a Daraz product page.
    
#     Args:
#         driver: Selenium WebDriver instance with the product page loaded.
    
#     Returns:
#         float: The rating (e.g., 4.4), or 0.0 if extraction fails.
#     """
#     try:
#         # Wait up to 10 seconds for the rating element to appear
#         # We will try multiple selectors to make sure we find the correct element
#         rating_element = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".score-average, .product-rating .rating-value"))
#         )
        
#         # Get the rating text, strip any excess whitespace
#         rating_text = rating_element.text.strip()
        
#         if rating_text:
#             # Try to parse the rating as a float
#             try:
#                 rating = float(rating_text)
#                 logger.info(f"Extracted rating: {rating}")
#                 return rating
#             except ValueError:
#                 logger.warning(f"Failed to convert rating text to float: {rating_text}")
#                 return 0.0
#         else:
#             logger.warning("Rating text is empty")
#             return 0.0
#     except Exception as e:
#         logger.warning(f"Failed to extract rating: {str(e)}")
#         return 0.0


def extract_review_count(product):
    """Extract review count for a product."""
    try:
        review_count_element = product.find_element(By.CSS_SELECTOR, '.qzqFw')
        return review_count_element.text.strip().replace("(", "").replace(")", "")
    except Exception:
        return "0 reviews"

def extract_product_image(item, driver):
    """
    Extract the product image URL reliably.
    """
    try:
        # Scroll to the item to trigger lazy loading
        driver.execute_script("arguments[0].scrollIntoView();", item)
        time.sleep(0.5)  # Quick pause for loading
        
        # Try multiple selectors to find the image
        img_element = None
        possible_selectors = [
            ".picture-wrapper img",  # Adjust based on Daraz’s HTML
            ".image-wrapper img",
            "img[src*='drz.lazcdn']",
            "img[data-src*='drz.lazcdn']",
            "img"  # Fallback to any img tag
        ]
        
        for selector in possible_selectors:
            try:
                img_element = item.find_element(By.CSS_SELECTOR, selector)
                if img_element:
                    logger.info(f"Found image with selector: {selector}")
                    break
            except:
                continue
        
        if not img_element:
            logger.warning("No image element found in this item")
            return "https://via.placeholder.com/150?text=No+Image"
        
        # Wait for a real image URL (not a base64 placeholder)
        WebDriverWait(driver, 5).until(
            lambda d: img_element.get_attribute("src") and not img_element.get_attribute("src").startswith("data:")
        )
        
        # Get the image URL
        img_url = img_element.get_attribute("src")
        
        # Check for lazy-loaded fallback
        if img_url.startswith("data:") or "placeholder" in img_url.lower():
            img_url = img_element.get_attribute("data-src") or img_url
        
        # Only clean the URL if it has size parameters
        if "_400x400" in img_url or "_720x720" in img_url:
            img_url = re.sub(r'_\d+x\d+.*?\.', '.', img_url)
        
        logger.info(f"Extracted image URL: {img_url[:50]}...")
        return img_url
    
    except Exception as e:
        logger.warning(f"Image extraction failed: {str(e)}")
        return "https://via.placeholder.com/150?text=No+Image"

def scrape_daraz(query, max_products=5):
    """Scrape Daraz product listings with reviews and sentiment analysis."""
    driver = create_driver()
    
    try:
        search_url = f"https://www.daraz.pk/catalog/?q={query.replace(' ', '+')}"
        driver.get(search_url)
        logger.info(f"Loading search URL: {search_url}")
        
        # Wait for product items to be present
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "Bm3ON"))
            )
            logger.info("Search results loaded")
        except:
            logger.error("Failed to load search results")
            return []
        
        products = []
        seen_items = set()
        items = driver.find_elements(By.CLASS_NAME, "Bm3ON")[:max_products]
        logger.info(f"Found {len(items)} product items")
        
        for item in items:
            try:
                image = extract_product_image(item, driver)
                
                title = item.find_element(By.CSS_SELECTOR, ".RfADt a").get_attribute("title")
                price = item.find_element(By.CSS_SELECTOR, ".ooOxS").text.strip()
                link = item.find_element(By.CSS_SELECTOR, ".RfADt a").get_attribute("href")
                stars = extract_star_count(item)
                review_count = extract_review_count(item)
                
                # Skip duplicates
                if (title, price) in seen_items:
                    logger.info(f"Skipping duplicate product: {title}")
                    continue
                seen_items.add((title, price))
                
                logger.info(f"Scraping reviews for product: {title}")
                reviews = scrape_product_reviews(driver, link)
                
                # Calculate sentiment score
                sentiment_score = sum(r["sentiment"] for r in reviews) / len(reviews) if reviews else 0
                
                product_data = {
                    "title": title,
                    "price": price,
                    "image_url": image,
                    "link": link,
                    "stars": stars,
                    "review_count": review_count,
                    "reviews": reviews,
                    "sentiment_score": sentiment_score,
                    "average_rating": sum(r['rating'] for r in reviews) / len(reviews) if reviews else 0,
                    "positive_reviews": sum(1 for r in reviews if r['sentiment'] >= 4)
                }
                products.append(product_data)
                logger.info(f"Added product: {title}")
            
            except Exception as e:
                logger.error(f"Error processing product: {str(e)}")
                continue
    
    finally:
        driver.quit()
        logger.info("Driver closed")
    
    return products

# Example usage
if __name__ == "__main__":
    query = "infinix smart 9"
    products = scrape_daraz(query, max_products=5)
    for product in products:
        print(f"Title: {product['title']}")
        print(f"Image URL: {product['image_url']}")
        print("-" * 50)


