import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
from afinn import Afinn
from nrclex import NRCLex

# Initialize AFINN for sentiment analysis
afinn = Afinn()

# Yelp Scraper Class
class YelpScraper:
    def __init__(self, api_key, location='Boston, MA', num_pages=3):
        self.api_key = api_key
        self.location = location
        self.num_pages = num_pages
        self.base_url = 'https://www.yelp.com/search'

    def get_yelp_urls(self, search_query):
        """Generate Yelp search URLs for the given search query."""
        search_query_encoded = search_query.replace(' ', '%20')
        location_encoded = self.location.replace(' ', '%20')

        return [
            f"{self.base_url}?find_desc={search_query_encoded}&find_loc={location_encoded}&start={page * 10}"
            for page in range(self.num_pages)
        ]

    def fetch_page_content(self, url, retries=3):
        """Fetch page content with retries using a rotating proxy service."""
        for attempt in range(retries):
            try:
                proxy_url = f"https://api.scraperapi.com/?api_key={self.api_key}&url={url}&country_code=us"
                response = requests.get(proxy_url)

                if response.status_code == 200:
                    print(f"Success: Fetched content for {url}")
                    return response.text
                elif response.status_code in [403, 429]:
                    print("Access denied, retrying with delay...")
                    time.sleep(random.uniform(10, 20))
                elif response.status_code == 500:
                    print("Server error (500). Retrying after a longer delay...")
                    time.sleep(random.uniform(20, 30))
                else:
                    print(f"Unexpected status code {response.status_code} for {url}")
            except requests.RequestException as e:
                print(f"Error fetching {url}: {e}")
                time.sleep(random.uniform(5, 10))
        return None

    def scrape_reviews(self, search_query):
        """Scrape reviews from Yelp based on the search query."""
        urls = self.get_yelp_urls(search_query)
        reviews_data = []

        for url in urls:
            print(f"Fetching URL: {url}")
            page_content = self.fetch_page_content(url)
            if page_content:
                soup = BeautifulSoup(page_content, 'html.parser')

                restaurant_name = self.extract_restaurant_name(soup)
                review_texts = self.extract_reviews(soup)

                for review in review_texts:
                    reviews_data.append((restaurant_name, review))

                time.sleep(random.uniform(10, 15))

        return reviews_data

    @staticmethod
    def extract_restaurant_name(soup):
        """Extract restaurant name from page content."""
        restaurant_name_tag = soup.find('h3', class_='y-css-hcgwj4')
        return restaurant_name_tag.get_text(strip=True) if restaurant_name_tag else "Unknown"

    @staticmethod
    def extract_reviews(soup):
        """Extract review texts from page content."""
        review_containers = soup.find_all('p', class_='y-css-1d5urxi')
        return [review.get_text(strip=True) for review in review_containers]


# Analysis Class
class ReviewAnalyzer:
    def __init__(self):
        pass

    @staticmethod
    def analyze_sentiment_afinn(reviews):
        """Perform AFINN sentiment analysis on reviews."""
        sentiment_data = []
        for restaurant, review in reviews:
            score = afinn.score(review)
            sentiment_label = 'positive' if score > 0 else ('negative' if score < 0 else 'neutral')
            sentiment_data.append((review, score, sentiment_label, restaurant))
        return sentiment_data

    @staticmethod
    def analyze_emotions_nrc(reviews):
        """Perform NRC emotion analysis on reviews."""
        emotions_data = []
        for restaurant, review in reviews:
            nrc_result = NRCLex(review)
            top_emotions = nrc_result.top_emotions
            emotions_data.append((review, top_emotions, restaurant))
        return emotions_data


# FileWriter Class
class FileWriter:
    @staticmethod
    def save_sentiment_results(sentiment_results, filename='sentiment_analysis_results.csv'):
        """Save sentiment analysis results to a CSV file."""
        sentiment_df = pd.DataFrame(sentiment_results, columns=['Review', 'Score', 'Sentiment', 'Restaurant'])
        sentiment_df.to_csv(filename, index=False)
        print(f"Sentiment analysis results saved to {filename}")

    @staticmethod
    def save_emotions_results(emotions_results, filename='emotions_analysis.txt'):
        """Save emotion analysis results to a text file."""
        with open(filename, 'w') as f:
            for review, emotions, restaurant in emotions_results:
                f.write(f"Restaurant: {restaurant}\nReview: {review}\nEmotions: {emotions}\n\n")
        print(f"Emotion analysis results saved to {filename}")


# Main Function
def main():
    api_key = ''  # Replace with your ScraperAPI key
    search_query = 'restaurants'

    # Initialize Scraper and Analyzer
    scraper = YelpScraper(api_key=api_key)
    analyzer = ReviewAnalyzer()
    file_writer = FileWriter()

    # Scrape reviews
    reviews = scraper.scrape_reviews(search_query)

    # AFINN Sentiment Analysis
    sentiment_results = analyzer.analyze_sentiment_afinn(reviews)
    file_writer.save_sentiment_results(sentiment_results)

    # NRC Emotion Analysis
    emotions_results = analyzer.analyze_emotions_nrc(reviews)
    file_writer.save_emotions_results(emotions_results)


if __name__ == "__main__":
    main()
