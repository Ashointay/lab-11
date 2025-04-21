CREATE TABLE IF NOT EXISTS PhoneBook (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    phone TEXT NOT NULL
);

CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(id INT, first_name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM PhoneBook
    WHERE first_name ILIKE '%' || pattern || '%'
       OR phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM PhoneBook WHERE first_name = p_name) THEN
        UPDATE PhoneBook SET phone = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO PhoneBook (first_name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, first_name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT PhoneBook.id, PhoneBook.first_name::TEXT, PhoneBook.phone::TEXT
    FROM PhoneBook
    ORDER BY PhoneBook.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM PhoneBook
    WHERE (p_name IS NOT NULL AND first_name = p_name)
       OR (p_phone IS NOT NULL AND phone = p_phone);
END;
$$;