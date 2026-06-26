from db import get_cursor, commit


def get_all_schemes():
    cur = get_cursor()
    cur.execute("SELECT * FROM GOVERNMENT_SCHEMES ORDER BY Launch_Year DESC")
    return cur.fetchall()


def get_scheme_by_id(scheme_id):
    cur = get_cursor()
    cur.execute("SELECT * FROM GOVERNMENT_SCHEMES WHERE Scheme_ID=%s", (scheme_id,))
    return cur.fetchone()


def create_scheme(data):
    cur = get_cursor()
    cur.execute("""
        INSERT INTO GOVERNMENT_SCHEMES (Scheme_Name, Launch_Year, Benefits, Eligibility)
        VALUES (%s,%s,%s,%s)
    """, (data['scheme_name'], data.get('launch_year'), data.get('benefits'), data.get('eligibility')))
    commit()
    return cur.lastrowid


def update_scheme(scheme_id, data):
    cur = get_cursor()
    cur.execute("""
        UPDATE GOVERNMENT_SCHEMES SET Scheme_Name=%s, Launch_Year=%s, Benefits=%s, Eligibility=%s
        WHERE Scheme_ID=%s
    """, (data['scheme_name'], data.get('launch_year'), data.get('benefits'), data.get('eligibility'), scheme_id))
    commit()


def delete_scheme(scheme_id):
    cur = get_cursor()
    cur.execute("DELETE FROM GOVERNMENT_SCHEMES WHERE Scheme_ID=%s", (scheme_id,))
    commit()


def enroll_artisan(artisan_id, scheme_id):
    cur = get_cursor()
    cur.execute("INSERT IGNORE INTO ENROLLED_IN (Artisan_ID, Scheme_ID) VALUES (%s,%s)",
                (artisan_id, scheme_id))
    commit()


def unenroll_artisan(artisan_id, scheme_id):
    cur = get_cursor()
    cur.execute("DELETE FROM ENROLLED_IN WHERE Artisan_ID=%s AND Scheme_ID=%s",
                (artisan_id, scheme_id))
    commit()
