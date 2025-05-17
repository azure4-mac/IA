CREATE TABLE IF NOT EXISTS hieroglyphs (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    transliteration VARCHAR(50),
    meaning TEXT,
    category CHAR(1)
);

-- Exemplo de inserção
INSERT INTO hieroglyphs (code, transliteration, meaning, category)
VALUES
('A15', 'iA', 'adorar', 'A'),
('nTr', 'nṯr', 'deus', 'N'),
('nfr', 'nfr', 'bom', 'F')
ON CONFLICT DO NOTHING;
