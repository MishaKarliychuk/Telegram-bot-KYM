import sqlite3

_connection = None
def get_connection():
    global _connection
    if _connection == None:
        _connection = sqlite3.connect('users.db', check_same_thread=False)
    return _connection

def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS users')
    c. execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        status INT,
        REGION TEXT,
        MARK TEXT,
        TYPE_OF_MARK TEXT,
        FROM_PRICE TEXT,
        TO_PRICE INT,
        FROM_YEAR INT,
        TO_YEAR INT,
        PETROL TEXT,
        KPP TEXT,
        FROM_MILEAGE INT,
        TO_MILEAGE TEXT,
        url TEXT
    )""")
    conn.commit()

init_db()
##########


def take_user(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?',([id]))
    return c.fetchone()

def take_users_status(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE status = ?',([id]))
    return c.fetchall()

def take_users_mark(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f'SELECT * FROM users WHERE MARK = "{id}"')
    return c.fetchall()

def take_users_geo(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f'SELECT * FROM users WHERE REGION = "{id}"')
    return c.fetchall()

def take_users_from_year(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE FROM_YEAR = ?',([id]))
    return c.fetchall()

def take_all_user():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    return c.fetchall()

def add_user(idd):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f'INSERT INTO users (user_id, status ,REGION, MARK, TYPE_OF_MARK, FROM_PRICE, TO_PRICE,TO_YEAR, FROM_YEAR, PETROL,KPP, FROM_MILEAGE, TO_MILEAGE) VALUES ({idd}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)')
    conn.commit()

def upd_url(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET url = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_geo(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET REGION = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_price_from(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET FROM_PRICE = ? WHERE user_id = ?',(info, id))
    conn.commit()

    
def upd_price_to(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET TO_PRICE = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_mark(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET MARK = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_type_mark(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET TYPE_OF_MARK = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_year_from(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET FROM_YEAR = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_year_to(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET TO_YEAR = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_petrol(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET PETROL = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_kpp(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET KPP = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_mielege_from(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET FROM_MILEAGE = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_mielege_to(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET TO_MILEAGE = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_status(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET status = ? WHERE user_id = ?',(info, id))
    conn.commit()

def upd_url(id,info):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET url = ? WHERE user_id = ?',(info, id))
    conn.commit()

def delete_u(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE user_id=?',(id,))
    conn.commit()