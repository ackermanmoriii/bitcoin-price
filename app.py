import os
import logging
from flask import Flask, jsonify, request

# --- 1. تنظیمات اولیه لاگینگ ---
# لاگ‌ها به ما کمک می‌کنند تا بفهمیم برنامه ما چه می‌کند و در صورت بروز مشکل، کجا را بررسی کنیم.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- 2. ایجاد نمونه برنامه Flask ---
app = Flask(__name__)

# --- 3. تنظیمات برنامه (از متغیرهای محیطی) ---
# در برنامه‌های واقعی، این تنظیمات از فایل‌های پیکربندی یا متغیرهای محیطی خوانده می‌شوند.
# ما از os.getenv استفاده می‌کنیم تا بتوانیم آن‌ها را از بیرون تنظیم کنیم.
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your_super_secret_key_if_not_set_in_env')
app.config['ENV'] = os.getenv('FLASK_ENV', 'development') # development, production, testing
app.config['DEBUG'] = (app.config['ENV'] == 'development')

# --- 4. تعریف مسیرها (Routes) ---

@app.route('/')
def home():
    """
    مسیر ریشه: صفحه اصلی برنامه.
    یک پیام خوش‌آمدگویی به صورت JSON برمی‌گرداند.
    """
    logger.info("Accessing home route.")
    return jsonify({
        "message": "Welcome to our Flask application!",
        "environment": app.config['ENV'],
        "status": "online"
    })

@app.route('/greet/<name>')
def greet(name):
    """
    مسیر سلام کردن: به یک نام مشخص سلام می‌کند.
    مثال: /greet/Ali
    """
    logger.info(f"Greeting request for name: {name}")
    if not name.isalpha(): # یک اعتبارسنجی ساده: نام باید فقط حروف باشد
        logger.warning(f"Invalid name provided: {name}")
        return jsonify({"error": "Name must contain only letters."}), 400
    return jsonify({"message": f"Hello, {name}!"})

@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    """
    مسیر مدیریت داده:
    - GET: اطلاعات نمونه را برمی‌گرداند.
    - POST: داده‌های ارسال شده را دریافت و تایید می‌کند.
    """
    if request.method == 'GET':
        logger.info("GET request to /data.")
        return jsonify({
            "data_type": "sample",
            "items": ["item1", "item2", "item3"],
            "count": 3
        })
    elif request.method == 'POST':
        logger.info("POST request to /data.")
        # در یک برنامه واقعی، در اینجا درخواست.json یا درخواست.form را تجزیه و تحلیل می‌کنید.
        # فرض می‌کنیم داده‌ها در قالب JSON ارسال شده‌اند.
        received_data = request.json
        if received_data:
            logger.info(f"Received POST data: {received_data}")
            return jsonify({
                "message": "Data received successfully!",
                "your_data": received_data,
                "status": "processed"
            }), 201 # 201 Created
        else:
            logger.warning("POST request to /data received no JSON data.")
            return jsonify({"error": "No JSON data provided."}), 400

# --- 5. مدیریت خطاها (Error Handlers) ---
# این‌ها به ما کمک می‌کنند تا خطاهای رایج را به شکل دوستانه‌تری به کاربر نمایش دهیم.

@app.errorhandler(404)
def not_found_error(error):
    """
    مدیریت خطای 404 (صفحه پیدا نشد).
    """
    logger.error(f"404 Not Found: {request.url}")
    return jsonify({"error": "Resource not found", "path": request.path}), 404

@app.errorhandler(500)
def internal_error(error):
    """
    مدیریت خطای 500 (خطای داخلی سرور).
    در اینجا، خطا را به همراه traceback کامل لاگ می‌کنیم.
    """
    logger.exception("An unhandled internal server error occurred.") # Logs full traceback
    return jsonify({"error": "An internal server error occurred", "message": str(error)}), 500

# --- 6. بلاک اجرای برنامه ---
# این بلاک تضمین می‌کند که app.run() فقط زمانی اجرا می‌شود که فایل به طور مستقیم اجرا شود،
# نه زمانی که به عنوان ماژول وارد (import) می‌شود.
if __name__ == '__main__':
    logger.info(f"Starting Flask app in {app.config['ENV']} mode...")
    # 'host='0.0.0.0'' اجازه می‌دهد برنامه از خارج نیز قابل دسترسی باشد (مفید در داکر یا محیط‌های ابری).
    # 'port=5000' پورت پیش‌فرض را تعیین می‌کند.
    app.run(host='0.0.0.0', port=5000)
