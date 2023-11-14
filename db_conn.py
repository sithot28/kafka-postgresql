# db_conn.py
import psycopg2
import psycopg2.pool

class DatabaseConnection:
    def __init__(self, db_config):
        self.pool = psycopg2.pool.SimpleConnectionPool(1, 10, **db_config)

    def insert_into_db(self, data):
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO sales_transaction (sales_id, issued_date, quantity, amount) VALUES (%s, %s, %s, %s)",
                    (data[0], data[1], data[2], data[3])
                )
                conn.commit()
        except psycopg2.DatabaseError as e:
            print('Error insert: ',data)
            conn.rollback()
            raise e
        finally:
            self.pool.putconn(conn)

    def close_pool(self):
        self.pool.closeall()

