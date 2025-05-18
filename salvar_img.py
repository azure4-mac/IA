from PIL import Image
import os
caminho_img="caminho/para/sua/imagem.png"
nome_classe="A1"

def salvar_no_dataset(caminho_img, nome_classe, pasta_dataset='dataset', tamanho=(64, 64)):
    imagem = Image.open(caminho_img).convert('RGBA')

    imagem_redimensionada = imagem.resize(tamanho, Image.LANCZOS)

    pasta_classe = os.path.join(pasta_dataset, nome_classe)
    os.makedirs(pasta_classe, exist_ok=True)

    nome_arquivo = os.path.basename(caminho_img)
    caminho_final = os.path.join(pasta_classe, nome_arquivo)

    imagem_redimensionada.save(caminho_final)

    print(f"Imagem salva em: {caminho_final}")
