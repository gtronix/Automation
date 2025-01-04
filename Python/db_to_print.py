import sqlite3

# Database
db_name = 'rss_feeds.db'

# Function to retrieve and print all RSS feed entries from the database
def print_rss_feeds(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT title, url, description, published_date FROM rss_feed')
    feeds = cursor.fetchall()
    
    for feed in feeds:
        title, url, description, published_date = feed
        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Description: {description}")
        print(f"Published Date: {published_date}")
        print("-" * 40)  # Separator for readability

    conn.close()

# Print the RSS feeds from the database
print_rss_feeds(db_name)

