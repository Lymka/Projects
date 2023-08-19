import psycopg2
import os
import configparser
import random
import string

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
                dimensions VARCHAR(100) NOT NULL,
                description VARCHAR(255) NOT NULL,
                price INTEGER NOT NULL,
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


def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def generate_data():
    connection = psycopg2.connect(
        host=db_config['host'],
        database=db_config['database'],
        user=db_config['user'],
        password=db_config['password']
    )
    connection.autocommit = True

    cursor = connection.cursor()

    # Generate categories
    for _ in range(10):
        category_name = generate_random_string(10)
        dimensions = f"{random.randint(1, 100)}x{random.randint(1, 100)}x{random.randint(1, 100)}"
        description = generate_random_string(30)
        price = random.randint(50, 500)
        image_path = '/static/images/' + generate_random_string(10) + '.jpg'

        cursor.execute('''
            INSERT INTO categories (category_name, dimensions, description, price, image_path)
            VALUES (%s, %s, %s, %s, %s)
        ''', (category_name, dimensions, description, price, image_path))

    # Generate products
    for _ in range(100):
        product_name = generate_random_string(15)
        price = round(random.uniform(10, 1000), 2)
        quantity = random.randint(1, 100)
        image_path = '/static/images/' + generate_random_string(10) + '.jpg'
        category_id = random.randint(1, 10)

        cursor.execute('''
            INSERT INTO products (product_name, price, quantity, image_path, category_id)
            VALUES (%s, %s, %s, %s, %s)
        ''', (product_name, price, quantity, image_path, category_id))

    cursor.close()
    connection.close()


if __name__ == "__main__":
    create_database()
    create_tables()
    generate_data()