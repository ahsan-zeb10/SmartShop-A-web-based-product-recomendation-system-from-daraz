from pymongo import MongoClient

client = MongoClient("mongodb+srv://ahtishamm2030:sham2030@fyp.mnymv.mongodb.net/?retryWrites=true&w=majority&appName=FYP")
db = client["FYP"]
products_collection = db["products"]

# Insert a test product
test_product = {
    "title": "Test Laptop",
    "price": "Rs 100,000",
    "image_url": "https://example.com/laptop.jpg",
    "link": "https://daraz.pk/laptop",
    "stars": 4,
    "category": "electronics"
}

result = products_collection.insert_one(test_product)
print(f"✅ Successfully inserted test product with ID: {result.inserted_id}")

# Fetch all products
products = list(products_collection.find({}))
if not products:
    print("❌ MongoDB is NOT storing products!")
else:
    print(f"✅ Found {len(products)} products in MongoDB!")
