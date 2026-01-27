import sqlite3
import os

# Assignment 9: Advanced SQL
# Task 1: Complex JOINs with Aggregation - Find total price of first 5 orders
# Task 2: Understanding Subqueries - Find average order price per customer

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


def main():
    # Open the database
    db_path = "../db/lesson.db"
    conn = sqlite3.connect(db_path)
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
    
    # Close the database
    conn.close()

if __name__ == "__main__":
    main()
