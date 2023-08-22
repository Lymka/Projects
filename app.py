from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import psycopg2
import bcrypt
import os
import configparser

app = Flask(__name__)

config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.cfg')

config = configparser.ConfigParser()
config.read(config_path)

app.secret_key = config.get('APP', 'SECRET_KEY')

login_manager = LoginManager(app)

db_config = {
    'host': config.get('DATABASE', 'DB_HOST'),
    'database': config.get('DATABASE', 'DB_NAME'),
    'user': config.get('DATABASE', 'DB_USER'),
    'password': config.get('DATABASE', 'DB_PASSWORD')
}

class User(UserMixin):
    def __init__(self, login):
        self.id = login

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id) 

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def create_category(category_data):
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
            INSERT INTO categories (category_name, dimensions, description, price, image_path)
            VALUES (%s, %s, %s, %s, %s)
        ''', (category_data['category_name'], category_data['dimensions'], category_data['description'], category_data['price'], category_data['image_path']))

        cursor.close()
        connection.close()

        print("Категория успешно добавлена.")
        return True
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении категории: {e}")
        return False


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

        cursor.execute('''
            SELECT category_id, category_name, dimensions, description, price, image_path FROM categories
        ''')
        categories = cursor.fetchall()

        cursor.close()
        connection.close()

        return categories
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

        cursor.execute('''
            SELECT category_name, dimensions, description, price, image_path
            FROM categories
            WHERE category_id = %s
        ''', (category_id,))
        category = cursor.fetchone()

        cursor.close()
        connection.close()

        return category
    except psycopg2.Error as e:
        print(f"Ошибка при получении данных о категории: {e}")
        return None



def update_category(category_id, new_category_data):
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
            UPDATE categories
            SET category_name = %s,
                dimensions = %s,
                description = %s,
                price = %s,
                image_path = %s
            WHERE category_id = %s
        ''', (new_category_data['category_name'], new_category_data['dimensions'], new_category_data['description'], new_category_data['price'], new_category_data['image_path'], category_id))

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

        cursor.execute('''
            INSERT INTO products (product_name, price, quantity, image_path, category_id)
            VALUES (%s, %s, %s, %s, %s)
        ''', (product_data['product_name'], product_data['price'], product_data['quantity'], product_data['image_path'], product_data['category_id']))

        cursor.close()
        connection.close()

        print("Товар успешно добавлена.")
        return True
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении товара: {e}")
        return False


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

        cursor.execute('''
            SELECT p.product_id, p.product_name, p.price, p.quantity, p.image_path, p.category_id, c.category_name
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
        ''')
        products = cursor.fetchall()

        cursor.close()
        connection.close()

        print("Список товаров:")
        for product in products:
            print(product)

        return products
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

        cursor.execute('''
            SELECT products.product_id, products.product_name, products.price, products.quantity, products.image_path, categories.category_id
            FROM products
            LEFT JOIN categories ON products.category_id = categories.category_id
            WHERE products.product_id = %s
        ''', (product_id,))
        product = cursor.fetchone()

        cursor.close()
        connection.close()

        return product
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

        cursor.execute('''
            UPDATE products
            SET product_name = %s, price = %s, quantity = %s, image_path = %s, category_id = %s
            WHERE product_id = %s
        ''', (product_data['product_name'], product_data['price'], product_data['quantity'], product_data['image_path'], product_data['category_id'], product_id))

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


def create_user(login, password):
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
        ''', (login, password))

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


@app.route('/')
def index():
    categories = read_categories()
    return render_template('index.html', categories=categories)


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/admin')
@login_required
def admin_home():
    current_page = 'admin'
    return render_template('admin-home.html', current_page=current_page)

@app.route('/admin/products')
@login_required
def admin_products():
    current_page = 'products'
    products = read_products()
    return render_template('admin-products.html', products=products, current_page=current_page)

@app.route('/admin/categories')
@login_required
def admin_categories():
    current_page = 'categories'
    categories = read_categories()
    return render_template('admin-categories.html', categories=categories, current_page=current_page)


@app.route('/admin/category', methods=['POST', 'GET'])
@login_required
def admin_create_category():
    if request.method == "POST":
        category_name = request.form['category_name']
        dimensions = request.form['dimensions']
        description = request.form['description']
        price = request.form['price']
        image_path = request.form['image_path']

        category_data = {
            'category_name': category_name,
            'dimensions': dimensions,
            'description': description,
            'price': price,
            'image_path': image_path
        }

        if create_category(category_data):
            return redirect('/admin/categories')
        
    elif request.method == 'GET':
        return render_template('admin-category-edit.html')


@app.route('/admin/product', methods=['POST', 'GET'])
@login_required
def admin_create_product():
    if request.method == "POST":
        product_name = request.form['product_name']
        price = request.form['price']
        quantity = request.form['quantity']
        image_path = request.form['image_path']
        category_id = request.form['category_id']

        product_data = {
            'product_name': product_name,
            'price': price,
            'quantity': quantity,
            'image_path': image_path,
            'category_id': category_id
        }

        if create_product(product_data):
            return redirect('/admin/products')
        
    elif request.method == 'GET':
        categories = read_categories()
        return render_template('admin-product-edit.html', categories=categories)


@app.route('/admin/category/delete/<int:category_id>', methods=['GET'])
@login_required
def admin_delete_category(category_id):
    delete_category(category_id)
    return redirect('/admin/categories')


@app.route('/admin/product/delete/<int:product_id>', methods=['GET'])
@login_required
def admin_delete_product(product_id):
    delete_product(product_id)
    return redirect('/admin/products')


@app.route('/admin/category/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_category(category_id):
    edit_mode = True
    category_data = read_category_by_id(category_id)

    if request.method == 'POST':
        category_name = request.form['category_name']
        dimensions = request.form['dimensions']
        description = request.form['description']
        price = request.form['price']
        image_path = request.form['image_path']

        category_data = {
            'category_name': category_name,
            'dimensions': dimensions,
            'description': description,
            'price': price,
            'image_path': image_path
        }

        update_category(category_id, category_data)
        return redirect('/admin/categories')

    return render_template('admin-category-edit.html', edit_mode=edit_mode, category_data=category_data)


@app.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_product(product_id):
    edit_mode = True
    product_data = read_product_by_id(product_id)
    categories = read_categories()

    if request.method == 'POST':
        product_name = request.form['product_name']
        price = request.form['price']
        quantity = request.form['quantity']
        image_path = request.form['image_path']
        category_id = request.form['category_id']

        product_data = {
            'product_name': product_name,
            'price': price,
            'quantity': quantity,
            'image_path': image_path,
            'category_id': category_id
        }

        update_product(product_id, product_data)
        return redirect('/admin/products')

    return render_template('admin-product-edit.html', edit_mode=edit_mode, product_data=product_data, categories=categories)


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
            user = User(login)
            login_user(user)
            return jsonify({'message': 'Выполняется вход.'}), 200
        else:
            error_message = 'Неверные учетные данные. Пожалуйста, попробуйте снова.'
            return render_template('login.html', error=error_message)
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run()