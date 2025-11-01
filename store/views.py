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


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# MERCHANT_KEY = 'kbzk98n@654!'

# # --- 🎯 CRITICAL FIX: Ensure the key is exactly 16 bytes long ---
# # This line trims the 20-byte key to a 16-byte key: 'KFZMLV7397327500'
# MERCHANT_KEY = (MERCHANT_KEY + '0'*32)[:16]
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

        # Convert amount safely
        try:
            amount = float(amount)
        except ValueError:
            amount = 0

        # Save order
        order = Orders(
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
        order.save()

        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()

        # Create Razorpay order (amount in paise)
        razorpay_order = razorpay_client.order.create({
            "amount": int(amount * 100),  # Razorpay expects paise
            "currency": "INR",
            "payment_capture": "1",  # Auto-capture after payment
            "notes": {
                "order_id": str(order.order_id),
                "name": name,
                "email": email
            }
        })

        # Store Razorpay order ID in DB for verification
        order.razorpay_order_id = razorpay_order['id']
        order.save()
        
        # Amount in paise for Razorpay
        razorpay_amount = int(amount * 100)

# Pass amount in rupees for display
        context = {
            "order": order,
            "razorpay_order_id": razorpay_order['id'],
            "razorpay_merchant_key": settings.RAZORPAY_KEY_ID,
            "amount": razorpay_amount,           # for Razorpay
            "display_amount": amount,            # for showing to user in ₹
            "currency": "INR",
            "callback_url": "https://hypertense-kookily-grayce.ngrok-free.dev/store/paymenthandler/",
        }

        # Pass info to frontend
        # context = {
        #     "order": order,
        #     "razorpay_order_id": razorpay_order['id'],
        #     "razorpay_merchant_key": settings.RAZORPAY_KEY_ID,
        #     "amount": int(amount * 100),
        #     "currency": "INR",
        #     "callback_url": "https://hypertense-kookily-grayce.ngrok-free.dev/store/paymenthandler/",
        # }

        return render(request, 'store/payment.html', context)

    return render(request, 'store/checkout.html')


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
                # ✅ Signature verified successfully

                # Update your order status in DB
                order = Orders.objects.get(razorpay_order_id=razorpay_order_id)
                order.payment_id = payment_id
                order.payment_status = "Success"
                order.save()

                # Add an order update entry
                OrderUpdate.objects.create(order_id=order.order_id, update_desc="Payment Successful")

                return render(request, 'store/paymentsuccess.html', {"payment_id": payment_id,"order_id": order.order_id})

            except razorpay.errors.SignatureVerificationError:
                # ❌ Signature mismatch
                return render(request, 'store/paymentfailed.html')

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")

    return HttpResponse("Invalid request method", status=400)
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


