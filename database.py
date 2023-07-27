import psycopg2

db_config = {
    'host': 'localhost',
    'database': 'forest_product_catalog',
    'user': 'postgres',
    'password': '1234'
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

        # Проверяем, существует ли база данных с заданным именем
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

            # Создаем новую базу данных
            cursor.execute(f"CREATE DATABASE {db_config['database']} ENCODING 'UTF8' TEMPLATE template0")

            cursor.close()
            connection.close()

            print(f"База данных '{db_config['database']}' успешно создана.")
        else:
            print(f"База данных '{db_config['database']}' уже существует.")
    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных: {e}")

def create_tables():
    try:
        # Подключение к созданной базе данных
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True

        # Создание объекта для выполнения SQL-запросов
        cursor = connection.cursor()

        # Создание таблицы с категориями
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                category_id SERIAL PRIMARY KEY,
                category_name VARCHAR(100) NOT NULL,
                image_path VARCHAR(255) NOT NULL
            )
        ''')

        # Создание таблицы с продуктами
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

        # Создание таблицы с пользователями
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id SERIAL PRIMARY KEY,
                login VARCHAR(100) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')

        # Закрываем курсор и соединение
        cursor.close()
        connection.close()

        print("Таблицы успешно созданы.")
    except psycopg2.Error as e:
        print(f"Ошибка при создании таблиц: {e}")

if __name__ == "__main__":
    create_database()
    create_tables()