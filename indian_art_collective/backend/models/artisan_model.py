from db import get_cursor, commit
from utils.auth import hash_password


def get_all_artisans():
    cur = get_cursor()
    cur.execute("SELECT Artisan_ID, Name, Email, DOB, Years_of_Experience, Skill_Level, Address, State, Phone, Gender FROM ARTISANS")
    return cur.fetchall()


def get_artisan_by_id(artisan_id):
    cur = get_cursor()
    cur.execute("SELECT Artisan_ID, Name, Email, DOB, Years_of_Experience, Skill_Level, Address, State, Phone, Gender FROM ARTISANS WHERE Artisan_ID=%s", (artisan_id,))
    return cur.fetchone()


def get_artisan_by_email(email):
    cur = get_cursor()
    cur.execute("SELECT * FROM ARTISANS WHERE Email=%s", (email,))
    return cur.fetchone()


def create_artisan(data):
    cur = get_cursor()
    hashed = hash_password(data['password'])
    cur.execute("""
        INSERT INTO ARTISANS (Name, Email, DOB, Years_of_Experience, Skill_Level, Address, State, Phone, Gender, Password)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (data['name'], data['email'], data.get('dob'), data.get('years_of_experience', 0),
          data.get('skill_level', 'Beginner'), data.get('address'), data.get('state'),
          data.get('phone'), data.get('gender'), hashed))
    commit()
    return cur.lastrowid


def update_artisan(artisan_id, data):
    cur = get_cursor()
    cur.execute("""
        UPDATE ARTISANS SET Name=%s, Email=%s, DOB=%s, Years_of_Experience=%s,
        Skill_Level=%s, Address=%s, State=%s, Phone=%s, Gender=%s
        WHERE Artisan_ID=%s
    """, (data['name'], data['email'], data.get('dob'), data.get('years_of_experience', 0),
          data.get('skill_level', 'Beginner'), data.get('address'), data.get('state'),
          data.get('phone'), data.get('gender'), artisan_id))
    commit()


def delete_artisan(artisan_id):
    cur = get_cursor()
    cur.execute("DELETE FROM ARTISANS WHERE Artisan_ID=%s", (artisan_id,))
    commit()


def get_artisan_stats(artisan_id):
    cur = get_cursor()
    cur.execute("SELECT COUNT(*) as total FROM PRODUCT WHERE Artisan_ID=%s", (artisan_id,))
    products = cur.fetchone()['total']
    cur.execute("""
        SELECT COUNT(o.Order_ID) as total_orders, COALESCE(SUM(o.Total_Amount),0) as earnings
        FROM ORDERS o JOIN PRODUCT p ON o.Product_ID=p.Product_ID
        WHERE p.Artisan_ID=%s
    """, (artisan_id,))
    order_data = cur.fetchone()
    cur.execute("""
        SELECT e.Exhibition_ID, e.Exhibition_Name, e.Location, e.Start_Date, e.End_Date
        FROM EXHIBITION e JOIN PARTICIPATES p ON e.Exhibition_ID=p.Exhibition_ID
        WHERE p.Artisan_ID=%s
    """, (artisan_id,))
    exhibitions = cur.fetchall()
    return {
        'products': products,
        'orders': order_data['total_orders'],
        'earnings': float(order_data['earnings']),
        'exhibitions': exhibitions
    }


def get_artisan_schemes(artisan_id):
    cur = get_cursor()
    cur.execute("""
        SELECT g.* FROM GOVERNMENT_SCHEMES g
        JOIN ENROLLED_IN e ON g.Scheme_ID=e.Scheme_ID
        WHERE e.Artisan_ID=%s
    """, (artisan_id,))
    return cur.fetchall()


def get_artisan_exhibitions(artisan_id):
    cur = get_cursor()
    cur.execute("""
        SELECT e.* FROM EXHIBITION e
        JOIN PARTICIPATES p ON e.Exhibition_ID=p.Exhibition_ID
        WHERE p.Artisan_ID=%s
    """, (artisan_id,))
    return cur.fetchall()
