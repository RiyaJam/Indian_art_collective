from db import get_cursor, commit
from datetime import date


def get_all_orders():
    cur = get_cursor()
    cur.execute("""
        SELECT o.*, b.Name as Buyer_Name, p.Product_Name, a.Name as Artisan_Name
        FROM ORDERS o
        LEFT JOIN BUYER b ON o.Buyer_ID=b.Buyer_ID
        LEFT JOIN PRODUCT p ON o.Product_ID=p.Product_ID
        LEFT JOIN ARTISANS a ON p.Artisan_ID=a.Artisan_ID
        ORDER BY o.Order_Date DESC
    """)
    return cur.fetchall()


def get_order_by_id(order_id):
    cur = get_cursor()
    cur.execute("""
        SELECT o.*, b.Name as Buyer_Name, b.Email as Buyer_Email, b.Phone as Buyer_Phone,
               p.Product_Name, p.Image_URL, p.Price, a.Name as Artisan_Name
        FROM ORDERS o
        LEFT JOIN BUYER b ON o.Buyer_ID=b.Buyer_ID
        LEFT JOIN PRODUCT p ON o.Product_ID=p.Product_ID
        LEFT JOIN ARTISANS a ON p.Artisan_ID=a.Artisan_ID
        WHERE o.Order_ID=%s
    """, (order_id,))
    return cur.fetchone()


def get_orders_by_artisan(artisan_id):
    cur = get_cursor()
    cur.execute("""
        SELECT o.*, b.Name as Buyer_Name, p.Product_Name, p.Image_URL
        FROM ORDERS o
        JOIN PRODUCT p ON o.Product_ID=p.Product_ID
        JOIN BUYER b ON o.Buyer_ID=b.Buyer_ID
        WHERE p.Artisan_ID=%s
        ORDER BY o.Order_Date DESC
    """, (artisan_id,))
    return cur.fetchall()


def create_order(data):
    cur = get_cursor()
    # Get product price
    cur.execute("SELECT Price, Stock_Quantity FROM PRODUCT WHERE Product_ID=%s", (data['product_id'],))
    product = cur.fetchone()
    if not product:
        return None, "Product not found"
    if product['Stock_Quantity'] < data['quantity']:
        return None, "Insufficient stock"

    total = float(product['Price']) * int(data['quantity'])
    cur.execute("""
        INSERT INTO ORDERS (Order_Date, Quantity, Total_Amount, Buyer_ID, Product_ID)
        VALUES (%s,%s,%s,%s,%s)
    """, (date.today(), data['quantity'], total, data['buyer_id'], data['product_id']))
    # Reduce stock
    cur.execute("UPDATE PRODUCT SET Stock_Quantity=Stock_Quantity-%s WHERE Product_ID=%s",
                (data['quantity'], data['product_id']))
    commit()
    return cur.lastrowid, None


def delete_order(order_id):
    cur = get_cursor()
    cur.execute("DELETE FROM ORDERS WHERE Order_ID=%s", (order_id,))
    commit()
