# AutoElite Car Dealership - Full Stack Website

A modern, responsive car dealership website with a Python Flask backend and MySQL database.

![AutoElite](https://img.shields.io/badge/AutoElite-Car%20Dealership-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![MySQL](https://img.shields.io/badge/MySQL-XAMPP-orange)

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation Guide](#installation-guide)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Support](#support)

## Features

✨ **Frontend Features:**
- Responsive design with Bootstrap 5
- Modern UI with smooth animations
- jQuery for interactive elements
- Shopping cart functionality
- User registration and authentication
- Car inventory with filtering
- Mobile-friendly design

🔧 **Backend Features:**
- Python Flask RESTful API
- MySQL database with XAMPP
- JWT-based authentication
- User session management
- Secure password hashing
- CORS enabled for frontend communication

## Prerequisites

Before you begin, ensure you have the following installed:

### 1. XAMPP
Download and install XAMPP from [https://www.apachefriends.org](https://www.apachefriends.org)
- Includes Apache web server and MySQL database
- Available for Windows, macOS, and Linux

### 2. Python 3.8+
Download and install Python from [https://www.python.org/downloads](https://www.python.org/downloads)
- **Important**: During installation, check "Add Python to PATH"
- Verify installation by running `python --version` in command prompt

### 3. Git (Optional)
For cloning the repository from [https://git-scm.com](https://git-scm.com)

## Installation Guide

### Step 1: Get the Project Files
```bash
# Option 1: Clone with Git
git clone <repository-url>
cd car-dealership

# Option 2: Download ZIP
# Download and extract the project files to a folder called 'car-dealership'
```

### Step 2: Set Up Python Virtual Environment
```bash
# Navigate to project directory
cd car-dealership

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Your command prompt should now show (venv)
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

**If requirements.txt is missing, install manually:**
```bash
pip install Flask==2.3.3
pip install Flask-MySQLdb==1.0.1
pip install Flask-CORS==4.0.0
pip install Werkzeug==2.3.7
pip install python-dotenv==1.0.0
pip install bcrypt==4.0.1
pip install PyJWT==2.8.0
```

## Database Setup

### Step 1: Start XAMPP Services
1. Open XAMPP Control Panel
2. Click "Start" next to **Apache** and **MySQL**
3. Both should show green "Running" status
4. Leave XAMPP running in the background

### Step 2: Create Database
1. Open your web browser
2. Go to: `http://localhost/phpmyadmin`
3. Click "New" in the left sidebar
4. Enter database name: `car_dealership`
5. Click "Create"

### Step 3: Verify Database Connection
The Flask application will automatically create all necessary tables when it runs for the first time.

## Running the Application

### Step 1: Start Backend Server
```bash
# Make sure you're in the project directory and virtual environment is activated
cd backend
python app.py
```

**Expected Output:**
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
* Restarting with stat
* Debugger is active!
* Debugger PIN: XXX-XXX-XXX
```

### Step 2: Access the Website
Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
car-dealership/
├── frontend/                 # All HTML files
│   ├── index.html           # Homepage with hero section
│   ├── about.html           # About Us page
│   ├── cars.html            # Car inventory with filtering
│   └── create-account.html  # User registration form
├── backend/                 # Python Flask application
│   ├── app.py              # Main Flask application
│   ├── config.py           # Database configuration
│   ├── models.py           # Database models & setup
│   ├── auth.py             # Authentication routes
│   ├── cars.py             # Car inventory API
│   ├── cart.py             # Shopping cart API
│   └── utils.py            # Helper functions
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## API Endpoints

### 🔐 Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | User registration | No |
| POST | `/api/auth/login` | User login | No |
| POST | `/api/auth/verify` | Verify JWT token | Yes |

### 🚗 Cars
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/cars` | Get all cars (filterable) | No |
| GET | `/api/cars/<id>` | Get specific car details | No |

### 🛒 Shopping Cart
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/cart` | Get user's cart | Yes |
| POST | `/api/cart/add/<car_id>` | Add car to cart | Yes |
| DELETE | `/api/cart/remove/<car_id>` | Remove car from cart | Yes |

### 🩺 Health Check
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | API status check |

## Testing

### 1. API Health Check
Open in browser: `http://localhost:5000/api/health`

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "Car Dealership API is running"
}
```

### 2. Test Car Inventory
Open in browser: `http://localhost:5000/api/cars`

**Expected Response:** JSON array of car objects

### 3. Test Website Functionality
1. **Homepage**: `http://localhost:5000` - Should show featured cars
2. **Registration**: `http://localhost:5000/create-account.html` - Create a user account
3. **Car Inventory**: `http://localhost:5000/cars.html` - Browse and filter cars
4. **Shopping Cart**: Add cars to cart (requires login)

## Troubleshooting

### 🔴 Common Issues and Solutions

#### 1. "MySQL Connection Error"
**Problem**: Cannot connect to MySQL database
**Solution**:
- Ensure XAMPP MySQL is running
- Check if port 3306 is available
- Verify database exists: `car_dealership`

#### 2. "Module Not Found"
**Problem**: Python modules not found
**Solution**:
```bash
# Reactivate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall requirements
pip install -r requirements.txt
```

#### 3. "Port 5000 Already in Use"
**Solution**:
```bash
# Change port in backend/app.py
app.run(debug=True, port=5001)

# Or kill existing process
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
# macOS/Linux:
lsof -ti:5000 | xargs kill -9
```

#### 4. "CORS Errors"
**Problem**: Cross-Origin Request Blocked
**Solution**:
- Ensure accessing via `http://localhost:5000`
- Flask CORS is already configured

#### 5. "Tables Not Created"
**Solution**: Manual table creation in phpMyAdmin:
```sql
CREATE TABLE users (
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
);

CREATE TABLE cars (
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
);

CREATE TABLE cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    car_id INT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (car_id) REFERENCES cars(id),
    UNIQUE KEY unique_user_car (user_id, car_id)
);
```

### 🟡 Debugging Steps

1. **Check Flask Console** for Python errors
2. **Browser Developer Tools** (F12) for JavaScript errors
3. **Network Tab** in Developer Tools for API calls
4. **Verify XAMPP** services are running
5. **Check Database** in phpMyAdmin

## Support

If you encounter issues:

1. **Check the troubleshooting section above**
2. **Verify all prerequisites are installed**
3. **Ensure all services are running** (XAMPP, Flask)
4. **Check console outputs** for error messages

### Quick Start Checklist
- [ ] XAMPP installed and running
- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Database created in phpMyAdmin
- [ ] Flask server running on port 5000
- [ ] Website accessible at `http://localhost:5000`

---

**Happy Coding!** 🚗💨

If everything is set up correctly, you should have a fully functional car dealership website running locally with user registration, car inventory, and shopping cart functionality.