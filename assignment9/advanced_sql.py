import sqlite3
import os
from datetime import date

# Assignment 9: Advanced SQL
# Task 1: Complex JOINs with Aggregation - Find total price of first 5 orders
# Task 2: Understanding Subqueries - Find average order price per customer
# Task 3: An Insert Transaction Based on Data - Create an order with line items

def task1_order_totals(cursor):
    """Task 1: Complex JOINs with Aggregation
    Find the total price of each of the first 5 orders.
    """
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
    
    cursor.execute(sql)
    return cursor.fetchall()


def task2_customer_average_orders(cursor):
    """Task 2: Understanding Subqueries
    For each customer, find the average price of their orders.
    Uses a subquery to calculate order totals, then averages them by customer.
    """
    sql = '''
    SELECT 
        customers.customer_name,
        AVG(order_totals.total_price) as average_total_price
    FROM customers
    LEFT JOIN (
        SELECT 
            orders.customer_id AS customer_id_b,
            SUM(products.price * line_items.quantity) AS total_price
        FROM orders
        JOIN line_items ON orders.order_id = line_items.order_id
        JOIN products ON line_items.product_id = products.product_id
        GROUP BY orders.customer_id
    ) AS order_totals
    ON customers.customer_id = order_totals.customer_id_b
    GROUP BY customers.customer_id
    ORDER BY customers.customer_name
    '''
    
    cursor.execute(sql)
    return cursor.fetchall()


def task3_insert_order_transaction(cursor, conn):
    """Task 3: An Insert Transaction Based on Data
    Create a new order for 'Perez and Sons' employee 'Miranda Harris'
    with 10 of each of the 5 least expensive products.
    """
    try:
        # Start transaction
        conn.execute("BEGIN TRANSACTION")
        
        # Get customer_id for 'Perez and Sons'
        cursor.execute("SELECT customer_id FROM customers WHERE customer_name = ?", 
                       ("Perez and Sons",))
        customer_id = cursor.fetchone()[0]
        
        # Get employee_id for 'Miranda Harris'
        cursor.execute("SELECT employee_id FROM employees WHERE first_name = ? AND last_name = ?", 
                       ("Miranda", "Harris"))
        employee_id = cursor.fetchone()[0]
        
        # Get 5 least expensive products
        cursor.execute("SELECT product_id FROM products ORDER BY price ASC LIMIT 5")
        product_ids = [row[0] for row in cursor.fetchall()]
        
        # Insert order and get order_id using RETURNING
        order_date = str(date.today())
        cursor.execute(
            "INSERT INTO orders (customer_id, employee_id, date) VALUES (?, ?, ?) RETURNING order_id",
            (customer_id, employee_id, order_date)
        )
        order_id = cursor.fetchone()[0]
        
        # Insert 5 line items (10 of each product)
        for product_id in product_ids:
            cursor.execute(
                "INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
                (order_id, product_id, 10)
            )
        
        # Commit transaction
        conn.commit()
        
        # Retrieve and return the order details
        cursor.execute("""
            SELECT 
                line_items.line_item_id,
                line_items.quantity,
                products.product_name
            FROM line_items
            JOIN products ON line_items.product_id = products.product_id
            WHERE line_items.order_id = ?
            ORDER BY line_items.line_item_id
        """, (order_id,))
        
        return cursor.fetchall(), order_id
        
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
        return None, None


def main():
    # Open the database
    db_path = "../db/lesson.db"
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()
    
    # Task 1: Find total price of first 5 orders
    print("=" * 50)
    print("Task 1: Complex JOINs with Aggregation")
    print("=" * 50)
    print("Order ID | Total Price")
    print("---------|------------")
    results = task1_order_totals(cursor)
    for row in results:
        print(f"{row[0]:8d} | ${row[1]:.2f}")
    
    print("\n" + "=" * 50)
    print("Task 2: Understanding Subqueries")
    print("=" * 50)
    print("Customer Name          | Average Order Total")
    print("-----------------------|-------------------")
    results = task2_customer_average_orders(cursor)
    for row in results:
        if row[1] is not None:
            print(f"{row[0]:22s} | ${row[1]:10.2f}")
        else:
            print(f"{row[0]:22s} | None")
    
    print("\n" + "=" * 50)
    print("Task 3: An Insert Transaction Based on Data")
    print("=" * 50)
    results, order_id = task3_insert_order_transaction(cursor, conn)
    
    if results and order_id:
        print(f"Created order {order_id} for Perez and Sons")
        print("\nLine Item ID | Quantity | Product Name")
        print("-------------|----------|--------------------")
        for row in results:
            print(f"{row[0]:12d} | {row[1]:8d} | {row[2]}")
        
        # Clean up: delete the line items and order we just created
        print("\nCleaning up order...")
        cursor.execute("DELETE FROM line_items WHERE order_id = ?", (order_id,))
        cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
        conn.commit()
        print(f"Deleted order {order_id} and its line items.")
    
    # Close the database
    conn.close()

if __name__ == "__main__":
    main()
