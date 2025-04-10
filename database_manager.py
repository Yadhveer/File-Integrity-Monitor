import psycopg2

class DatabaseManager:
    def __init__(self, host, user, password, database, port):
        self.connection = psycopg2.connect(
            host=host,
            dbname=database,
            user=user,
            password=password,
            port=port
        )
        self.cursor = self.connection.cursor()

    def view_db(self):
        self.cursor.execute("SELECT name, last_modified FROM hash;")
        files = self.cursor.fetchall()
        return files  

    
    def add_to_db(self, filename, hash_value):
        self.cursor.execute("""
        INSERT INTO hash (name, hash_value, last_modified)
        VALUES (%s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (name) DO UPDATE
        SET hash_value = EXCLUDED.hash_value,
        last_modified = CURRENT_TIMESTAMP;
        """, (filename, hash_value))

        self.connection.commit()

    def remove_from_db(self, filename):
        self.cursor.execute("DELETE FROM hash WHERE name = %s;", (filename,))
        self.connection.commit()


    def fetch_all_hashes(self):
        self.cursor.execute("SELECT name, hash_value FROM hash;")
        return self.cursor.fetchall()  


    def close(self):
        self.connection.close()