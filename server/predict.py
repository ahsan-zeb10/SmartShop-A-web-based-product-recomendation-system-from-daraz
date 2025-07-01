import joblib
import re

# Load the trained model and vectorizer
model = joblib.load("./models/roman_urdu_sentiment_model.pkl")
vectorizer = joblib.load("./models/roman_urdu_vectorizer.pkl")

# Kaggle preprocessing functions (same as in train_model.py)
def cleaner(word):
    word = re.sub(r'\#\.', '', word)
    word = re.sub(r'\n', '', word)
    word = re.sub(r',', '', word)
    word = re.sub(r'\-', ' ', word)
    word = re.sub(r'\.', '', word)
    word = re.sub(r'\\', ' ', word)
    word = re.sub(r'\\x\.+', '', word)
    word = re.sub(r'\d', '', word)
    word = re.sub(r'^_.', '', word)
    word = re.sub(r'_', ' ', word)
    word = re.sub(r'^ ', '', word)
    word = re.sub(r' $', '', word)
    word = re.sub(r'\?', '', word)
    return word.lower()

def array_cleaner(array):
    X = []
    for sentence in array:
        clean_sentence = ''
        words = str(sentence).split(' ')
        for word in words:
            clean_sentence = clean_sentence + ' ' + cleaner(word)
        X.append(clean_sentence)
    return X

# Test the model on new text
test_texts = [
    "Sai kha ya her kisi kay bus ki bat nhi hai",  # Positive example
    "Yeh bohat bura hai",  # Negative example
    "Theek hai, koi khas baat nahi",  # Neutral example
]

# Preprocess the test texts
cleaned_texts = array_cleaner(test_texts)

# Vectorize the test texts
X_test = vectorizer.transform(cleaned_texts)

# Predict sentiments
predictions = model.predict(X_test)

# Print results
for text, prediction in zip(test_texts, predictions):
    print(f"Text: {text}")
    print(f"Predicted Sentiment: {prediction}\n")