CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT
);

CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    user_id INT,
    action TEXT,
    created_at TIMESTAMP DEFAULT now()
);

INSERT INTO users (name, email)
SELECT 'user' || i, 'user' || i || '@example.com'
FROM generate_series(1, 1000) AS i;
