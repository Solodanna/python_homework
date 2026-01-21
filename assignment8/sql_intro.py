import sqlite3

def add_publisher(cursor, name):
    """Add a publisher to the database. Handle duplicates."""
    try:
        cursor.execute('''
            INSERT INTO publishers (name)
            VALUES (?)
        ''', (name,))
        print(f"Publisher '{name}' added successfully")
        return True
    except sqlite3.IntegrityError:
        print(f"Publisher '{name}' already exists")
        return False
    except sqlite3.Error as e:
        print(f"Error adding publisher: {e}")
        return False

def add_magazine(cursor, name, publisher_id):
    """Add a magazine to the database. Handle duplicates."""
    try:
        cursor.execute('''
            INSERT INTO magazines (name, publisher_id)
            VALUES (?, ?)
        ''', (name, publisher_id))
        print(f"Magazine '{name}' added successfully")
        return True
    except sqlite3.IntegrityError:
        print(f"Magazine '{name}' already exists")
        return False
    except sqlite3.Error as e:
        print(f"Error adding magazine: {e}")
        return False

def add_subscriber(cursor, name, address):
    """Add a subscriber to the database. Check for duplicates (name AND address)."""
    try:
        # Check if subscriber with same name and address already exists
        cursor.execute('''
            SELECT id FROM subscribers
            WHERE name = ? AND address = ?
        ''', (name, address))
        if cursor.fetchone():
            print(f"Subscriber '{name}' with address '{address}' already exists")
            return False
        
        cursor.execute('''
            INSERT INTO subscribers (name, address)
            VALUES (?, ?)
        ''', (name, address))
        print(f"Subscriber '{name}' added successfully")
        return True
    except sqlite3.Error as e:
        print(f"Error adding subscriber: {e}")
        return False

def add_subscription(cursor, subscriber_id, magazine_id, expiration_date):
    """Add a subscription to the database. Handle duplicates."""
    try:
        # Check if subscription already exists
        cursor.execute('''
            SELECT id FROM subscriptions
            WHERE subscriber_id = ? AND magazine_id = ?
        ''', (subscriber_id, magazine_id))
        if cursor.fetchone():
            print(f"Subscription already exists for subscriber {subscriber_id} and magazine {magazine_id}")
            return False
        
        cursor.execute('''
            INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date)
            VALUES (?, ?, ?)
        ''', (subscriber_id, magazine_id, expiration_date))
        print(f"Subscription added successfully")
        return True
    except sqlite3.Error as e:
        print(f"Error adding subscription: {e}")
        return False

def query_all_subscribers(cursor):
    """Retrieve all information from the subscribers table."""
    try:
        cursor.execute('SELECT * FROM subscribers')
        rows = cursor.fetchall()
        print("\n--- All Subscribers ---")
        print("ID | Name | Address")
        print("-" * 50)
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]}")
    except sqlite3.Error as e:
        print(f"Error retrieving subscribers: {e}")

def query_magazines_sorted(cursor):
    """Retrieve all magazines sorted by name."""
    try:
        cursor.execute('SELECT * FROM magazines ORDER BY name')
        rows = cursor.fetchall()
        print("\n--- All Magazines (Sorted by Name) ---")
        print("ID | Name | Publisher ID")
        print("-" * 50)
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]}")
    except sqlite3.Error as e:
        print(f"Error retrieving magazines: {e}")

def query_magazines_by_publisher(cursor, publisher_name):
    """Find magazines for a particular publisher using a JOIN."""
    try:
        cursor.execute('''
            SELECT m.id, m.name, p.name as publisher_name
            FROM magazines m
            JOIN publishers p ON m.publisher_id = p.id
            WHERE p.name = ?
        ''', (publisher_name,))
        rows = cursor.fetchall()
        print(f"\n--- Magazines by Publisher '{publisher_name}' ---")
        print("ID | Magazine Name | Publisher")
        print("-" * 50)
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]}")
    except sqlite3.Error as e:
        print(f"Error retrieving magazines by publisher: {e}")

try:
    # Connecting to the SQLite database (creates it if it doesn't exist)
    connection = sqlite3.connect('../db/magazines.db')
    cursor = connection.cursor()
    print("Successfully connected to the database")
    
    # Enable foreign key constraints
    connection.execute("PRAGMA foreign_keys = 1")
    
    # Creating publishers table
    try:
        cursor.execute('''
            CREATE TABLE publishers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        ''')
        print("Publishers table created")
    except sqlite3.Error as e:
        print(f"Error creating publishers table: {e}")
    
    # Creating magazines table
    try:
        cursor.execute('''
            CREATE TABLE magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY (publisher_id) REFERENCES publishers(id)
            )
        ''')
        print("Magazines table created")
    except sqlite3.Error as e:
        print(f"Error creating magazines table: {e}")
    
    # Creating subscribers table
    try:
        cursor.execute('''
            CREATE TABLE subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL
            )
        ''')
        print("Subscribers table created")
    except sqlite3.Error as e:
        print(f"Error creating subscribers table: {e}")
    
    # Creating subscriptions table
    try:
        cursor.execute('''
            CREATE TABLE subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscriber_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                expiration_date TEXT NOT NULL,
                FOREIGN KEY (subscriber_id) REFERENCES subscribers(id),
                FOREIGN KEY (magazine_id) REFERENCES magazines(id)
            )
        ''')
        print("Subscriptions table created")
    except sqlite3.Error as e:
        print(f"Error creating subscriptions table: {e}")
    
    # Commit the changes
    connection.commit()
    
    # Populate tables with data
    print("\n--- Populating Publishers ---")
    add_publisher(cursor, "Penguin Books")
    add_publisher(cursor, "HarperCollins")
    add_publisher(cursor, "Simon & Schuster")
    
    connection.commit()
    
    print("\n--- Populating Magazines ---")
    add_magazine(cursor, "The Economist", 1)
    add_magazine(cursor, "National Geographic", 2)
    add_magazine(cursor, "Time Magazine", 3)
    
    connection.commit()
    
    print("\n--- Populating Subscribers ---")
    add_subscriber(cursor, "John Smith", "123 Main St")
    add_subscriber(cursor, "Jane Doe", "456 Oak Ave")
    add_subscriber(cursor, "John Smith", "789 Pine Rd")
    
    connection.commit()
    
    print("\n--- Populating Subscriptions ---")
    add_subscription(cursor, 1, 1, "2026-12-31")
    add_subscription(cursor, 1, 2, "2026-06-30")
    add_subscription(cursor, 2, 2, "2026-09-15")
    
    connection.commit()
    print("\nAll data committed to database")
    
    # Execute queries
    query_all_subscribers(cursor)
    query_magazines_sorted(cursor)
    query_magazines_by_publisher(cursor, "Penguin Books")
    
except sqlite3.Error as e:
    print(f"Error connecting to database: {e}")
    
finally:
    # Close the connection
    if connection:
        connection.close()
        print("Database connection closed")
