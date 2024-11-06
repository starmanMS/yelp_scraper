# Yelp Review Scraper and Sentiment Analyzer

This project is a Python-based tool to scrape restaurant reviews from Yelp, perform sentiment and emotion analysis on the reviews, and save the results to files. The tool leverages **ScraperAPI** for dynamic page access, **BeautifulSoup** for HTML parsing, **AFINN** for sentiment analysis, and **NRCLex** for emotion analysis.

## Table of Contents
- [Project Overview](#project-overview)
- [Requirements](#requirements)
- [How It Works](#how-it-works)
  - [YelpScraper Class](#yelpscraper-class)
  - [ReviewAnalyzer Class](#reviewanalyzer-class)
  - [FileWriter Class](#filewriter-class)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Saving and Interpreting Results](#saving-and-interpreting-results)
- [Notes](#notes)

---

## Project Overview

This tool scrapes Yelp reviews for restaurants in a specified location and performs:
1. **Sentiment Analysis** with AFINN, categorizing each review as positive, neutral, or negative.
2. **Emotion Analysis** with NRCLex to identify top emotions within each review.

Results are stored in:
- `sentiment_analysis_results.csv` for sentiment data
- `emotions_analysis.txt` for detailed emotion analysis results.

## Requirements

- **Python 3.x**
- **Libraries**: `requests`, `beautifulsoup4`, `pandas`, `random`, `time`, `afinn`, `nrclex`
  
Install libraries:
```bash
pip install requests beautifulsoup4 pandas afinn nrclex
```

## How It Works

### YelpScraper Class

The `YelpScraper` class is responsible for:
- **Generating URLs** for Yelp search pages for a given query and location.
- **Fetching page content** from Yelp using ScraperAPI with retries in case of errors.
- **Extracting reviews** from the page content with BeautifulSoup.
  
**Key methods**:
- `get_yelp_urls`: Generates paginated search URLs based on the search query.
- `fetch_page_content`: Fetches page content through ScraperAPI with handling for 403, 429, and 500 errors.
- `scrape_reviews`: Scrapes reviews for each URL generated and returns them in a list.
- `extract_restaurant_name` and `extract_reviews`: Helper methods to parse HTML content to find the restaurant name and review text.

### ReviewAnalyzer Class

The `ReviewAnalyzer` class processes scraped reviews to perform:
- **AFINN Sentiment Analysis**: Scores each review and labels it as positive, neutral, or negative.
- **NRC Emotion Analysis**: Identifies top emotions in each review.

**Key methods**:
- `analyze_sentiment_afinn`: Calculates sentiment scores for each review.
- `analyze_emotions_nrc`: Identifies top emotions for each review.

### FileWriter Class

The `FileWriter` class saves analysis results to files:
- `save_sentiment_results`: Saves sentiment scores and labels to a CSV file.
- `save_emotions_results`: Saves top emotions to a text file.

## Getting Started

1. **Add Your ScraperAPI Key**: Replace `api_key` in the `main()` function with your ScraperAPI key.
2. **Set the Location** (optional): You can set `location` when initializing `YelpScraper` to specify a location for search results.

## Usage

To run the script, simply execute the main function:
```bash
python yelp_scraper.py
```

The `main` function:
1. Initializes `YelpScraper`, `ReviewAnalyzer`, and `FileWriter` classes.
2. Scrapes reviews for a specified search query (`restaurants` by default).
3. Analyzes the reviews for sentiment and emotion.
4. Saves the analysis results.

## Saving and Interpreting Results

- **Sentiment Analysis Results**: Saved in `sentiment_analysis_results.csv` with columns:
  - `Review`: Text of the review
  - `Score`: Sentiment score (positive, negative, or neutral)
  - `Sentiment`: Label (positive, negative, or neutral)
  - `Restaurant`: Name of the restaurant

- **Emotion Analysis Results**: Saved in `emotions_analysis.txt` with details for each review:
  - `Restaurant`: Name of the restaurant
  - `Review`: Text of the review
  - `Emotions`: Top emotions detected by NRCLex

## Notes

1. **ScraperAPI Key**: Ensure you have a valid ScraperAPI key for fetching Yelp pages.
2. **Proxies and Rate Limits**: This script uses ScraperAPI with random delays to avoid rate limits. Adjust the `time.sleep` intervals as necessary if you encounter blocking issues.
3. **HTML Structure**: The CSS selectors (e.g., `'y-css-hcgwj4'`) may change, requiring updates to `extract_restaurant_name` and `extract_reviews`.

--- 

This tool provides a streamlined way to gather insights from Yelp reviews, providing both sentiment and emotion analysis data for deeper understanding of customer feedback.