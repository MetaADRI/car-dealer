from flask import Blueprint, request, jsonify
from models import mysql, verify_token

cart_bp = Blueprint('cart', __name__)

def get_user_id_from_token():
    token = request.headers.get('Authorization')
    if not token:
        return None
    return verify_token(token.replace('Bearer ', ''))

@cart_bp.route('/cart', methods=['GET'])
def get_cart():
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT c.*, ci.id as cart_item_id 
            FROM cart_items ci 
            JOIN cars c ON ci.car_id = c.id 
            WHERE ci.user_id = %s
        ''', (user_id,))
        cart_items = cursor.fetchall()
        cursor.close()
        
        # Convert Decimal to float
        for item in cart_items:
            item['price'] = float(item['price'])
        
        return jsonify({'cart': cart_items})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/cart/add/<int:car_id>', methods=['POST'])
def add_to_cart(car_id):
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        cursor = mysql.connection.cursor()
        
        # Check if car exists and is available
        cursor.execute('SELECT id FROM cars WHERE id = %s AND is_available = TRUE', (car_id,))
        car = cursor.fetchone()
        
        if not car:
            return jsonify({'error': 'Car not available'}), 404
        
        # Check if already in cart
        cursor.execute('SELECT id FROM cart_items WHERE user_id = %s AND car_id = %s', (user_id, car_id))
        existing_item = cursor.fetchone()
        
        if existing_item:
            return jsonify({'error': 'Car already in cart'}), 400
        
        # Add to cart
        cursor.execute('INSERT INTO cart_items (user_id, car_id) VALUES (%s, %s)', (user_id, car_id))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Car added to cart successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/cart/remove/<int:car_id>', methods=['DELETE'])
def remove_from_cart(car_id):
    user_id = get_user_id_from_token()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM cart_items WHERE user_id = %s AND car_id = %s', (user_id, car_id))
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Item not found in cart'}), 404
        
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Item removed from cart'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500