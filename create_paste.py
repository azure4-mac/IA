from dotenv import load_dotenv
import psycopg
import os
import re

output_dir = "dataset"
os.makedirs(output_dir, exist_ok=True)

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não definida no .env")

with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT gardiner FROM hieroglifo")
        gardiners = cursor.fetchall()

for (gardiner,) in gardiners:
    codigo = gardiner.strip()
    if re.match(r"^[A-Z]+\d+$", codigo):
        caminho = os.path.join(output_dir, codigo)
        os.makedirs(caminho, exist_ok=True)
        print(f"Pasta criada: {caminho}")
