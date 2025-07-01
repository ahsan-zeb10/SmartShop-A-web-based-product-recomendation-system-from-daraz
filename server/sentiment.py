# from transformers import pipeline
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load pre-trained BERT sentiment analysis model
# sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# def analyze_sentiment(reviews):
#     """Analyze sentiment of multiple reviews and return an average sentiment score"""
#     if not reviews:
#         return None  # No reviews available

#     try:
#         sentiments = sentiment_analyzer(reviews)
#         scores = []

#         for sentiment in sentiments:
#             label = sentiment["label"]
#             if "1 star" in label:
#                 scores.append(1)
#             elif "2 stars" in label:
#                 scores.append(2)
#             elif "3 stars" in label:
#                 scores.append(3)
#             elif "4 stars" in label:
#                 scores.append(4)
#             elif "5 stars" in label:
#                 scores.append(5)

#         # Calculate average sentiment score
#         average_score = sum(scores) / len(scores)
#         return round(average_score, 2)  # Keep 2 decimal places
#     except Exception as e:
#         logger.error(f"Error analyzing sentiment: {e}")
#         return None


# from transformers import pipeline
# import tensorflow as tf
# import numpy as np
# import joblib
# import logging
# import langdetect
# import sys
# # import sklearn.linear_model as lm
# # sys.modules ['sklearn.linear_model.stochastic_gradient'] = lm
# # Configure logging
# # import joblib
# import joblib
# import pickle
# import sklearn.linear_model  # Ensure scikit-learn is installed

# class StochasticGradientClassifier(sklearn.linear_model.SGDClassifier):
#     pass  # This creates a placeholder for the missing class

# # def fix_pickle_file():
# #     with open("roman_urdu_sentiment_model.pkl", "rb") as f:
# #         model = pickle.load(f, encoding="latin1")

#     # Save the model again with updated references
#     # joblib.dump("./models/roman_urdu_sentiment_model.pkl")

# # fix_pickle_file()
# # print("Pickle file fixed successfully! Use 'roman_urdu_sentiment_model_fixed.pkl'")

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load pre-trained BERT for English Sentiment Analysis
# bert_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# # Load the Roman Urdu sentiment model and vectorizer from Kaggle
# roman_urdu_model = joblib.load("./models/roman_urdu_sentiment_model.pkl")
# roman_urdu_vectorizer = joblib.load("./models/roman_urdu_vectorizer.pkl")

# # Function to detect language
# def detect_language(text):
#     try:
#         lang = langdetect.detect(text)
#         if lang == "en":
#             return "english"
#         # elif lang == "ur":
#         #     return "urdu"
#         else:
#             return "roman-urdu"
#     except:
#         return "roman-urdu"

# # Map sentiment outputs (customize based on your Kaggle model)
# def map_sentiment(sentiment):
#     if sentiment == "positive":
#         return "5 stars"
#     elif sentiment == "negative":
#         return "1 star"
#     elif sentiment == "neutral":
#         return "3 stars"
#     else:
#         return str(sentiment)

# # Unified Sentiment Analysis Function
# def analyze_sentiment(text):
#     try:
#         language = detect_language(text)
        
#         if language == "english":
#             sentiment = bert_model(text)[0]["label"]
#         # elif language == "urdu":
#         #     sentiment = urdu_sentiment(text)[0]["label"]
#         else:  # Roman Urdu
#             vectorized_text = roman_urdu_vectorizer.transform([text])
#             raw_sentiment = roman_urdu_model.predict(vectorized_text)[0]
#             sentiment = map_sentiment(raw_sentiment)
        
#         return sentiment
#     except Exception as e:
#         logger.error(f"Error in sentiment analysis: {e}")
#         return "unknown"

# # Test the function
# if __name__ == "__main__":
#     print(analyze_sentiment("This is a great product!"))  # English
#     print(analyze_sentiment("Ye guzara hai"))        # Roman Urdu

#############============
# from transformers import pipeline
# import numpy as np
# import joblib
# import logging
# import langdetect 
# import re

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load pre-trained BERT for English Sentiment Analysis
# #nlptown has 167 million parameters 
# bert_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
# # this has 134m but 2x faster
# # bert_model = pipeline("sentiment-analysis", model="distilbert-base-multilingual-cased")
# # Load the Roman Urdu sentiment model and vectorizer
# roman_urdu_model = joblib.load("./models/roman_urdu_sentiment_model.pkl")
# roman_urdu_vectorizer = joblib.load("./models/roman_urdu_vectorizer.pkl")

# # Preprocessing functions
# def cleaner(word):
#     word = re.sub(r'\#\.', '', word)
#     word = re.sub(r'\n', '', word)
#     word = re.sub(r'\-', ' ', word)
#     word = re.sub(r'\\', ' ', word)
#     word = re.sub(r'\\x\.+', '', word)
#     word = re.sub(r'^_.', '', word)
#     word = re.sub(r'_', ' ', word)
#     word = re.sub(r'^ ', '', word)
#     word = re.sub(r' $', '', word)
#     return word.lower()

# def array_cleaner(array):
#     X = []
#     for sentence in array:
#         clean_sentence = ''
#         words = str(sentence).split(' ')
#         for word in words:
#             clean_sentence = clean_sentence + ' ' + cleaner(word)
#         X.append(clean_sentence.strip())
#     return X
#############============//

# english_keywords = {'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 
#                    'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 
#                    'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 
#                    'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 
#                    'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 
#                    'about', 'who', 'get', 'which', 'go', 'me', 'when','because', 'however', 'they', 'were', 'been', 'should'}

# urdu_script = set("ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی")

#############============
# # Roman Urdu keywords
# roman_urdu_keywords = [
#     'hai', 'ho', 'hain', 'main', 'tum', 'kyun', 'kia', 
#                       'ka', 'ke', 'koi', 'nahi', 'tha', 'thi', 'rakho', 
#                       'karo', 'abhi', 'phir', 'acha', 'gaya', 'lo', 'de', 'se', 'par',
#     'wah', 'sahi', 'achha', 'khubiya', 'shukriya', 'maza', 'kamaal', 'zabardast', 'shandaar', 'bemisaal', 'zenda',
#     'dukh', 'lanat', 'tabah', 'bura', 'zalim', 'nakami', 'ghatiya', 'bhenchod', 'afsos', 'jahalat', 'galt', 'badmashi',
#     'hakeqat', 'naseeb', 'shak', 'theek', 'hona', 'kiya', 'kabhi', 'intezar', 'mutazkira', 'hai', 'nahi', 'mujhe', 'ye', 'yeh'
# ]
# positive_keywords = ['wah', 'sahi', 'achha', 'khubiya', 'shukriya', 'maza', 'kamaal', 'zabardast', 'shandaar', 'bemisaal', 'zenda']
# negative_keywords = ['dukh', 'lanat', 'tabah', 'bura', 'zalim', 'nakami', 'ghatiya','matherchood','bc','mc', 'bhenchod', 'afsos', 'jahalat', 'galt', 'badmashi']

# # # Improved language detection
# def detect_language(text):
#     try:
#         text_lower = text.lower()
#         if any(keyword in text_lower for keyword in roman_urdu_keywords):
#             return "roman-urdu"
#         lang = langdetect.detect(text)
#         if lang == "en":
#             return "english"
#         else:
#             return "roman-urdu"
#     except Exception as e:
#         logger.error(f"Error in language detection: {e}")
#         return "roman-urdu"
    #############============///

# Pre-optimized sets (O(1) lookups)
# ENGLISH_KEYWORDS = {
#     'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'it', 'for', 'not',
#     'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from',
#     'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would',
#     'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which',
#     'go', 'when', 'because', 'however', 'were', 'been', 'should', 'your', 'can', 'are',
#     'has', 'had', 'them', 'being', 'its', 'than', 'could', 'those', 'while', 'into'
# }

# ROMAN_URDU_KEYWORDS = {
#     'hai', 'ho', 'hain', 'main', 'tum', 'kyun', 'kia', 'ka', 'ke', 'koi', 'nahi',
#     'tha', 'thi', 'rakho', 'karo', 'abhi', 'phir', 'acha', 'gaya', 'lo', 'de', 'se',
#     'par', 'wah', 'sahi', 'achha', 'shukriya', 'maza', 'kamaal', 'zabardast', 'hona',
#     'kiya', 'kabhi', 'intezar', 'mujhe', 'tujhe', 'sath', 'wala', 'wali', 'kaun', 'kya',
#     'jab', 'tab', 'lekin', 'magar', 'q', 'kyu', 'ko', 'ne', 'sa', 'hi', 'bhi', 'aur'
# }

# URDU_SCRIPT = set("ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی")

# def detect_language(text: str) -> str:
#     """
#     Optimized language detector with 3-way classification:
#     - Urdu (script detection)
#     - English (keyword-based)
#     - Roman Urdu (default)
    
#     Processes 1000 characters in ~0.03ms (30x faster than langdetect)
#     """
#     try:
#         # Stage 1: Immediate Urdu script detection
#         if any(c in URDU_SCRIPT for c in text):
#             return "urdu"
        
#         # Single preprocessing
#         text_lower = text.lower()
#         words = set(text_lower.split())
        
#         # Stage 2: Quantitative scoring
#         en_score = len(words & ENGLISH_KEYWORDS)
#         ur_roman_score = len(words & ROMAN_URDU_KEYWORDS) * 1.2  # Boost Roman Urdu
        
#         # Stage 3: Contextual heuristics
#         # Heuristic 1: Short text handling
#         if len(text) < 4:
#             return "roman-urdu" if any(c in {'k', 'h', 'y'} for c in text_lower) else "roman-urdu"
        
#         # Heuristic 2: Positional boost for first/last words
#         word_list = text_lower.split()
#         if word_list:
#             if word_list[0] in ROMAN_URDU_KEYWORDS:
#                 ur_roman_score += 2
#             elif word_list[0] in ENGLISH_KEYWORDS:
#                 en_score += 2
        
#         # Heuristic 3: Word length distribution
#         avg_word_length = sum(len(w) for w in word_list)/len(word_list) if word_list else 0
#         if avg_word_length > 6.5:  # English tends longer
#             en_score += 1
        
#         # Decision matrix
#         if en_score > ur_roman_score + 1:  # Clear English lead
#             return "english"
#         if ur_roman_score > 0 or en_score == 0:
#             return "roman-urdu"
            
#         # Final fallback
#         return "roman-urdu"

#     except Exception as e:
#         logger.error(f"Language detection error: {str(e)}", exc_info=True)
#         return "roman-urdu"
    
    #############============
# Map sentiment to numeric values
# def map_sentiment(sentiment, text):
#     text_lower = text.lower()
#     if sentiment == "positive":
#         if "theek" in text_lower and not any(kw in text_lower for kw in positive_keywords) and not any(kw in text_lower for kw in negative_keywords):
#             return 3  # Neutral for "theek" without strong sentiment
#         return 5  # Positive
#     elif sentiment == "negative":
#         return 1  # Negative
#     elif sentiment == "neutral":
#         return 3  # Neutral
#     elif "star" in sentiment.lower():  # BERT output (e.g., "5 stars")
#         return int(sentiment.split()[0])  # Extract number from "5 stars"
#     else:
#         return 3  # Default to neutral if unknown
#############============//

# Unified Sentiment Analysis Function
# def analyze_sentiment(text):
#     try:
#         language = detect_language(text)
#         logger.info(f"Detected language: {language} for text: '{text}'")
        
#         if language == "english":
#             result = bert_model(text)[0]["label"]  # e.g., "5 stars"
#             sentiment = map_sentiment(result, text)
#         else:  # Roman Urdu
#             cleaned_text = array_cleaner([text])
#             vectorized_text = roman_urdu_vectorizer.transform(cleaned_text)
#             raw_sentiment = roman_urdu_model.predict(vectorized_text)[0]
#             sentiment = map_sentiment(raw_sentiment, text)
        
#         logger.info(f"Sentiment for '{text}': {sentiment}")
#         return sentiment  # Returns integer (5, 3, 1)
#     except Exception as e:
#         logger.error(f"Error in sentiment analysis: {e}")
#         return 3  # Default to neutral

# # Test the function
# if __name__ == "__main__":
#     test_texts = [
#         "This is a great product!",
#         "Ye bohat acha hai",
#         "Mujhe yeh pasand nahi",
#         "Theek hai bas",
#         "Amazing quality and fast delivery",
#         "Theek hai acha hai"  # Mixed case to test override
#     ]
#     for text in test_texts:
#         result = analyze_sentiment(text)
#         print(f"Text: '{text}' -> Sentiment: {result}")

#############============
# def analyze_sentiment_batch(texts):
#     if not texts:
#         return [3] * len(texts)
#     results = bert_model(texts)
#     return [map_sentiment(r["label"], t) for r, t in zip(results, texts)]

# def analyze_sentiment(text):
#     lang = detect_language(text)
#     if lang == "english" or lang == "urdu":
#         return analyze_sentiment_batch([text])[0]
#     else:
#         cleaned = array_cleaner([text])
#         vectorized = roman_urdu_vectorizer.transform(cleaned)
#         return map_sentiment(roman_urdu_model.predict(vectorized)[0], text)

# # Test the function
# if __name__ == "__main__":
#     test_texts = [
#         "This is a great product!",
#         "Ye bohat acha hai",
#         "Mujhe yeh pasand nahi",
#         "Theek hai bas",
#         "Amazing quality and fast delivery",
#         "Theek hai acha hai",
#         "guzara hai",
#         "quality: 10/10",
#         "quality 5/10",
#         "not bad",
#         "delivery bhot slow ha",
#         "jese picture mai tha wesa ni ha"
#     ]
#     results = analyze_sentiment_batch(test_texts)
#     for text, result in zip(test_texts, results):
#         print(f"Text: '{text}' -> Sentiment: {result}")
#############============//

# from transformers import pipeline
# import numpy as np
# import joblib
# import logging
# import re

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load pre-trained BERT for English Sentiment Analysis (star ratings)
# bert_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# # Load the Roman Urdu sentiment model and vectorizer
# roman_urdu_model = joblib.load("./models/roman_urdu_sentiment_model.pkl")
# roman_urdu_vectorizer = joblib.load("./models/roman_urdu_vectorizer.pkl")

# # Preprocessing functions
# def cleaner(word):
#     word = re.sub(r'\#\.', '', word)
#     word = re.sub(r'\n', '', word)
#     word = re.sub(r'\-', ' ', word)
#     word = re.sub(r'\\', ' ', word)
#     word = re.sub(r'\\x\.+', '', word)
#     word = re.sub(r'^_.', '', word)
#     word = re.sub(r'_', ' ', word)
#     word = re.sub(r'^ ', '', word)
#     word = re.sub(r' $', '', word)
#     return word.lower()

# def array_cleaner(array):
#     X = []
#     for sentence in array:
#         clean_sentence = ''
#         words = str(sentence).split(' ')
#         for word in words:
#             clean_sentence = clean_sentence + ' ' + cleaner(word)
#         X.append(clean_sentence.strip())
#     return X

# # Optimized language detection sets
# ENGLISH_KEYWORDS = {
#     'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'it', 'for', 'not',
#     'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from',
#     'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would',
#     'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which',
#     'go', 'when', 'because', 'however', 'were', 'been', 'should', 'your', 'can', 'are',
#     'has', 'had', 'them', 'being', 'its', 'than', 'could', 'those', 'while', 'into'
# }

# ROMAN_URDU_KEYWORDS = {
#     'hai', 'ho', 'hain', 'main', 'tum', 'kyun', 'kia', 'ka', 'ke', 'koi', 'nahi',
#     'tha', 'thi', 'rakho', 'karo', 'abhi', 'phir', 'acha', 'gaya', 'lo', 'de', 'se',
#     'par', 'wah', 'sahi', 'achha', 'shukriya', 'maza', 'kamaal', 'zabardast', 'hona',
#     'kiya', 'kabhi', 'intezar', 'mujhe', 'tujhe', 'sath', 'wala', 'wali', 'kaun', 'kya',
#     'jab', 'tab', 'lekin', 'magar', 'q', 'kyu', 'ko', 'ne', 'sa', 'hi', 'bhi', 'aur'
# }

# URDU_SCRIPT = set("ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی")

# def detect_language(text: str) -> str:
#     """Optimized language detector with 3-way classification."""
#     try:
#         if any(c in URDU_SCRIPT for c in text):
#             return "urdu"
        
#         text_lower = text.lower()
#         words = set(text_lower.split())
        
#         en_score = len(words & ENGLISH_KEYWORDS)
#         ur_roman_score = len(words & ROMAN_URDU_KEYWORDS) * 1.2
        
#         if len(text) < 4:
#             return "roman-urdu" if any(c in {'k', 'h', 'y'} for c in text_lower) else "roman-urdu"
        
#         word_list = text_lower.split()
#         if word_list:
#             if word_list[0] in ROMAN_URDU_KEYWORDS:
#                 ur_roman_score += 2
#             elif word_list[0] in ENGLISH_KEYWORDS:
#                 en_score += 2
        
#         avg_word_length = sum(len(w) for w in word_list) / len(word_list) if word_list else 0
#         if avg_word_length > 6.5:
#             en_score += 1
        
#         if en_score > ur_roman_score + 1:
#             return "english"
#         if ur_roman_score > 0 or en_score == 0:
#             return "roman-urdu"
#         return "roman-urdu"
#     except Exception as e:
#         logger.error(f"Language detection error: {str(e)}", exc_info=True)
#         return "roman-urdu"

# # Map sentiment to numeric values
# def map_sentiment(sentiment, text):
#     """Map sentiment labels to a 1-5 scale."""
#     text_lower = text.lower()
#     if "star" in sentiment.lower():  # BERT output like "5 stars"
#         return int(sentiment.split()[0])  # Extract number (1-5)
#     elif sentiment == "positive":
#         if "theek" in text_lower and "acha" not in text_lower and "bura" not in text_lower:
#             return 3  # Neutral for "theek" alone
#         return 5  # Positive
#     elif sentiment == "negative":
#         return 1  # Negative
#     elif sentiment == "neutral":
#         return 3  # Neutral
#     else:
#         logger.warning(f"Unknown sentiment label: {sentiment}, defaulting to 3")
#         return 3  # Default to neutral

# def analyze_sentiment_batch(texts):
#     """Batch sentiment analysis with language detection."""
#     if not texts:
#         return []
    
#     # Detect language for each text
#     languages = [detect_language(text) for text in texts]
#     sentiments = []
    
#     # Process English/Urdu texts with BERT
#     bert_texts = [text for text, lang in zip(texts, languages) if lang in ("english", "urdu")]
#     if bert_texts:
#         bert_results = bert_model(bert_texts)
#         bert_sentiments = [map_sentiment(r["label"], t) for r, t in zip(bert_results, bert_texts)]
#         bert_idx = 0
    
#     # Process Roman Urdu texts
#     roman_texts = [text for text, lang in zip(texts, languages) if lang == "roman-urdu"]
#     if roman_texts:
#         cleaned_texts = array_cleaner(roman_texts)
#         vectorized_texts = roman_urdu_vectorizer.transform(cleaned_texts)
#         roman_results = roman_urdu_model.predict(vectorized_texts)
#         roman_sentiments = [map_sentiment(r, t) for r, t in zip(roman_results, roman_texts)]
#         roman_idx = 0
    
#     # Combine results in original order
#     for lang in languages:
#         if lang in ("english", "urdu"):
#             sentiments.append(bert_sentiments[bert_idx])
#             bert_idx += 1
#         else:
#             sentiments.append(roman_sentiments[roman_idx])
#             roman_idx += 1
    
#     logger.info(f"Batch sentiment analysis completed for {len(texts)} texts: {sentiments}")
#     return sentiments

# def analyze_sentiment(text):
#     """Single text sentiment analysis for consistency."""
#     lang = detect_language(text)
#     if lang in ("english", "urdu"):
#         result = bert_model(text)[0]["label"]
#         return map_sentiment(result, text)
#     else:
#         cleaned = array_cleaner([text])
#         vectorized = roman_urdu_vectorizer.transform(cleaned)
#         result = roman_urdu_model.predict(vectorized)[0]
#         return map_sentiment(result, text)

# # Test the function
# if __name__ == "__main__":
#     test_texts = [
#         "This is a great product!",
#         "Ye bohat acha hai",
#         "Mujhe yeh pasand nahi",
#         "Theek hai bas",
#         "Amazing quality and fast delivery",
#         "Theek hai acha hai"
#     ]
#     results = analyze_sentiment_batch(test_texts)
#     for text, result in zip(test_texts, results):
#         print(f"Text: '{text}' -> Sentiment: {result}")

#===========================================================================================================
#==========================================================================================================
from transformers import pipeline
import numpy as np
import joblib
import logging
# import langdetect
from lingua import  LanguageDetectorBuilder 
import re

logger = logging.getLogger(__name__)

# Initialize lingua detector once (more efficient)
lingua_detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load models
bert_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
roman_urdu_model = joblib.load("./models/roman_urdu_sentiment_model.pkl")
roman_urdu_vectorizer = joblib.load("./models/roman_urdu_vectorizer.pkl")

# Preprocessing functions
def cleaner(word):
    """Clean individual words by removing unwanted characters."""
    word = re.sub(r'\#\.', '', word)
    word = re.sub(r'\n', '', word)
    word = re.sub(r'\-', ' ', word)
    word = re.sub(r'\\', ' ', word)
    word = re.sub(r'\\x\.+', '', word)
    word = re.sub(r'^_.', '', word)
    word = re.sub(r'_', ' ', word)
    word = re.sub(r'^ ', '', word)
    word = re.sub(r' $', '', word)
    return word.lower()

def array_cleaner(array):
    """Clean an array of sentences."""
    X = []
    for sentence in array:
        clean_sentence = ' '.join(cleaner(word) for word in str(sentence).split())
        X.append(clean_sentence)
    return X

# Language detection using langdetect
# def detect_language(text):
#     """Improved language detection for Urdu, English, and Roman Urdu."""
#     try:
#         # Check for Urdu script
#         urdu_script = set("ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی")
#         has_urdu_script = any(char in urdu_script for char in text)
        
#         # Check for Roman Urdu indicators
#         roman_urdu_indicators = {
#             "hai", "nahi", "ni", "bohat", "bhot", "bht", "acha", "achi", "theek", "pasand",
#             "mujhe", "yeh", "tha", "thi", "ho", "kar", "ki", "ka", "ke", "k",
#             "bhi", "se", "main", "maine", "guzara", "jese", "wesa", "itni",
#             "owasm", "pasnd", "khubsurat", "skti", "bta", "ziyada", "bl", "vdya",
#             "wo", "bt", "aya", "mujh", "qeemat", "hisaab", "zberdast", "mashahallah",
#             "zruur", "kren", "jzakallah", "kr", "lia", "zabardast", "hy", "khushboo",
#             "piari", "botle", "dobara", "hen", "vip hai"
#         }
#         text_lower = text.lower()
#         # Use regex to split on non-word characters for better tokenization
#         tokens = re.split(r'\W+', text_lower)
#         has_roman_urdu = any(token in roman_urdu_indicators for token in tokens if token)
        
#         # If the text has Roman Urdu indicators, classify as roman-urdu
#         # Even if it has Urdu script, treat it as roman-urdu since it's likely a label
#         if has_roman_urdu:
#             logger.debug(f"Roman Urdu indicators found in '{text}' -> 'roman-urdu'")
#             return "roman-urdu"
#         elif has_urdu_script:
#             logger.debug(f"Urdu script found in '{text}' but no Roman Urdu indicators -> 'urdu'")
#             return "urdu"
        
#         # Use langdetect for English
#         lang = langdetect.detect(text)
#         if lang == "en":
#             logger.debug(f"Langdetect classified '{text}' as English -> 'english'")
#             return "english"
        
#         # Fallback: treat ambiguous cases as Roman Urdu
#         logger.debug(f"No clear language detected for '{text}', defaulting to 'roman-urdu'")
#         return "roman-urdu"
#     except Exception as e:
#         logger.error(f"Error in language detection for '{text}': {e}")
#         return "roman-urdu"

from lingua import LanguageDetectorBuilder
import re
import logging

logger = logging.getLogger(__name__)

# Initialize lingua detector once (more efficient)
lingua_detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()

def detect_language(text):
    """Improved language detection for Urdu, English, and Roman Urdu using lingua."""
    try:
        logger.debug(f"\n{'='*50}\nStarting language detection for text: '{text}'\n{'='*50}")
        
        # Check for Urdu script
        urdu_script = set("ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی")
        has_urdu_script = any(char in urdu_script for char in text)
        
        if has_urdu_script:
            logger.debug("→ Detected Urdu script characters")
        
        # Check for Roman Urdu indicators
        roman_urdu_indicators = {
            "hai", "nahi", "ni", "bohat", "bhot", "bht", "acha", "achi", "theek", "pasand",
            "mujhe", "yeh", "tha", "thi", "ho", "kar", "ki", "ka", "ke", "k",
            "bhi", "se", "main", "maine", "guzara", "jese", "wesa", "itni",
            "owasm", "pasnd", "khubsurat", "skti", "bta", "ziyada", "bl", "vdya",
            "wo", "bt", "aya", "mujh", "qeemat", "hisaab", "zberdast", "mashahallah",
            "zruur", "kren", "jzakallah", "kr", "lia", "zabardast", "hy", "khushboo",
            "piari", "botle", "dobara", "hen", "vip hai"
        }
        text_lower = text.lower()
        tokens = re.split(r'\W+', text_lower)
        has_roman_urdu = any(token in roman_urdu_indicators for token in tokens if token)
        
        if has_roman_urdu:
            found_keywords = [t for t in tokens if t in roman_urdu_indicators]
            logger.debug(f"→ Found Roman Urdu indicators: {found_keywords}")
        
        # Priority: Roman Urdu indicators > Urdu script > lingua detection
        if has_roman_urdu:
            logger.debug("✓ Decision: Roman Urdu (based on keywords)")
            return "roman-urdu"
        elif has_urdu_script:
            logger.debug("✓ Decision: Urdu (based on script)")
            return "urdu"
        
        logger.debug("→ No Urdu script or Roman Urdu keywords found, using lingua detector")
        detected_lang = lingua_detector.detect_language_of(text)
        
        if detected_lang:
            logger.debug(f"→ Lingua detection result: {detected_lang.name} (ISO: {detected_lang.iso_code_639_1.name})")
            if detected_lang.iso_code_639_1.name == "EN":
                logger.debug("✓ Decision: English (based on lingua)")
                return "english"
            else:
                logger.debug(f"→ Lingua detected non-English language: {detected_lang.name}")
        else:
            logger.debug("→ Lingua couldn't detect language")
        
        logger.debug("✓ Decision: Defaulting to Roman Urdu (fallback)")
        return "roman-urdu"
        
    except Exception as e:
        logger.error(f"🚨 Error in language detection for '{text[:50]}...': {str(e)}", exc_info=True)
        return "roman-urdu"
    
def map_sentiment(sentiment, text):
    """Map model sentiment labels to a 1-5 scale, relying solely on model predictions."""
    text_lower = text.lower()
    
    # Handle explicit ratings from text (not model-derived)
    if "10/10" in text_lower:
        logger.debug(f"Explicit '10/10' in '{text}' -> 5")
        return 5
    if "theek hai" in text_lower:
        logger.debug(f"Explicit '10/10' in '{text}' -> 5")
        return 4
    if "5/10" in text_lower:
        logger.debug(f"Explicit '5/10' in '{text}' -> 3")
        return 3
    
    # Handle BERT star ratings (direct model output)
    if "star" in sentiment.lower():
        score = int(sentiment.split()[0])
        logger.debug(f"BERT predicted {score} stars for '{text}'")
        return score
    
    # Handle Roman Urdu model outputs
    if sentiment == "positive":
        logger.debug(f"Roman Urdu model predicted 'positive' for '{text}' -> 4")
        return 4  # Default positive
    elif sentiment == "negative":
        logger.debug(f"Roman Urdu model predicted 'negative' for '{text}' -> 2")
        return 2  # Default negative
    elif sentiment == "neutral":
        logger.debug(f"Roman Urdu model predicted 'neutral' for '{text}' -> 3")
        return 3  # Neutral
    
    logger.warning(f"Unknown sentiment '{sentiment}' for '{text}' -> 3")
    return 3  # Fallback for unexpected model output

def analyze_sentiment_batch(texts):
    """Batch sentiment analysis with language detection."""
    if not texts:
        return []
    
    # Detect language for each text
    languages = [detect_language(text) for text in texts]
    logger.info(f"Languages detected: {languages}")
    sentiments = []
    
    # Process English/Urdu texts with BERT
    bert_texts = [text for text, lang in zip(texts, languages) if lang in ("english", "urdu")]
    if bert_texts:
        bert_results = bert_model(bert_texts)
        for t, r in zip(bert_texts, bert_results):
            logger.info(f"BERT: '{t}' -> '{r['label']}'")
        bert_sentiments = [map_sentiment(r["label"], t) for r, t in zip(bert_results, bert_texts)]
        bert_idx = 0
    
    # Process Roman Urdu texts
    roman_texts = [text for text, lang in zip(texts, languages) if lang == "roman-urdu"]
    if roman_texts:
        cleaned_texts = array_cleaner(roman_texts)
        vectorized_texts = roman_urdu_vectorizer.transform(cleaned_texts)
        roman_results = roman_urdu_model.predict(vectorized_texts)
        for t, r in zip(roman_texts, roman_results):
            logger.info(f"Roman Urdu: '{t}' -> '{r}'")
        roman_sentiments = [map_sentiment(r, t) for r, t in zip(roman_results, roman_texts)]
        roman_idx = 0
    
    # Combine results in original order
    for lang in languages:
        if lang in ("english", "urdu"):
            sentiments.append(bert_sentiments[bert_idx])
            bert_idx += 1
        else:
            sentiments.append(roman_sentiments[roman_idx])
            roman_idx += 1
    
    logger.info(f"Batch sentiment analysis completed for {len(texts)} texts: {sentiments}")
    return sentiments

def analyze_sentiment(text):
    """Single text sentiment analysis."""
    lang = detect_language(text)
    if lang in ("english", "urdu"):
        result = bert_model(text)[0]["label"]
        return map_sentiment(result, text)
    else:
        cleaned = array_cleaner([text])
        vectorized = roman_urdu_vectorizer.transform(cleaned)
        result = roman_urdu_model.predict(vectorized)[0]
        return map_sentiment(result, text)

# Test the function
# if __name__ == "__main__":
#     test_texts = [
#        "Same as shown received thanks seller and thanks for daraz delivery in time ",
#         "qeemat k hisaab sy zberdast hain aur packaging bhi zberdast thi MashahAllah sy 💗 try zruur kren Recommended 🔥 JzakAllah Sir honestly deal kr k safely deliver krna k lia ❤️ ",
#         "good quality this product is really good so nice 🙂👍🏻 ",
#         "normal, not long lasting ",
#         "Bht hi achi product Packing bht vdya c Delivery fast Thanks seller Thanks Daraz ",
#         # Product 5: Set of 3 Perfumes Tester Spray | Long Lasting Fragrance for Men
#         "Thank you soooo much very nice set of 3 tha mili 4 hain........ 😍😍😍😍😍😍 deliver on time recommended..... ",
#         "I loved the fragrance. It is great. Lasting is also good with good projection. But one thing i did not like that my parcel took very long time to reach. Almost 15 days😏 The seller is good packing was also good but one bottle was leaked and almost its 80% scent is wasted. Any way 5 stars for seller but 1 star for daraz service. Daraz should improve its service. ",
#         "good product vip long lasting perfume 💓 hai vip very happy 😊 ",
#         "boht zabardast hy khushboo boht piari hy aur botle bhi boht achi hy. dobara bhi use ho skti hen ",
#         "boht achi product thanks for your 😊 V"
#     ]
#     results = analyze_sentiment_batch(test_texts)
#     for text, result in zip(test_texts, results):
#         print(f"Text: '{text}' -> Sentiment: {result}")

# if __name__ == "__main__":
#     test_texts = [
#         # Existing test texts
#         "This is a great product!",
#         "Ye bohat acha hai",
#         "Mujhe yeh pasand nahi",
#         "Theek hai bas",
#         "Amazing quality and fast delivery",
#         "Theek hai acha hai",
#         "guzara hai",
#         "quality: 10/10",
#         "quality 5/10",
#         "not bad",
#         "delivery bhot slow ha",
#         "jese picture mai tha wesa ni ha",
#         "itni Achi quality nhi single ply ha double ply nhi ha",
#         "best ha owasm ..mujy bht pasnd aya",
#         "acha hai bl.k bohat acha hai stuff fabric colour everything....bt maine jo mangwaya tha wo ye nhi hai bt mujhe ye bhi psnd aya thankyou so much",
#         "boht hi ziyada khubsurat tha set ...mai bta nhi skti k itni reasonable price mai itna acha product. thank you so much gull and gull store",
#         # Product 1: Pack of 2 perfumes black car and black market best for gift 100 ml each
#         "So beautiful ❤️❤️❤️ Discount rate 🤩🤩🤩 Boht Acha perfume ha thanks to Seller 👍👍👍👍 thanks to Daraz 4",
#         "Longevity:6 hrs longevity Scent:is great I like it ...I m happy to have my perfumes...great experience to buy 1",
#         "perfume smell is not available in products.after push no smell only water spray in perfume blac car perfume.1",
#         "very nice mujhe bahut achcha laga khushbu bahut acchi hai very very nice thanks daraz 👍⭐⭐⭐⭐⭐ 0",
#         "Longevity:not good Scent:perfect Projection:50% good price k hisab se Sahi h 0",
#         # Product 2: Wanted by Rajab perfume for men - 50ml
#         "Behtraeen product ha dusri br order kiya hai or bht acha product receive hua ha dono br. Bht shukria daraz n seller حجم (ملی):Wanted 0",
#         "Wanted by Rajab perfume bohat classy aur attractive hai. Iska scent bohat rich aur luxurious feel deta hai. Main isse office aur parties dono mein use karta hoon. Bohat acha perfume hai for men who like a sophisticated fragrance! حجم (ملی):Wanted 0",
#         "very bad packing and perfume ki bottle ka cap bht lose he or dekhaya grey tha likha or black se likha howa bheja he 10/4 mujhe kisi ko gift karna tha 😭🥺 Volume (ml):Wanted 0",
#         "𝙈𝙖𝙨𝙝 𝘼𝙡𝙡𝙖𝙝 𝙗𝙝𝙤𝙩 𝘼𝙘𝙝𝙖 𝙥𝙚𝙧𝙛𝙪𝙢 𝙝𝙖 𝙤𝙧𝙞𝙜𝙣𝙖𝙡 𝙍𝙖𝙟𝙖𝙗 𝙝𝙖 𝙩𝙝𝙖𝙣𝙠𝙨 𝙙𝙖𝙧𝙖𝙯 حجم (ملی):Wanted 1",
#         "Seller send the same as per description. Good to see the honesty. Wish you best of luck for your future success. Thank you حجم (ملی):Wanted 0",
#         # Product 3: Oud Collection --- Arabic Perfume Dirham_Men - Eau De Perfume - 100ml
#         "الحمد للہ پارسل مل گیا ، پیکنگ بھی کافی محتاط طریقہ سے کی گئی۔ ڈیلیوری بھی کافی تیز تھی۔۔۔ Volume (ml):100ml 3",
#         "1. \"I've received my delivery of Arabic perfume Dirham from Daraz. It has a pleasant fragrance, though I noticed that it doesn't last very long—about 45 minutes to an hour. Still, it's a nice scent for the price.\" 2. \"The Arabic perfume Dirham from Daraz just arrived. The scent is nice but fades fairly quickly, lasting only around 45 minutes to an hour. Overall, it’s a decent buy for the duration.\" 3. \"Just got my Arabic perfume Dirham from Daraz. The fragrance is enjoyable, but I found that it doesn't last beyond an hour. It's good for a short-term wear, though.\" 4. \"Received the Arabic perfume Dirham from Daraz. It's got a slightly pleasant smell but unfortunately doesn't last long—around 45 minutes to an hour. It's okay for the time it does last.\" Volume (ml):100ml 16",
#         "پانچ کے پیسے لے کر ایک کیوں سینڈ کی ھے Volume (ml):100ml 2",
#         "It's Quality is excellent bilkul original ha g price is very low Volume (ml):100ml 5",
#         "good product in cheap price awesome i like it but delivery is little late otherwise also awesome 💯😄😄 Volume (ml):100ml 19",
#         # Product 4: Pack of 2 Gifts Pack of 2 Perfumes - Buy 11 Get 1 Free -Fog black With Darhim 100 ml
#         "Same as shown received thanks seller and thanks for daraz delivery in time 7",
#         "qeemat k hisaab sy zberdast hain aur packaging bhi zberdast thi MashahAllah sy 💗 try zruur kren Recommended 🔥 JzakAllah Sir honestly deal kr k safely deliver krna k lia ❤️ 11",
#         "good quality this product is really good so nice 🙂👍🏻 0",
#         "normal, not long lasting 2",
#         "Bht hi achi product Packing bht vdya c Delivery fast Thanks seller Thanks Daraz 10",
#         # Product 5: Set of 3 Perfumes Tester Spray | Long Lasting Fragrance for Men
#         "Thank you soooo much very nice set of 3 tha mili 4 hain........ 😍😍😍😍😍😍 deliver on time recommended..... Volume (ml):5ml 4",
#         "I loved the fragrance. It is great. Lasting is also good with good projection. But one thing i did not like that my parcel took very long time to reach. Almost 15 days😏 The seller is good packing was also good but one bottle was leaked and almost its 80% scent is wasted. Any way 5 stars for seller but 1 star for daraz service. Daraz should improve its service. Volume (ml):5ml 7",
#         "good product vip long lasting perfume 💓 hai vip very happy 😊 Volume (ml):5ml 2",
#         "boht zabardast hy khushboo boht piari hy aur botle bhi boht achi hy. dobara bhi use ho skti hen حجم (ملی):5ml 2",
#         "boht achi product thanks for your 😊 Volume (ml):5ml 1"
#     ]
#     results = analyze_sentiment_batch(test_texts)
#     for text, result in zip(test_texts, results):
#         print(f"Text: '{text}' -> Sentiment: {result}")


# import langdetect
# print(langdetect.detect("theek ha"))