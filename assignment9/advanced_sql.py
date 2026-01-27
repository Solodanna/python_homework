import sqlite3
import os

# Task 1: Complex JOINs with Aggregation
# Find the total price of each of the first 5 orders
# Join orders, line_items, and products tables
# GROUP BY order_id, SELECT order_id and SUM(price * quantity)
# ORDER BY order_id LIMIT 5

def main():
    # Open the database
    db_path = "../db/lesson.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # SQL statement to find total price of each of the first 5 orders
    sql = '''
    SELECT 
        orders.order_id,
        SUM(products.price * line_items.quantity) as total_price
    FROM orders
    JOIN line_items ON orders.order_id = line_items.order_id
    JOIN products ON line_items.product_id = products.product_id
    GROUP BY orders.order_id
    ORDER BY orders.order_id
    LIMIT 5
    '''
    
    # Execute the SQL statement
    cursor.execute(sql)
    results = cursor.fetchall()
    
    # Print the results
    print("Order ID | Total Price")
    print("---------|------------")
    for row in results:
        print(f"{row[0]:8d} | ${row[1]:.2f}")
    
    # Close the database
    conn.close()

if __name__ == "__main__":
    main()
