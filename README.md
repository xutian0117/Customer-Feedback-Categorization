# Customer Feedback Categorization

## Overview

This project focuses on categorizing customer feedback using Natural Language Processing (NLP) techniques. The goal is to classify feedback into predefined categories to help identify common themes and areas for improvement in the customer experience.

## Features

- **Data Preprocessing**: Converts text to lowercase, removes punctuation, and stems words to ensure consistency.
- **N-gram Generation**: Creates bigrams, trigrams, and four-grams to enhance keyword matching.
- **Keyword Matching**: Matches feedback against a comprehensive list of keywords to categorize responses accurately.
- **Categorization Logic**: Classifies feedback into multiple categories such as Website Usability, Mobile Experience, Checkout, etc.

## Keyword Categories

The feedback is categorized into the following groups:

- **Website Usability**: Issues related to website speed, navigation, and usability.
- **Website Layout**: Feedback on the layout, design, and organization of the website.
- **Mobile Experience**: Comments about mobile and tablet usability.
- **Checkout**: Issues encountered during the checkout process.
- **Account & Customer Service**: Problems with account management and customer service interactions.
- **Promotion & Discount**: Feedback regarding promotions, discounts, and special offers.
- **Product Related**: Comments on product information, availability, and quality.
- **Gifting**: Feedback on gifting options and related services.
- **Shipping Issues**: Issues related to shipping costs, delivery speed, and tracking.
- **No Suggestion**: Positive feedback or no suggestions for improvement.
- **Other Category**: Feedback that does not fit into any predefined category.

## Implementation Details

### Data Loading

The input data is loaded from a table and converted to a pandas DataFrame. Only rows with non-null feedback are processed.

### Preprocessing

Text preprocessing includes:
- Lowercasing text
- Removing punctuation
- Replacing special phrases with single tokens
- Stemming words

### Keyword Matching

Keywords are preprocessed and expanded using n-grams (bigrams, trigrams, four-grams). Each feedback entry is categorized based on the presence of these keywords.

### Categorization

The categorization function processes each feedback entry, matches it against the keywords, and assigns appropriate categories. If no match is found, the feedback is classified as 'Other Category'.

## Usage

To run the categorization process, simply load your feedback data into the KNIME workflow, and the script will output a categorized table.

## Dependencies


- re
- autocorrect
- nltk
- pandas
- numpy

Make sure to install the necessary Python packages using:
```bash
pip install autocorrect nltk pandas numpy
