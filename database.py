import psycopg2
import os
import configparser

config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.cfg')

config = configparser.ConfigParser()
config.read(config_path)

db_config = {
    'host': config.get('DATABASE', 'DB_HOST'),
    'database': config.get('DATABASE', 'DB_NAME'),
    'user': config.get('DATABASE', 'DB_USER'),
    'password': config.get('DATABASE', 'DB_PASSWORD')
}

def database_exists(database_name):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (database_name,))
        exists = cursor.fetchone()

        cursor.close()
        connection.close()

        return exists is not None
    except psycopg2.Error as e:
        print(f"Ошибка при проверке наличия базы данных: {e}")
        return False

def create_database():
    try:
        if not database_exists(db_config['database']):
            connection = psycopg2.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password']
            )
            connection.autocommit = True
            cursor = connection.cursor()

            cursor.execute(f"CREATE DATABASE {db_config['database']} ENCODING 'UTF8' TEMPLATE template0")

            cursor.close()
            connection.close()

            print(f"База данных '{db_config['database']}' успешно создана.")
        else:
            print(f"База данных '{db_config['database']}' уже существует.")
    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных: {e}")

def drop_tables():
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True

        cursor = connection.cursor()

        cursor.execute('''
            DROP TABLE IF EXISTS products CASCADE
        ''')

        cursor.execute('''
            DROP TABLE IF EXISTS categories CASCADE
        ''')

        cursor.execute('''
            DROP TABLE IF EXISTS users CASCADE
        ''')

        cursor.close()
        connection.close()

        print("Таблицы успешно удалены.")
    except psycopg2.Error as e:
        print(f"Ошибка при удалении таблиц: {e}")

def create_tables():

    drop_tables()

    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True

        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                category_id SERIAL PRIMARY KEY,
                category_name VARCHAR(100) NOT NULL,
                image_path VARCHAR(255) NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id SERIAL PRIMARY KEY,
                product_name VARCHAR(100) NOT NULL,
                price NUMERIC NOT NULL,
                quantity INTEGER NOT NULL,
                image_path VARCHAR(255) NOT NULL,
                category_id INTEGER REFERENCES categories(category_id) ON DELETE CASCADE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                login VARCHAR(100) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')

        cursor.close()
        connection.close()

        print("Таблицы успешно созданы.")
    except psycopg2.Error as e:
        print(f"Ошибка при создании таблиц: {e}")

if __name__ == "__main__":
    create_database()
    create_tables()