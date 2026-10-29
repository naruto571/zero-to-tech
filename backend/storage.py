import sqlite3

DB_FILE = "history.db"

def get_conn(): #定义怎么连接数据库的方式，每次连接数据库都要调用这个函数
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row #让查询结果带上列名(默认是元组)
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        text TEXT,
        score REAL,
        label TEXT,
        pinyin TEXT,
        created_at TEXT
    )
    """)
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_history_session_created "
        "ON history(session_id, created_at)" #将session_id和created_at都创建索引，
        #顺序是由说法的，先创建的是为了筛选的，后创建的是为了排序的
    )
    conn.commit()
    conn.close()

def save_record(session_id, record): 
    #这里的参数表示每次存的时候，调用方都要交代一下这条记录属于哪个session_id，哪个会话
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (session_id, text, score, label, pinyin, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?)",
        [session_id, record["text"], record["score"],
         record["label"], record["pinyin"], record["created_at"]],
    )
    conn.commit()
    conn.close()

def get_history(session_id, limit):
    conn = get_conn()
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT * FROM history WHERE session_id = ? ORDER BY created_at DESC LIMIT ?",
        [session_id, limit],
    ).fetchall()
    conn.close()

    records = []
    for row in rows:
        records.append(dict(row))
    return records




