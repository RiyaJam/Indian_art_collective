from db import get_cursor, commit


def get_all_products(filters=None):
    cur = get_cursor()
    query = """
        SELECT p.*, a.Name as Artisan_Name, a.State as Artisan_State,
               c.Craft_Name, c.Category, c.Region
        FROM PRODUCT p
        LEFT JOIN ARTISANS a ON p.Artisan_ID=a.Artisan_ID
        LEFT JOIN CRAFT c ON p.Craft_ID=c.Craft_ID
    """
    conditions = []
    params = []

    if filters:
        if filters.get('search'):
            s = f"%{filters['search']}%"
            conditions.append("(p.Product_Name LIKE %s OR a.Name LIKE %s OR c.Craft_Name LIKE %s)")
            params.extend([s, s, s])
        if filters.get('min_price'):
            conditions.append("p.Price >= %s")
            params.append(filters['min_price'])
        if filters.get('max_price'):
            conditions.append("p.Price <= %s")
            params.append(filters['max_price'])
        if filters.get('category'):
            conditions.append("c.Category = %s")
            params.append(filters['category'])
        if filters.get('region'):
            conditions.append("c.Region = %s")
            params.append(filters['region'])
        if filters.get('skill_level'):
            conditions.append("a.Skill_Level = %s")
            params.append(filters['skill_level'])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    sort = filters.get('sort') if filters else None
    if sort == 'price_asc':
        query += " ORDER BY p.Price ASC"
    elif sort == 'price_desc':
        query += " ORDER BY p.Price DESC"
    elif sort == 'latest':
        query += " ORDER BY p.Created_At DESC"
    else:
        query += " ORDER BY p.Created_At DESC"

    cur.execute(query, params)
    return cur.fetchall()


def get_product_by_id(product_id):
    cur = get_cursor()
    cur.execute("""
        SELECT p.*, a.Name as Artisan_Name, a.State as Artisan_State, a.Skill_Level,
               c.Craft_Name, c.Category, c.Region, c.Description as Craft_Description
        FROM PRODUCT p
        LEFT JOIN ARTISANS a ON p.Artisan_ID=a.Artisan_ID
        LEFT JOIN CRAFT c ON p.Craft_ID=c.Craft_ID
        WHERE p.Product_ID=%s
    """, (product_id,))
    return cur.fetchone()


def get_products_by_artisan(artisan_id):
    cur = get_cursor()
    cur.execute("""
        SELECT p.*, c.Craft_Name, c.Category
        FROM PRODUCT p
        LEFT JOIN CRAFT c ON p.Craft_ID=c.Craft_ID
        WHERE p.Artisan_ID=%s
        ORDER BY p.Created_At DESC
    """, (artisan_id,))
    return cur.fetchall()


def create_product(data):
    cur = get_cursor()
    cur.execute("""
        INSERT INTO PRODUCT (Product_Name, Price, Stock_Quantity, Description, Artisan_ID, Craft_ID, Image_URL)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (data['product_name'], data['price'], data.get('stock_quantity', 0),
          data.get('description'), data['artisan_id'], data.get('craft_id'),
          data.get('image_url', '/static/uploads/default_product.jpg')))
    commit()
    return cur.lastrowid


def update_product(product_id, data):
    cur = get_cursor()
    cur.execute("""
        UPDATE PRODUCT SET Product_Name=%s, Price=%s, Stock_Quantity=%s,
        Description=%s, Craft_ID=%s, Image_URL=%s
        WHERE Product_ID=%s
    """, (data['product_name'], data['price'], data.get('stock_quantity', 0),
          data.get('description'), data.get('craft_id'),
          data.get('image_url'), product_id))
    commit()


def delete_product(product_id):
    cur = get_cursor()
    cur.execute("DELETE FROM PRODUCT WHERE Product_ID=%s", (product_id,))
    commit()


def get_featured_products(limit=6):
    cur = get_cursor()
    cur.execute("""
        SELECT p.*, a.Name as Artisan_Name, c.Craft_Name
        FROM PRODUCT p
        LEFT JOIN ARTISANS a ON p.Artisan_ID=a.Artisan_ID
        LEFT JOIN CRAFT c ON p.Craft_ID=c.Craft_ID
        WHERE p.Stock_Quantity > 0
        ORDER BY p.Created_At DESC LIMIT %s
    """, (limit,))
    return cur.fetchall()
