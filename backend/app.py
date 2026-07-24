from flask import Flask
from flask_cors import CORS
from config import Config
from models import init_db
from auth import auth_bp
from cars import cars_bp
from cart import cart_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
init_db(app)

# Enable CORS — allow Cloudflare Pages origin
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(cars_bp, url_prefix='/api')
app.register_blueprint(cart_bp, url_prefix='/api')


# Health check endpoint
@app.route('/api/health')
def health_check():
    return {'status': 'healthy', 'message': 'Car Dealership API is running'}


if __name__ == '__main__':
    app.run(debug=True, port=5000)
