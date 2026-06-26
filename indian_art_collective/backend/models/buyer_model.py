from db import get_cursor, commit
from utils.auth import hash_password


def get_all_buyers():
    cur = get_cursor()
    cur.execute("SELECT Buyer_ID, Name, Email, Phone, Address FROM BUYER")
    return cur.fetchall()


def get_buyer_by_id(buyer_id):
    cur = get_cursor()
    cur.execute("SELECT Buyer_ID, Name, Email, Phone, Address FROM BUYER WHERE Buyer_ID=%s", (buyer_id,))
    return cur.fetchone()


def get_buyer_by_email(email):
    cur = get_cursor()
    cur.execute("SELECT * FROM BUYER WHERE Email=%s", (email,))
    return cur.fetchone()


def create_buyer(data):
    cur = get_cursor()
    hashed = hash_password(data['password'])
    cur.execute("""
        INSERT INTO BUYER (Name, Email, Phone, Address, Password)
        VALUES (%s,%s,%s,%s,%s)
    """, (data['name'], data['email'], data.get('phone'), data.get('address'), hashed))
    commit()
    return cur.lastrowid


def update_buyer(buyer_id, data):
    cur = get_cursor()
    cur.execute("""
        UPDATE BUYER SET Name=%s, Email=%s, Phone=%s, Address=%s WHERE Buyer_ID=%s
    """, (data['name'], data['email'], data.get('phone'), data.get('address'), buyer_id))
    commit()


def delete_buyer(buyer_id):
    cur = get_cursor()
    cur.execute("DELETE FROM BUYER WHERE Buyer_ID=%s", (buyer_id,))
    commit()


def get_buyer_orders(buyer_id):
    cur = get_cursor()
    cur.execute("""
        SELECT o.*, p.Product_Name, p.Image_URL, a.Name as Artisan_Name
        FROM ORDERS o
        JOIN PRODUCT p ON o.Product_ID=p.Product_ID
        JOIN ARTISANS a ON p.Artisan_ID=a.Artisan_ID
        WHERE o.Buyer_ID=%s
        ORDER BY o.Order_Date DESC
    """, (buyer_id,))
    return cur.fetchall()
