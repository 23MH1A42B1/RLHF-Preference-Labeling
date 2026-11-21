import json

def main():
    with open('data/seed_pairs.json', 'r', encoding='utf-8') as f:
        pairs = json.load(f)

    sql_lines = [
        '-- RLHF Preference Tool Database Initialization',
        'CREATE TABLE IF NOT EXISTS labels (',
        '    id SERIAL PRIMARY KEY,',
        '    prompt TEXT NOT NULL,',
        '    response_a TEXT NOT NULL,',
        '    response_b TEXT NOT NULL,',
        '    category VARCHAR(255) NOT NULL,',
        '    annotator_id VARCHAR(255),',
        '    chosen VARCHAR(50),',
        '    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,',
        '    labeled_at TIMESTAMP WITH TIME ZONE,',
        '    pair_id INTEGER',
        ');',
        '',
        'CREATE INDEX IF NOT EXISTS idx_labels_annotator_id ON labels(annotator_id);',
        'CREATE INDEX IF NOT EXISTS idx_labels_category ON labels(category);',
        'CREATE INDEX IF NOT EXISTS idx_labels_pair_id ON labels(pair_id);',
        ''
    ]

    for idx, p in enumerate(pairs, 1):
        prompt = p['prompt'].replace("'", "''")
        resp_a = p['response_a'].replace("'", "''")
        resp_b = p['response_b'].replace("'", "''")
        cat = p['category'].replace("'", "''")
        sql_lines.append(
            f"INSERT INTO labels (id, prompt, response_a, response_b, category, annotator_id, chosen, created_at, pair_id) "
            f"VALUES ({idx}, '{prompt}', '{resp_a}', '{resp_b}', '{cat}', NULL, NULL, NOW(), {idx}) "
            f"ON CONFLICT (id) DO NOTHING;"
        )

    sql_lines.append('')
    sql_lines.append("SELECT setval('labels_id_seq', (SELECT COALESCE(MAX(id), 1) FROM labels));")

    with open('data/init.sql', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_lines) + '\n')

    print(f"Generated data/init.sql with {len(pairs)} records.")

if __name__ == '__main__':
    main()

