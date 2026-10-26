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

These instructions are for Windows and PowerShell. First, install Python 3.10 or newer. Download or clone this project, then open a terminal in the project folder that contains `manage.py`.

### 1️⃣ Create and activate a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, allow scripts for this terminal session and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 2️⃣ Install the project dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3️⃣ Set up the database

```powershell
python manage.py migrate
```

To sign in to the Django admin, create an administrator account when prompted:

```powershell
python manage.py createsuperuser
```

### 4️⃣ Start the website

```powershell
python manage.py runserver
```

Keep this terminal open while using the site. In Google Chrome, visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/). To open the admin site, visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and sign in with the superuser account.

Press `Ctrl+C` in the terminal to stop the development server.



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
