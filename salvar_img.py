import os
from PIL import Image
import psycopg
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
DATASET_DIR = 'dataset'
TAMANHO = (64, 64)

def redimensionar_e_salvar(imagem_path):
    imagem = Image.open(imagem_path).convert('RGBA')
    imagem_redimensionada = imagem.resize(TAMANHO, Image.LANCZOS)
    imagem_redimensionada.save(imagem_path)

def processar_imagens_do_hieroglifo(gardiner, cursor):
    pasta_classe = os.path.join(DATASET_DIR, gardiner)

    if not os.path.exists(pasta_classe):
        print(f"Pasta {pasta_classe} não existe, pulando.")
        return

    arquivos = [f for f in os.listdir(pasta_classe) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    print(f"Encontradas {len(arquivos)} imagens na pasta {pasta_classe}.")

    for arquivo in arquivos:
        caminho_img = os.path.join(pasta_classe, arquivo)
        try:
            redimensionar_e_salvar(caminho_img)
            print(f"Imagem redimensionada e salva: {caminho_img}")

            cursor.execute('''
                INSERT INTO hieroglifo_images (hieroglifo_gardiner, image_path, description)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
            ''', (gardiner, caminho_img, None))

        except Exception as e:
            print(f"Erro ao processar imagem {caminho_img}: {e}")

def main():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT gardiner FROM hieroglifo')
            hieroglifos = cursor.fetchall()

            for (gardiner,) in hieroglifos:
                print(f"Processando hieroglifo gardiner={gardiner}")
                processar_imagens_do_hieroglifo(gardiner, cursor)

        conn.commit()
        print("Processamento finalizado e commit realizado.")
