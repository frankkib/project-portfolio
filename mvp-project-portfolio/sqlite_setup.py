import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('frank.db')

# Create a cursor object to execute SQL statements
cursor = conn.cursor()

# Execute the SQL statements
cursor.executescript('''
    -- Create a new table with the desired structure
    CREATE TABLE IF NOT EXISTS houses (
        id INTEGER PRIMARY KEY,
        location TEXT,
        price REAL,
        description TEXT,
        created_at TIMESTAMP,
        is_available BOOLEAN,
        photo_filename TEXT NOT NULL,
        user_id INTEGER
    );

    -- Copy the data from the old table to the new table
    INSERT INTO house (id, location, price, description, created_at, is_available, photo_filename, user_id)
    SELECT id, location, price, description, created_at, is_available, '', user_id
    FROM houses;

''')

# Commit the changes and close the connection
conn.commit()
conn.close()
