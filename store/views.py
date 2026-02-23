from django.utils import timezone
from django.http import HttpResponse,JsonResponse
from .models import Product,Contact, Orders, OrderUpdate
from math import ceil
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Contact
import json
from django.views.decorators.csrf import csrf_exempt
from paytmchecksum import PaytmChecksum
from math import ceil
import razorpay
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm 


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# 🟢 Register new user
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

# 🟢 Login user
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {username}!")
            return redirect('ShopHome')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'store/login.html')

# 🟢 Logout user
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

def index(request):
    allProds=[]
    catprods= Product.objects.values('category','product_id')
    cats ={item['category']for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod, range(1,nSlides),nSlides])

    params={'allProds':allProds}  
    return render(request, 'store/index.html', params)

@login_required(login_url='login')  # ✅ Ensure only logged-in users can checkout
def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '0')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        try:
            amount = float(amount)
        except ValueError:
            amount = 0

        # ✅ Save order with user
        order = Orders.objects.create(
            user=request.user,
            items_json=items_json,
            name=name,
            email=email,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
            amount=amount
        )
        OrderUpdate.objects.create(order_id=order.order_id, update_desc="Order placed successfully")

        # ✅ Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount": int(amount * 100),  # Convert to paise
            "currency": "INR",
            "payment_capture": "1",
            "notes": {
                "order_id": str(order.order_id),
                "user": request.user.username,
                "email": email,
            },
        })

        order.razorpay_order_id = razorpay_order['id']
        order.save()

        context = {
            "order": order,
            "razorpay_order_id": razorpay_order['id'],
            "razorpay_merchant_key": settings.RAZORPAY_KEY_ID,
            "amount": int(amount * 100),
            "display_amount": amount,
            "currency": "INR",
            "callback_url": "https://hypertense-kookily-grayce.ngrok-free.dev/store/paymenthandler/",
        }

        return render(request, "store/payment.html", context)

    return render(request, "store/checkout.html", {
        "prefill": {
            "name": request.user.get_full_name() or request.user.username,
            "email": request.user.email,
        }
    })


@csrf_exempt
def paymenthandler(request):
    """Handle payment success/failure callback from Razorpay"""
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            # Verify the payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            try:
                razorpay_client.utility.verify_payment_signature(params_dict)

                # Update your order status in DB
                order = Orders.objects.get(razorpay_order_id=razorpay_order_id)
                order.payment_id = payment_id
                order.payment_status = "Success"
                order.save()

                # Add an order update entry
                OrderUpdate.objects.create(order_id=order.order_id, update_desc="Payment Successful")

                return render(request, 'store/paymentsuccess.html', {"payment_id": payment_id,"order_id": order.order_id})

            except razorpay.errors.SignatureVerificationError:
                return render(request, 'store/paymentfailed.html')

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")

    return HttpResponse("Invalid request method", status=400)

def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if order.exists():
                order_obj = order.first()
                update_qs = OrderUpdate.objects.filter(order_id=orderId).order_by('timestamp')
                
                updates = []
                for item in update_qs:
                    formatted_time = item.timestamp.strftime("%d %b %Y, %I:%M %p")
                    updates.append({
                        'text': item.update_desc,
                        'time': formatted_time
                    })

                # items_json stored in order
                items = json.loads(order_obj.items_json)  # convert string JSON to Python dict/list

                return JsonResponse({
                    'updates': updates,
                    'items': items
                })
            else:
                return JsonResponse({'error': 'No order found'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return render(request, 'store/tracker.html')


@login_required(login_url='login')
def my_orders(request):
    """Show all orders placed by the logged-in user"""
    orders = Orders.objects.filter(user=request.user).order_by('-order_id')

    for order in orders:
        try:
            order.parsed_items = json.loads(order.items_json)
        except json.JSONDecodeError:
            order.parsed_items = {}

        # Get latest order update (optional)
        last_update = OrderUpdate.objects.filter(order_id=order.order_id).order_by('-timestamp').first()
        order.latest_update = last_update.update_desc if last_update else "Order placed"

    return render(request, 'store/my_orders.html', {"orders": orders})


def searchMatch(query, item):
    query = query.lower()
    if (query in item.desc.lower() or 
        query in item.product_name.lower() or 
        query in item.category.lower()):
        return True
    return False


def search(request):
    query = request.GET.get('search')
    allProds=[]
    catprods= Product.objects.values('category','product_id')
    cats ={item['category']for item in catprods}
    for cat in cats:
        prodtemp= Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch( query , item)]
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        if len(prod) != 0:
            allProds.append([prod, range(1,nSlides),nSlides])

    params={'allProds':allProds, 'msg':''}
    if len(allProds) == 0 or len(query) < 3 :
        params= {'msg':'Oops! Try entering a more specific search query.'}
    return render(request, 'store/search.html', params)


def about(request):
    return render(request, 'store/about.html')

def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')

        # Save to DB
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True

    return render(request, 'store/contact.html', {'thank': thank})


def productView(request, id):   # `id` comes from URL
    product = get_object_or_404(Product, product_id=id)  # ✅ use product_id field
    return render(request, 'store/prodView.html', {"product": product})


def privacy_policy(request):
    return render(request, 'store/privacy_policy.html')

def terms_conditions(request):
    return render(request, 'store/terms_conditions.html')

def refund_policy(request):
    return render(request, 'store/refund_policy.html')

def shipping_policy(request):
    return render(request, 'store/shipping_policy.html')


