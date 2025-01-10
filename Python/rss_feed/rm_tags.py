import sqlite3

# Database name
db_name = 'rss_feeds.db'

# Function to create a SQLite database and a table
def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rss_feed (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            url TEXT,
            description TEXT,
            published_date TEXT,
            tags TEXT,
            send INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert feed entry into the database
def insert_feed_entry(db_name, title, author, url, description, published_date, tags, send):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO rss_feed (title, author, url, description, published_date, tags, send)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, author, url, description, published_date, tags, send))
    conn.commit()
    conn.close()

# Function to remove records without valid tags
def remove_invalid_records(db_name, tags_file):
    # Read tags from the tags.txt file
    with open(tags_file, 'r') as file:
        valid_tags = {line.strip() for line in file if line.strip()}  # Use a set for fast lookup

    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Prepare a query to delete records without valid tags
    if valid_tags:
        # Create a placeholder for the tags
        placeholders = ', '.join('?' for _ in valid_tags)
        query = f'''
            DELETE FROM rss_feed
            WHERE tags NOT IN ({placeholders})
        '''
        cursor.execute(query, tuple(valid_tags))
    else:
        # If there are no valid tags, delete all records
        cursor.execute('DELETE FROM rss_feed')

    conn.commit()
    conn.close()

# Example usage
if __name__ == '__main__':
    create_database(db_name)
    # Insert some example data (optional)
    # insert_feed_entry(db_name, 'Example Title', 'Author', 'http://example.com', 'Description', '2023-01-01', 'tag1,tag2', 1)
    
    # Remove records without valid tags
    remove_invalid_records(db_name, 'tags.txt')

