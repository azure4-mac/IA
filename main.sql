-- Inserir um novo hieróglifo
INSERT INTO hieroglyph (
    gardiner_code, 
    unicode_code, 
    description, 
    ideogram, 
    notes
) VALUES (
    '', -- Código Gardiner
    '', -- Código Unicode
    '', -- Descrição do hieróglifo
    '', -- Ideograma (se aplicável)
    '' -- Notas adicionais
);

INSERT INTO hieroglyph_images (
    hieroglyph_id,
    image_url,
    description
) VALUES (
    1,  -- id do hieróglifo existente mudar sempre q a img for de outro pfv
    '',  -- URL da imagem
    ''    -- descrição da imagem
);

