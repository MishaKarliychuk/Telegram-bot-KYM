import sqlite3

_connection = None
def get_connection():
    global _connection
    if _connection == None:
        _connection = sqlite3.connect('db_setup.db', check_same_thread=False)
    return _connection

def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS db_setup')
    c. execute("""
    CREATE TABLE IF NOT EXISTS setup(
        id INTEGER PRIMARY KEY,
        menedger TEXT,
        cost INT,
        cost_sell_auto TEXT
    )""")
    conn.commit()

init_db()
##########


def add_setup(men, cost, cost_sell_auto):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f'INSERT INTO setup (menedger, cost, cost_sell_auto) VALUES ("{men}", {cost}, {cost_sell_auto})')
    conn.commit()

def take_setup():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM setup')
    return c.fetchone()

def upd_men(info):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f'UPDATE setup SET menedger = "{info}" WHERE id = 1')
    conn.commit()

def upd_cost(info):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f'UPDATE setup SET cost = {info} WHERE id = 1')
    conn.commit()

def upd_cost_sell_auto(info):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f'UPDATE setup SET cost_sell_auto = {info} WHERE id = 1')
    conn.commit()