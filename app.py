from flask import Flask, render_template, request, jsonify, redirect, url_for
import psycopg2
import bcrypt

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'database': 'forest_product_catalog',
    'user': 'postgres',
    'password': '1234'
}

def create_category(category_name):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Вставка новой категории в таблицу "categories"
        cursor.execute('''
            INSERT INTO categories (category_name, image_path)
            VALUES (%s, %s)
        ''', (category_name['category_name'], category_name['image_path']))

        cursor.close()
        connection.close()

        
        print("Категория успешно добавлена.")
        return True  # Возвращаем True при успешном добавлении
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении категории: {e}")
        return False  # Возвращаем False при возникновении ошибки


def read_categories():
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Получение списка всех категорий
        cursor.execute('''
            SELECT category_id, category_name, image_path FROM categories
        ''')
        categories = cursor.fetchall()

        cursor.close()
        connection.close()

        print("Список категорий:")
        for category in categories:
            print(category)

        return categories  # Возвращаем список категорий
    except psycopg2.Error as e:
        print(f"Ошибка при получении списка категорий: {e}")
        return None


def read_category_by_id(category_id):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Получение данных о категории по её идентификатору
        cursor.execute('''
            SELECT category_name FROM categories
            WHERE category_id = %s
        ''', (category_id,))
        category = cursor.fetchone()

        cursor.close()
        connection.close()

        return category  # Возвращаем словарь с данными о категории или None, если категория не найдена
    except psycopg2.Error as e:
        print(f"Ошибка при получении данных о категории: {e}")
        return None


def update_category(category_id, new_category_name):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Обновление данных о категории
        cursor.execute('''
            UPDATE categories
            SET category_name = %s
            WHERE category_id = %s
        ''', (new_category_name, category_id))

        cursor.close()
        connection.close()

        print("Категория успешно обновлена.")
    except psycopg2.Error as e:
        print(f"Ошибка при обновлении категории: {e}")

def delete_category(category_id):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Удаление категории
        cursor.execute('''
            DELETE FROM categories
            WHERE category_id = %s
        ''', (category_id,))

        cursor.close()
        connection.close()

        print("Категория успешно удалена.")
    except psycopg2.Error as e:
        print(f"Ошибка при удалении категории: {e}")

def create_product(product_data):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Вставка нового товара в таблицу "products"
        cursor.execute('''
            INSERT INTO products (product_name, price, quantity, category_id)
            VALUES (%s, %s, %s, %s)
        ''', (product_data['product_name'], product_data['price'], product_data['quantity'], product_data['category_id']))

        cursor.close()
        connection.close()

        print("Товар успешно добавлен.")
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении товара: {e}")

def read_products():
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Получение списка всех товаров
        cursor.execute('''
            SELECT product_id, product_name, price, quantity, category_id FROM products
        ''')
        products = cursor.fetchall()

        cursor.close()
        connection.close()

        print("Список товаров:")
        for product in products:
            print(product)
    except psycopg2.Error as e:
        print(f"Ошибка при получении списка товаров: {e}")

def read_product_by_id(product_id):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Получение данных о товаре и категории по его идентификатору
        cursor.execute('''
            SELECT products.product_id, products.product_name, products.price, products.quantity, categories.category_id
            FROM products
            LEFT JOIN categories ON products.category_id = categories.category_id
            WHERE products.product_id = %s
        ''', (product_id,))
        product = cursor.fetchone()

        cursor.close()
        connection.close()

        return product  # Возвращаем словарь с данными о товаре и категории или None, если товар не найден
    except psycopg2.Error as e:
        print(f"Ошибка при получении данных о товаре: {e}")
        return None


def update_product(product_id, product_data):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Проверяем, существует ли товар с заданным product_id
        existing_product = read_product_by_id(product_id)
        if existing_product is None:
            print(f"Товар с ID {product_id} не найден. Невозможно обновить.")
            return False

        # Обновление данных о товаре
        cursor.execute('''
            UPDATE products
            SET product_name = %s, price = %s, quantity = %s, category_id = %s
            WHERE product_id = %s
        ''', (product_data['product_name'], product_data['price'], product_data['quantity'], product_data['category_id'], product_id))

        cursor.close()
        connection.close()

        print("Товар успешно обновлен.")
        return True
    except psycopg2.Error as e:
        print(f"Ошибка при обновлении товара: {e}")
        return False


def delete_product(product_id):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Удаление товара
        cursor.execute('''
            DELETE FROM products
            WHERE product_id = %s
        ''', (product_id,))

        cursor.close()
        connection.close()

        print("Товар успешно удален.")
    except psycopg2.Error as e:
        print(f"Ошибка при удалении товара: {e}")


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Функция для проверки пароля
def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_user(username, password):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Вставка нового пользователя в таблицу "users"
        cursor.execute('''
            INSERT INTO users (login, password)
            VALUES (%s, %s)
        ''', (username, password))

        cursor.close()
        connection.close()

        print("Пользователь успешно создан.")
        return True  # Возвращаем True при успешном создании пользователя
    except psycopg2.Error as e:
        print(f"Ошибка при создании пользователя: {e}")
        return False  # Возвращаем False при возникновении ошибки


def get_hashed_password(login):
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Получение хэшированного пароля пользователя по его имени
        cursor.execute('''
            SELECT password FROM users
            WHERE login = %s
        ''', (login,))
        password = cursor.fetchone()

        cursor.close()
        connection.close()

        return password[0] if password else None
    except psycopg2.Error as e:
        print(f"Ошибка при получении пароля пользователя: {e}")
        return None


@app.route('/category/<int:category_id>')
def show_category(category_id):
    category_data = read_category_by_id(category_id)
    return render_template('example_2.html', category_data=category_data)
        

@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_id(product_id):
    if request.method == 'GET':
        # Получение данных о товаре по идентификатору
        product_data = read_product_by_id(product_id)
        # Получение списка всех категорий
        categories = read_categories()
        return render_template('example.html', product_data=product_data, categories=categories)
    elif request.method == 'POST':
        # Обработка формы обновления товара
        product_name = request.form.get('product_name')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        category_id = request.form.get('category')  # Получаем ID выбранной категории из формы

        if product_name and price and quantity and category_id:
            product_data = {
                'product_name': product_name,
                'price': price,
                'quantity': quantity,
                'category_id': int(category_id)  # Преобразуем ID категории в целое число
            }
            if update_product(product_id, product_data):
                return jsonify({'message': 'Данные успешно обновлены в базе данных.'})
            else:
                return jsonify({'message': 'Произошла ошибка при обновлении данных в базе данных.'}), 500
        else:
            return jsonify({'message': 'Пожалуйста, заполните все поля формы.'}), 400


@app.route('/product')
def product():
    # Получение списка всех категорий
    categories = read_categories()
    return render_template('example.html', categories=categories)


@app.route('/save_data', methods=['POST'])
def save_product():
    product_name = request.form.get('product_name')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    category_id = request.form.get('category')  # Получаем ID выбранной категории из формы

    if product_name and price and quantity and category_id:
        product_data = {
            'product_name': product_name,
            'price': price,
            'quantity': quantity,
            'category_id': int(category_id)  # Преобразуем ID категории в целое число
        }
        create_product(product_data)
        return jsonify({'message': 'Данные успешно сохранены в базе данных.'})
    else:
        return jsonify({'message': 'Пожалуйста, заполните все поля формы.'}), 400


@app.route('/category')
def category():
    return render_template('example_2.html')


@app.route('/save_data_1', methods=['POST'])
def save_category():
    category_name = request.form.get('category_name')
    image_path = request.form.get('image_path')

    if category_name and image_path:
        category_data = {
            'category_name': category_name,
            'image_path': image_path,
        }
        create_category(category_data)
        return jsonify({'message': 'Данные успешно сохранены в базе данных.'})
    else:
        return jsonify({'message': 'Пожалуйста, заполните все поля формы.'}), 400
    

@app.route('/')
def index():
    categories = read_categories()
    return render_template('index.html', categories=categories)


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        hashed_password = hash_password(password)

        if create_user(login, hashed_password):
            return jsonify({'message': 'Пользователь успешно создан.'}), 200
        else:
            return jsonify({'message': 'Ошибка при создании пользователя.'}), 500

    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        hashed_password = get_hashed_password(login)

        if hashed_password and check_password(hashed_password, password):
            return jsonify({'message': 'Выполняется вход.'}), 200
        else:
            error_message = 'Неверные учетные данные. Пожалуйста, попробуйте снова.'
            return render_template('login.html', error=error_message)
    else:
        return render_template('login.html')


if __name__ == "__main__":
    app.run()