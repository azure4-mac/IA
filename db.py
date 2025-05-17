from dotenv import load_dotenv
import os
import psycopg

# Carrega variáveis do .env
load_dotenv()

# Conexão com o banco de dados Neon
DATABASE_URL = os.getenv("DATABASE_URL")

# Cria a conexão
conn = psycopg.connect(DATABASE_URL)

# Função para buscar um hieróglifo pelo código MdC (ex: A15)
def get_hieroglyph(code):
    with conn.cursor() as cur:
        cur.execute("SELECT transliteration, meaning, img_url FROM hieroglyphs WHERE code = %s", (code,))
        row = cur.fetchone()
        if row:
            return {
                "transliteration": row[0],
                "meaning": row[1],
                "img_url": row[2]   
            }
        return None
