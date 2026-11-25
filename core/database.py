import sqlite3,json,os
from contextlib import closing
from pathlib import Path
from datetime import datetime,timezone
DB_PATH=Path(os.environ.get('EFICIAGRO_DB',str(Path(__file__).resolve().parents[1]/'database/eficiagro.db')))

def connect():
    DB_PATH.parent.mkdir(parents=True,exist_ok=True)
    return sqlite3.connect(DB_PATH,timeout=15)

def init_db():
    with closing(connect()) as conn, conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS analises (
          id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL,
          propriedade TEXT NOT NULL, municipio TEXT, cultura TEXT, sistema TEXT,
          dados_json TEXT NOT NULL, resultados_json TEXT NOT NULL, diagnostico_json TEXT NOT NULL)''')

def save_analysis(data,scenarios,diagnosis):
    init_db()
    with closing(connect()) as conn, conn:
        cur=conn.execute('INSERT INTO analises (created_at,propriedade,municipio,cultura,sistema,dados_json,resultados_json,diagnostico_json) VALUES (?,?,?,?,?,?,?,?)',
            (datetime.now(timezone.utc).isoformat(timespec='seconds'),data.propriedade,data.municipio,data.cultura,data.sistema,
            json.dumps(data.to_dict(),ensure_ascii=False,allow_nan=False),json.dumps([s.to_dict() for s in scenarios],ensure_ascii=False,allow_nan=False),json.dumps(diagnosis,ensure_ascii=False,allow_nan=False)))
        return cur.lastrowid

def list_analyses(limit=30):
    init_db()
    with closing(connect()) as conn, conn:
        return conn.execute('SELECT id,created_at,propriedade,cultura,sistema FROM analises ORDER BY id DESC LIMIT ?',(limit,)).fetchall()

def get_analysis(analysis_id):
    init_db()
    with closing(connect()) as conn, conn:
        row=conn.execute('SELECT dados_json,resultados_json,diagnostico_json FROM analises WHERE id=?',(int(analysis_id),)).fetchone()
    return dict(zip(['entradas','cenarios','diagnostico'],map(json.loads,row))) if row else None
