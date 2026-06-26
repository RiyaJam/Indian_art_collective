from flask_mysqldb import MySQL

mysql = MySQL()

def init_db(app):
    mysql.init_app(app)

def get_cursor():
    return mysql.connection.cursor()

def commit():
    mysql.connection.commit()
