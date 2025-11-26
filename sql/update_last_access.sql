UPDATE users
SET last_access = NOW()
WHERE id = %s;
