# 🏥 MediCart – Online Medical Supply Store  

**MediCart** is a full-featured Django-based e-commerce platform for healthcare and medical products.  
It allows users to browse products, add them to a cart, place orders securely using Razorpay, and track their orders in real-time.


## 🚀 Features

### 🛒 Store & Products
- Browse medical products categorized by type.
- Dynamic product carousel with smooth UI animations (AOS).
- Add, remove, and update items in the shopping cart.
- View detailed product descriptions and pricing.

### 💳 Checkout & Payments
- Secure online payments integrated with **Razorpay**.
- Automatic order creation and payment verification.
- Real-time payment status updates stored in the database.

### 📦 Orders & Tracking
- Tracks every order with real-time status updates.
- Users can check their order progress by order ID and email.
- Updates displayed dynamically via JSON responses.

### 📞 Contact & Support
- Built-in contact form for customer queries.
- Automatic message saving in the database.

### ⚙️ Admin Management
- Fully manageable through Django Admin.
- CRUD operations for products, contacts, and orders.

---

## 🧠 Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend** | Django (Python) |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5 |
| **Database** | SQLite (default) / MySQL |
| **Payment Gateway** | Razorpay |
| **Other Tools** | AOS (Animate on Scroll), jQuery |

---

## 🏗️ Project Structure



final-year-project/
│
├── store/
│   ├── models.py          # Product, Contact, Orders, OrderUpdate models
│   ├── views.py           # Main business logic and Razorpay integration
│   ├── templates/store/   # HTML templates (index, checkout, payment, etc.)
│   ├── static/store/      # CSS, JS, images
│   ├── urls.py            # Route definitions
│   └── admin.py           # Admin registration
│
├── finalyearproject/
│   ├── settings.py        # Django configuration
│   ├── urls.py            # Root URLs
│   └── wsgi.py / asgi.py  # Deployment files
│
├── manage.py
└── README.md




## ⚙️ Installation & Setup

### 1️⃣ Clone the repository  

git clone https://github.com/harshil962/final-year-project.git
cd final-year-project




### 3️⃣ Install dependencies


pip install -r requirements.txt


### 4️⃣ Configure environment variables

Add your Razorpay credentials in `settings.py`  file:

python
RAZORPAY_KEY_ID = "your_razorpay_key"
RAZORPAY_KEY_SECRET = "your_razorpay_secret"


### 5️⃣ Apply migrations


python manage.py makemigrations
python manage.py migrate


### 6️⃣ Create superuser


python manage.py createsuperuser


### 7️⃣ Run the server

python manage.py runserver


Then open: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)



## 💵 Payment Flow (Razorpay Integration)

1. User adds items to cart and proceeds to checkout.
2. Razorpay order is created server-side with amount in paise.
3. Razorpay Checkout popup opens for secure payment.
4. On success/failure, `paymenthandler()` verifies the signature.
5. Order status updates in the database and shown to user.



## 🔐 Policies

* **Privacy Policy** – `/store/privacy_policy/`
* **Refund Policy** – `/store/refund_policy/`
* **Shipping Policy** – `/store/shipping_policy/`
* **Terms & Conditions** – `/store/terms_conditions/`
