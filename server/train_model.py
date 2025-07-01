# train_model.py

# Imports from the Kaggle notebook
# import logging
# import numpy as np
# import pandas as pd
# import joblib
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import SGDClassifier

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Define paths
# DATASET_PATH = "./models/RomanUrduDataSet.csv"  
# MODEL_PATH = "./models/roman_urdu_sentiment_model.pkl"
# VECTORIZER_PATH = "./models/roman_urdu_vectorizer.pkl"

# # Load dataset with proper encoding
# logger.info("Loading dataset...")
# try:
#     data = pd.read_csv(DATASET_PATH, header=None, names=['text', 'sentiment'], encoding="utf-8")
# except UnicodeDecodeError:
#     data = pd.read_csv(DATASET_PATH, header=None, names=['text', 'sentiment'], encoding="ISO-8859-1")

# # Replace NaN values instead of dropping them
# data['text'] = data['text'].fillna("").astype(str)
# data['sentiment'] = data['sentiment'].fillna("").astype(str)

# # Clean sentiment labels
# data['sentiment'] = data['sentiment'].str.strip().str.lower()

# # Clean text column (remove unwanted characters)
# def clean_text(text):
#     return text.encode("ascii", "ignore").decode("utf-8")  # Removes non-ASCII characters

# data['text'] = data['text'].apply(clean_text)

# # Verify unique sentiment labels
# logger.info(f"Unique sentiments: {data['sentiment'].unique()}")

# # Extract features and labels
# X = data['text']
# y = data['sentiment']

# # Vectorization
# logger.info("Vectorizing data...")
# vectorizer = TfidfVectorizer(sublinear_tf=True, ngram_range=(1, 3), max_df=0.5)
# X_train = vectorizer.fit_transform(X)

# # Train the model with increased iterations
# logger.info("Training model...")
# clf = SGDClassifier(alpha=0.0001, max_iter=1000, penalty="elasticnet", tol=1e-3)
# clf.fit(X_train, y)

# # Save the model and vectorizer
# logger.info("Saving model and vectorizer...")
# joblib.dump(clf, MODEL_PATH)
# joblib.dump(vectorizer, VECTORIZER_PATH)
# logger.info(f"Model saved to {MODEL_PATH}")
# logger.info(f"Vectorizer saved to {VECTORIZER_PATH}")

import os
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
import joblib
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define paths
DATASET_PATH = "./models/RomanUrduDataSet.csv"
MODEL_PATH = "./models/roman_urdu_sentiment_model.pkl"
VECTORIZER_PATH = "./models/roman_urdu_vectorizer.pkl"

# Kaggle preprocessing functions
def cleaner(word):
    """
    Clean a word by removing unwanted characters while preserving sentiment indicators.
    
    Args:
        word (str): The word to clean.
    
    Returns:
        str: The cleaned word in lowercase.
    """
    word = re.sub(r'\#\.', '', word)
    word = re.sub(r'\n', '', word)
    word = re.sub(r'\-', ' ', word)
    word = re.sub(r'\\', ' ', word)
    word = re.sub(r'\\x\.+', '', word)
    # Keep numbers, as they might indicate sentiment (e.g., "5 stars")
    word = re.sub(r'^_.', '', word)
    word = re.sub(r'_', ' ', word)
    word = re.sub(r'^ ', '', word)
    word = re.sub(r' $', '', word)
    return word.lower()

def array_cleaner(array):
    """
    Clean an array of sentences by applying the cleaner function to each word.
    
    Args:
        array (list): List of sentences to clean.
    
    Returns:
        list: List of cleaned sentences.
    """
    X = []
    for sentence in array:
        clean_sentence = ''
        words = str(sentence).split(' ')
        for word in words:
            clean_sentence = clean_sentence + ' ' + cleaner(word)
        X.append(clean_sentence)
    return X

# Manual loading of the dataset
logger.info("Loading dataset...")
texts = []
sentiments = []
valid_sentiments = ['positive', 'negative', 'neutral']

with open(DATASET_PATH, 'r', encoding='ISO-8859-1') as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        # Skip metadata lines
        if any(invalid in line for invalid in ['----------------', '----------', '-------', '------', '9090', 'till here']):
            continue
        # Find the last occurrence of a sentiment label
        matches = list(re.finditer(r'(Positive|Negative|Neutral)', line, re.IGNORECASE))
        if matches:
            last_match = matches[-1]  # Get the last match
            sentiment = last_match.group(0).lower()
            # Extract text as everything before the last sentiment label
            text = line[:last_match.start()].strip()
            if text and sentiment in valid_sentiments:
                texts.append(text)
                sentiments.append(sentiment)

# Create DataFrame
data = pd.DataFrame({'text': texts, 'sentiment': sentiments})

# Normalize text before removing duplicates
data['normalized_text'] = array_cleaner(data['text'])
# Remove duplicates based on normalized text
data = data.drop_duplicates(subset=['normalized_text'])
print("\nDataset shape after removing duplicates:", data.shape)

# Define refined keyword lists for sentiment validation
positive_keywords = ['wah', 'sahi', 'achha', 'khubiya', 'shukriya', 'maza', 'kamaal', 'zabardast', 'shandaar', 'bemisaal', 'zenda']
negative_keywords = ['dukh', 'lanat', 'tabah', 'bura', 'zalim', 'nakami', 'ghatiya', 'bhenchod', 'afsos', 'jahalat', 'galt', 'badmashi']
neutral_keywords = ['hakeqat', 'naseeb', 'shak', 'theek', 'hona', 'kiya', 'kabhi', 'intezar', 'mutazkira']

# Function to check if text contains keywords
def contains_keywords(text, keywords):
    text = text.lower()
    return any(keyword in text for keyword in keywords)

# Function to determine dominant sentiment based on keywords
def determine_sentiment(text):
    pos_score = sum(1 for keyword in positive_keywords if keyword in text.lower())
    neg_score = sum(1 for keyword in negative_keywords if keyword in text.lower())
    neu_score = sum(1 for keyword in neutral_keywords if keyword in text.lower())
    
    if pos_score > neg_score and pos_score > neu_score:
        return 'positive'
    elif neg_score > pos_score and neg_score > neu_score:
        return 'negative'
    else:
        return 'neutral'

# Flag and relabel mislabeled examples
data['is_mislabeled'] = False
data['new_sentiment'] = data['sentiment']
for idx, row in data.iterrows():
    text = row['normalized_text']
    sentiment = row['sentiment']
    if sentiment == 'positive' and contains_keywords(text, negative_keywords):
        data.at[idx, 'is_mislabeled'] = True
        data.at[idx, 'new_sentiment'] = determine_sentiment(text)
    elif sentiment == 'negative' and contains_keywords(text, positive_keywords):
        data.at[idx, 'is_mislabeled'] = True
        data.at[idx, 'new_sentiment'] = determine_sentiment(text)
    elif sentiment == 'neutral' and (contains_keywords(text, positive_keywords) or contains_keywords(text, negative_keywords)):
        # Allow some overlap for neutral, but relabel if strongly positive/negative
        if contains_keywords(text, positive_keywords) and contains_keywords(text, negative_keywords):
            data.at[idx, 'is_mislabeled'] = True
            data.at[idx, 'new_sentiment'] = determine_sentiment(text)
        elif contains_keywords(text, positive_keywords):
            data.at[idx, 'is_mislabeled'] = True
            data.at[idx, 'new_sentiment'] = 'positive'
        elif contains_keywords(text, negative_keywords):
            data.at[idx, 'is_mislabeled'] = True
            data.at[idx, 'new_sentiment'] = 'negative'

# Print mislabeled examples for inspection
print("\nMislabeled Examples (up to 20):\n", data[data['is_mislabeled']][['text', 'sentiment', 'new_sentiment']].head(20))

# Update sentiment labels
data['sentiment'] = data['new_sentiment']
data = data.drop(columns=['normalized_text', 'is_mislabeled', 'new_sentiment'])

# Verify initial data loading
print("First 10 rows:\n", data.head(10))
print("\nDataset shape:", data.shape)
print("\nMissing values:\n", data.isna().sum())
print("\nUnique Sentiments:", data['sentiment'].unique())
print("\nClass Distribution:\n", data['sentiment'].value_counts())

# Inspect more examples from each class to check for remaining issues
print("\nSample Negative Examples (20):\n", data[data['sentiment'] == 'negative'].head(20))
print("\nSample Neutral Examples (20):\n", data[data['sentiment'] == 'neutral'].head(20))
print("\nSample Positive Examples (20):\n", data[data['sentiment'] == 'positive'].head(20))

# Check if dataset is empty
if data.empty:
    raise ValueError("Dataset is empty after cleaning. Check the dataset content.")

# Remove rows with NaN in 'text' or 'sentiment'
original_shape = data.shape
data = data.dropna(subset=['text', 'sentiment'])
logger.info(f"Removed {original_shape[0] - data.shape[0]} rows with NaN values")

# Split the dataset into training and test sets
X = data['text']
y = data['sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Apply Kaggle's preprocessing
logger.info("Cleaning text data...")
X_train = array_cleaner(X_train)
X_test = array_cleaner(X_test)

# Vectorize the text data
logger.info("Vectorizing data...")
vectorizer = TfidfVectorizer(sublinear_tf=True, ngram_range=(1, 3), max_df=0.5)
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

# Compute class weights to handle imbalance
class_counts = y_train.value_counts()
total_samples = len(y_train)
class_weights = {label: total_samples / (len(class_counts) * count) for label, count in class_counts.items()}
print("\nClass Weights:", class_weights)

# Train the model with hyperparameter tuning
logger.info("Training model with hyperparameter tuning...")
param_grid = {'C': [0.1, 1, 10]}
clf = GridSearchCV(LinearSVC(penalty='l2', dual=False, tol=1e-3, class_weight=class_weights, max_iter=1000), 
                   param_grid, cv=5, scoring='f1_macro')
clf.fit(X_train, y_train)
print("\nBest parameters:", clf.best_params_)

# Evaluate the model
logger.info("Evaluating model...")
y_pred = clf.predict(X_test)
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save the model and vectorizer
logger.info("Saving model and vectorizer...")
joblib.dump(clf.best_estimator_, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)
logger.info(f"Model saved to {MODEL_PATH}")
logger.info(f"Vectorizer saved to {VECTORIZER_PATH}")