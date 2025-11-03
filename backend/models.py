from flask_mysqldb import MySQL
import MySQLdb.cursors
import bcrypt
import jwt
import datetime
from config import Config

mysql = MySQL()

def init_db(app):
    app.config['MYSQL_HOST'] = Config.MYSQL_HOST
    app.config['MYSQL_USER'] = Config.MYSQL_USER
    app.config['MYSQL_PASSWORD'] = Config.MYSQL_PASSWORD
    app.config['MYSQL_DB'] = Config.MYSQL_DB
    app.config['MYSQL_PORT'] = Config.MYSQL_PORT
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    
    mysql.init_app(app)
    
    # Create tables if they don't exist
    with app.app_context():
        cursor = mysql.connection.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                phone VARCHAR(20),
                address TEXT,
                date_of_birth DATE,
                security_question VARCHAR(255),
                security_answer VARCHAR(255),
                preferences JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Cars table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INT AUTO_INCREMENT PRIMARY KEY,
                make VARCHAR(50) NOT NULL,
                model VARCHAR(50) NOT NULL,
                year INT NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                type VARCHAR(50) NOT NULL,
                horsepower INT,
                transmission VARCHAR(50),
                fuel_type VARCHAR(50),
                mileage INT,
                seats INT,
                features TEXT,
                image_url VARCHAR(255),
                is_available BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Shopping cart table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cart_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                car_id INT NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (car_id) REFERENCES cars(id),
                UNIQUE KEY unique_user_car (user_id, car_id)
            )
        ''')
        
        # Insert sample cars if table is empty
        cursor.execute("SELECT COUNT(*) as count FROM cars")
        result = cursor.fetchone()
        
        if result['count'] == 0:
            sample_cars = [
                ('BMW', 'M5 Competition', 2023, 105900.00, 'Sedan', 617, '8-Speed Automatic', 'Gasoline', 0, 5, 'Leather Seats, Sunroof, Navigation', 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'),
                ('Mercedes-Benz', 'S-Class', 2023, 111100.00, 'Sedan', 496, '9-Speed Automatic', 'Gasoline', 0, 5, 'Premium Sound, Massage Seats, Panoramic Roof', 'https://images.unsplash.com/photo-1555215695-3004980ad54e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'),
                ('Audi', 'RS7 Sportback', 2023, 119995.00, 'Sedan', 591, '8-Speed Automatic', 'Gasoline', 0, 5, 'Quattro AWD, Sport Package, Premium Interior', 'https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'),
                ('Porsche', 'Cayenne', 2023, 85000.00, 'SUV', 335, '8-Speed Automatic', 'Gasoline', 0, 5, 'Premium Package, Sport Chrono, LED Headlights', 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80'),
                ('Tesla', 'Model S Plaid', 2023, 94990.00, 'Sedan', 1020, 'Single-Speed', 'Electric', 0, 5, 'Autopilot, Glass Roof, Premium Audio', 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2071&q=80'),
                ('BMW', 'X5 M Competition', 2023, 78900.00, 'SUV', 617, '8-Speed Automatic', 'Gasoline', 0, 7, 'Third Row Seating, M Sport Package, Heads-up Display', 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80')
            ]
            
            cursor.executemany('''
                INSERT INTO cars (make, model, year, price, type, horsepower, transmission, fuel_type, mileage, seats, features, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', sample_cars)
        
        mysql.connection.commit()
        cursor.close()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except:
        return None