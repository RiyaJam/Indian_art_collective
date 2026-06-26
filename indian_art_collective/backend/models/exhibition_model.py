from db import get_cursor, commit


def get_all_exhibitions():
    cur = get_cursor()
    cur.execute("SELECT * FROM EXHIBITION ORDER BY Start_Date ASC")
    return cur.fetchall()


def get_exhibition_by_id(exhibition_id):
    cur = get_cursor()
    cur.execute("SELECT * FROM EXHIBITION WHERE Exhibition_ID=%s", (exhibition_id,))
    return cur.fetchone()


def get_exhibition_artisans(exhibition_id):
    cur = get_cursor()
    cur.execute("""
        SELECT a.Artisan_ID, a.Name, a.State, a.Skill_Level
        FROM ARTISANS a JOIN PARTICIPATES p ON a.Artisan_ID=p.Artisan_ID
        WHERE p.Exhibition_ID=%s
    """, (exhibition_id,))
    return cur.fetchall()


def create_exhibition(data):
    cur = get_cursor()
    cur.execute("""
        INSERT INTO EXHIBITION (Exhibition_Name, Location, Start_Date, End_Date)
        VALUES (%s,%s,%s,%s)
    """, (data['exhibition_name'], data['location'], data['start_date'], data['end_date']))
    commit()
    return cur.lastrowid


def update_exhibition(exhibition_id, data):
    cur = get_cursor()
    cur.execute("""
        UPDATE EXHIBITION SET Exhibition_Name=%s, Location=%s, Start_Date=%s, End_Date=%s
        WHERE Exhibition_ID=%s
    """, (data['exhibition_name'], data['location'], data['start_date'], data['end_date'], exhibition_id))
    commit()


def delete_exhibition(exhibition_id):
    cur = get_cursor()
    cur.execute("DELETE FROM EXHIBITION WHERE Exhibition_ID=%s", (exhibition_id,))
    commit()


def assign_artisan_to_exhibition(artisan_id, exhibition_id):
    cur = get_cursor()
    cur.execute("INSERT IGNORE INTO PARTICIPATES (Artisan_ID, Exhibition_ID) VALUES (%s,%s)",
                (artisan_id, exhibition_id))
    commit()


def remove_artisan_from_exhibition(artisan_id, exhibition_id):
    cur = get_cursor()
    cur.execute("DELETE FROM PARTICIPATES WHERE Artisan_ID=%s AND Exhibition_ID=%s",
                (artisan_id, exhibition_id))
    commit()
