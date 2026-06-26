"""
Run this script once after setting up the database to fix any password issues.
Usage: python reset_passwords.py

This updates all demo user passwords to 'password123' using Werkzeug hashing.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from werkzeug.security import generate_password_hash

# Connect directly using pymysql/mysqlclient
try:
    import MySQLdb
except ImportError:
    print("ERROR: MySQLdb not installed. Run: pip install mysqlclient")
    sys.exit(1)

# ── CONFIG ─────────────────────────────────────────────────
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'          # ← Change this to your MySQL password
MYSQL_DB = 'indian_art_collective'
NEW_PASSWORD = 'password123'
# ────────────────────────────────────────────────────────────

def main():
    try:
        conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER,
                               passwd=MYSQL_PASSWORD, db=MYSQL_DB)
        cur = conn.cursor()
    except Exception as e:
        print(f"❌ Cannot connect to MySQL: {e}")
        print("Check MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD in this script.")
        sys.exit(1)

    hashed = generate_password_hash(NEW_PASSWORD)
    print(f"Generated hash for '{NEW_PASSWORD}'")

    # Update artisans
    cur.execute("UPDATE ARTISANS SET Password = %s", (hashed,))
    print(f"  ✓ Updated {cur.rowcount} artisan password(s)")

    # Update buyers
    cur.execute("UPDATE BUYER SET Password = %s", (hashed,))
    print(f"  ✓ Updated {cur.rowcount} buyer password(s)")

    # Update admin
    cur.execute("UPDATE ADMIN SET Password = %s", (hashed,))
    print(f"  ✓ Updated {cur.rowcount} admin password(s)")

    conn.commit()
    conn.close()

    print()
    print("✅ All passwords reset successfully!")
    print()
    print("You can now login with:")
    print("  Admin:   username=admin         password=password123")
    print("  Artisan: email=sunita@artisan.com  password=password123")
    print("  Buyer:   email=arjun@buyer.com     password=password123")

if __name__ == '__main__':
    main()
