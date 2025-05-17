from dotenv import load_dotenv
import os
import psycopg

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg.connect(DATABASE_URL)

def get_hieroglyph(code):
    with conn.cursor() as cur:
        # Busca dados básicos do hieróglifo
        cur.execute("""
            SELECT id, gardiner_code, description, ideogram, notes 
            FROM hieroglyph 
            WHERE gardiner_code = %s
        """, (code,))
        row = cur.fetchone()
        if not row:
            return None

        hieroglyph_id = row[0]
        gardiner_code = row[1]
        description = row[2]
        ideogram = row[3]
        notes = row[4]

        # Busca imagens relacionadas
        cur.execute("""
            SELECT image_url, description 
            FROM hieroglyph_images 
            WHERE hieroglyph_id = %s
        """, (hieroglyph_id,))
        images = cur.fetchall()

        images_list = []
        for img_url, img_desc in images:
            images_list.append({
                "image_url": img_url,
                "description": img_desc
            })

        return {
            "gardiner_code": gardiner_code,
            "description": description,
            "ideogram": ideogram,
            "notes": notes,
            "images": images_list
        }
