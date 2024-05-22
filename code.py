import knime.scripting.io as knio
import re
from autocorrect import Speller
from nltk import word_tokenize, ngrams
from nltk.stem import SnowballStemmer
import string
import pandas as pd
import nltk
nltk.download('punkt')

# Initialize stemmer
stemmer = SnowballStemmer("english")

# Load data
data = knio.input_tables[0].to_pandas()
data = data[data['Feedback'].notna()]

# Define keyword categories with updated and anonymized keywords
example_keywords = {
    'Website Usability': ['website confusing', 'better response', 'site speed', 'search issues', 'system lag', 'slow loading', 'complex navigation'],
    'Website Layout': ['well-organized', 'clear interface', 'layout issues', 'better design', 'more photos'],
    'Mobile Experience': ['mobile', 'phone', 'app', 'iOS', 'android', 'tablet'],
    'Checkout': ['checkout issues', 'payment problems', 'billing', 'cart issues', 'payment options'],
    'Account & Customer Service': ['account issues', 'customer service', 'login problems', 'profile management', 'order history'],
    'Promotion & Discount': ['discounts', 'promotions', 'coupons', 'special offers', 'free gifts'],
    'Product Related': ['product info', 'product availability', 'quality issues', 'product reviews'],
    'Gifting': ['gift options', 'gift wrapping', 'gift cards', 'special messages'],
    'Shipping Issues': ['shipping cost', 'delivery speed', 'tracking issues', 'international shipping', 'shipping options'],
    'No Suggestion': ['no issues', 'satisfied', 'happy', 'excellent', 'great experience'],
    'Other Category': []
}

# Preprocess keywords
for category in example_keywords:
    example_keywords[category] = [keyword.lower() for keyword in example_keywords[category]]

keywords_df = pd.DataFrame([(key, ", ".join(values)) for key, values in example_keywords.items()], columns=['Category', 'Keywords'])
keywords = {row['Category']: row['Keywords'].split(', ') for index, row in keywords_df.iterrows()}

def generate_ngrams(s, n):
    tokens = [token for token in s.lower().split() if token]
    return [" ".join(ngram) for ngram in zip(*[tokens[i:] for i in range(n)])]

def preprocess_text(text):
    special_phrases = {'apple pay': 'applepay'}  # Add other special phrases if needed

    for phrase, token in special_phrases.items():
        text = text.replace(phrase, token)

    punctuation = string.punctuation.replace('$', '').replace('%', '')
    text = text.lower().translate(str.maketrans('', '', punctuation))

    words = word_tokenize(text)
    processed_words = [stemmer.stem(word) if ' ' not in word else word for word in words]
    processed_text = " ".join(processed_words)

    for phrase, token in special_phrases.items():
        processed_text = processed_text.replace(token, phrase)

    return processed_text

for category, keyword_list in example_keywords.items():
    processed_keywords = [preprocess_text(word) for word in keyword_list]
    example_keywords[category] = processed_keywords

    bigrams = [generate_ngrams(word, 2) for word in processed_keywords]
    trigrams = [generate_ngrams(word, 3) for word in processed_keywords]
    fourgrams = [generate_ngrams(word, 4) for word in processed_keywords]

    bigrams = [item for sublist in bigrams for item in sublist]
    trigrams = [item for sublist in trigrams for item in sublist]
    fourgrams = [item for sublist in fourgrams for item in sublist]

    example_keywords[category] = processed_keywords + bigrams + trigrams + fourgrams

def categorize_response(response):
    categories = {key: 0 for key in keywords.keys()}
    preprocessed_response = preprocess_text(response)
    preprocessed_stemmed_response = ' '.join([stemmer.stem(word) for word in preprocessed_response.split()])

    for category, keyword_list in example_keywords.items():
        if keyword_list:
            for keyword in keyword_list:
                if f' {keyword} ' in f' {preprocessed_stemmed_response} ':
                    categories[category] = 1
                    break

    if sum(categories.values()) == 0:
        categories['Other Category'] = 1

    if categories['No Suggestion'] == 1 and sum(categories.values()) > 1:
        categories['No Suggestion'] = 0

    return pd.Series(categories)

category_df = data['Feedback'].apply(categorize_response)
data = pd.concat([data, category_df], axis=1)
data['Category'] = data[keywords.keys()].apply(lambda row: ', '.join(row[row == 1].index), axis=1)

knio.output_tables[0] = knio.Table.from_pandas(data)
