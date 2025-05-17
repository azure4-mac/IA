from dotenv import load_dotenv
import os
import psycopg

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Cria a conexão
conn = psycopg.connect(DATABASE_URL)

def get_hieroglyph(code):
    with conn.cursor() as cur:
        # Busca o hieróglifo pelo código de Gardiner
        cur.execute("""
            SELECT id, gardiner_code, unicode_code, description, ideogram, notes, symbol
            FROM hieroglyph 
            WHERE gardiner_code = %s
        """, (code,))
        
        row = cur.fetchone()
        if not row:
            return None

        hieroglyph_id = row[0]
        gardiner_code = row[1]
        unicode_code = row[2]
        description = row[3]
        ideogram = row[4]
        notes = row[5]
        symbol =[6]

        # Busca imagens relacionadas
        cur.execute("""
            SELECT image_url, description 
            FROM hieroglyph_images 
            WHERE hieroglyph_id = %s
        """, (hieroglyph_id,))
        
        images = cur.fetchall()

        images_list = [
            {"image_url": img[0], "description": img[1]}
            for img in images
        ]

        return {
            "gardiner_code": gardiner_code,
            "unicode_code": unicode_code,
            "description": description,
            "ideogram": ideogram,
            "notes": notes,
            "images": images_list
        }
