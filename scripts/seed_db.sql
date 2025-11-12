CREATE TABLE IF NOT EXISTS my_table (
    id SERIAL PRIMARY KEY,
    col1 TEXT,
    col2 TEXT,
    some_col TEXT
);

-- seed some rows
INSERT INTO my_table (col1, col2, some_col)
SELECT md5(random()::text), md5(random()::text), 'value'
FROM generate_series(1, 1000);
