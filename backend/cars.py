from flask import Blueprint, request, jsonify
from models import get_db_connection
from psycopg2.extras import RealDictCursor

cars_bp = Blueprint('cars', __name__)


@cars_bp.route('/cars', methods=['GET'])
def get_cars():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        brand = request.args.get('brand')
        car_type = request.args.get('type')
        price_min = request.args.get('price_min')
        price_max = request.args.get('price_max')
        year = request.args.get('year')

        query = 'SELECT * FROM cars WHERE is_available = TRUE'
        params = []

        if brand and brand != 'all':
            query += ' AND make = %s'
            params.append(brand)

        if car_type and car_type != 'all':
            query += ' AND type = %s'
            params.append(car_type)

        if price_min:
            query += ' AND price >= %s'
            params.append(float(price_min))

        if price_max:
            query += ' AND price <= %s'
            params.append(float(price_max))

        if year and year != 'all':
            query += ' AND year = %s'
            params.append(int(year))

        query += ' ORDER BY price ASC'

        cursor.execute(query, params)
        cars = cursor.fetchall()
        cursor.close()

        for car in cars:
            car['price'] = float(car['price'])
            car['id'] = car['id']

        return jsonify({'cars': cars})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()


@cars_bp.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute('SELECT * FROM cars WHERE id = %s AND is_available = TRUE', (car_id,))
        car = cursor.fetchone()
        cursor.close()

        if not car:
            return jsonify({'error': 'Car not found'}), 404

        car['price'] = float(car['price'])
        return jsonify({'car': car})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()
