import psycopg
from psycopg.rows import dict_row

conn = psycopg.connect(
    dbname="teubanco",
    user="teuusuario",
    password="tuasenha",
    host="localhost",
    port="5432",
    row_factory=dict_row
)

def get_meaning_by_code(code):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hieroglyphs WHERE code = %s", (code,))
        result = cur.fetchone()
        return result
