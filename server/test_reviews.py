from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fetch_reviews(product_url, max_reviews=5):
    """Scrapes 5 customer reviews from a Daraz product page with rating and reviewer name."""
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    try:
        driver.set_page_load_timeout(30)
        driver.get(product_url)
        print("Page loaded successfully")

        # Dismiss popups if present
        try:
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='close'], .next-dialog-close"))
            ).click()
            print("Dismissed popup")
        except:
            pass

        reviews = []
        scroll_attempts = 0
        last_review_count = 0

        while len(reviews) < max_reviews and scroll_attempts < 10:
            # Scroll down to load more reviews
            driver.execute_script("window.scrollBy(0, 500)")
            time.sleep(2)

            # Ensure the review section is loaded
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".mod-reviews .item"))
                )
            except:
                pass

            # Extract reviews
            review_elements = driver.find_elements(By.CSS_SELECTOR, ".mod-reviews .item")

            for review_element in review_elements:
                try:
                    # Extract reviewer name
                    reviewer_name_element = review_element.find_elements(By.CSS_SELECTOR, ".middle span")
                    reviewer_name = reviewer_name_element[0].text.strip() if reviewer_name_element else "Anonymous"

                    # Extract review text
                    review_text = review_element.find_element(By.CSS_SELECTOR, ".item-content").text.strip()

                    # Extract rating (count stars)
                    stars = len(review_element.find_elements(By.CSS_SELECTOR, ".starCtn img"))

                    # Skip seller responses
                    if "Seller Response" in review_text:
                        continue

                    # Add valid review to list
                    reviews.append({
                        "reviewer": reviewer_name,
                        "rating": stars,
                        "review": review_text
                    })

                    if len(reviews) >= max_reviews:
                        break

                except Exception as e:
                    print(f"Skipping invalid review: {e}")
                    continue

            # Stop scrolling if no new reviews are found
            if len(reviews) == last_review_count:
                scroll_attempts += 1
            else:
                scroll_attempts = 0
                last_review_count = len(reviews)

        return reviews if reviews else ["No valid reviews found"]

    except Exception as e:
        return [f"Error: {str(e)}"]

    finally:
        driver.quit()

# Test execution
if __name__ == "__main__":
    url = "https://www.daraz.pk/products/a05-4-gb-64-gb-8-mp-4-mp-500-mah-i466115711.html"
    reviews = fetch_reviews(url)
    print("\nVerified Reviews (JSON Array):")
    print(reviews)
