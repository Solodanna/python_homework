import sqlite3
import pandas as pd

try:
    # Connect to the lesson database
    connection = sqlite3.connect('../db/lesson.db')
    
    # SQL query to retrieve data from line_items and products tables
    query = '''
    SELECT 
        line_items.line_item_id,
        line_items.quantity,
        line_items.product_id,
        products.product_name,
        products.price
    FROM line_items
    JOIN products ON line_items.product_id = products.product_id
    '''
    
    # Read data into a DataFrame
    df = pd.read_sql_query(query, connection)
    
    print("=== First 5 rows of the DataFrame ===")
    print(df.head())
    
    # Add a 'total' column (quantity * price)
    df['total'] = df['quantity'] * df['price']
    
    print("\n=== DataFrame with 'total' column (first 5 rows) ===")
    print(df.head())
    
    # Group by product_id with aggregations
    grouped_df = df.groupby('product_id').agg({
        'line_item_id': 'count',
        'total': 'sum',
        'product_name': 'first'
    }).reset_index()
    
    # Rename the 'line_item_id' column to 'count' for clarity
    grouped_df = grouped_df.rename(columns={'line_item_id': 'count'})
    
    print("\n=== Grouped DataFrame (first 5 rows) ===")
    print(grouped_df.head())
    
    # Sort by product_name
    grouped_df = grouped_df.sort_values('product_name')
    
    print("\n=== Sorted by product_name (first 5 rows) ===")
    print(grouped_df.head())
    
    # Write to CSV file
    grouped_df.to_csv('order_summary.csv', index=False)
    print("\n=== order_summary.csv created successfully ===")
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    if connection:
        connection.close()
        print("Database connection closed")
