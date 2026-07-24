from flask import Blueprint, request, jsonify
from models import get_db_connection, hash_password, check_password, create_token, verify_token
from psycopg2.extras import RealDictCursor
import re

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    conn = None
    try:
        data = request.get_json()

        required_fields = ['username', 'email', 'password', 'firstName', 'lastName']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', data['email']):
            return jsonify({'error': 'Invalid email format'}), 400

        if len(data['password']) < 8:
            return jsonify({'error': 'Password must be at least 8 characters'}), 400

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute('SELECT id FROM users WHERE username = %s OR email = %s',
                       (data['username'], data['email']))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'error': 'Username or email already exists'}), 400

        hashed_password = hash_password(data['password'])

        cursor.execute('''
            INSERT INTO users (username, email, password_hash, first_name, last_name, phone, address, date_of_birth, security_question, security_answer, preferences)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (
            data['username'],
            data['email'],
            hashed_password,
            data['firstName'],
            data['lastName'],
            data.get('phone'),
            data.get('address'),
            data.get('dob'),
            data.get('securityQuestion'),
            data.get('securityAnswer'),
            data.get('preferences')
        ))

        result = cursor.fetchone()
        user_id = result['id']
        conn.commit()
        cursor.close()

        token = create_token(user_id)

        return jsonify({
            'message': 'User created successfully',
            'token': token,
            'user': {
                'id': user_id,
                'username': data['username'],
                'email': data['email'],
                'firstName': data['firstName'],
                'lastName': data['lastName']
            }
        }), 201

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()


@auth_bp.route('/login', methods=['POST'])
def login():
    conn = None
    try:
        data = request.get_json()

        login_id = data.get('username') or data.get('email')
        if not login_id or not data.get('password'):
            return jsonify({'error': 'Username/email and password are required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute('''
            SELECT id, username, email, password_hash, first_name, last_name
            FROM users WHERE username = %s OR email = %s
        ''', (login_id, login_id))

        user = cursor.fetchone()
        cursor.close()

        if not user or not check_password(data['password'], user['password_hash']):
            return jsonify({'error': 'Invalid credentials'}), 401

        token = create_token(user['id'])

        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'firstName': user['first_name'],
                'lastName': user['last_name']
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()


@auth_bp.route('/verify', methods=['POST'])
def verify():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Token required'}), 401

    user_id = verify_token(token.replace('Bearer ', ''))
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT id, username, email, first_name, last_name FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'firstName': user['first_name'],
                'lastName': user['last_name']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()
