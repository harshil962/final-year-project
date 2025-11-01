from django.db import models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='store/images', default="")

    def __str__(self):
        return self.product_name
    

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=10, default="")
    desc = models.CharField(max_length=5000, default="")

    def __str__(self):
        return self.name
    
# class Orders(models.Model):
#     order_id =models.AutoField(primary_key=True)
#     amount=models.IntegerField(default=0)
#     items_json= models.CharField(max_length=5000)
#     name=models.CharField(max_length=90)
#     email=models.CharField(max_length=90)
#     address=models.CharField(max_length=90)
#     city=models.CharField(max_length=90)
#     state=models.CharField(max_length=90)
#     zip_code=models.CharField(max_length=90)
#     phone = models.CharField(max_length=15, default='0000000000')

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    amount = models.IntegerField(default=0)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    address = models.CharField(max_length=90)
    city = models.CharField(max_length=90)
    state = models.CharField(max_length=90)
    zip_code = models.CharField(max_length=90)
    phone = models.CharField(max_length=15, default='0000000000')
    
    # --- Razorpay fields ---
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"Order {self.order_id} - {self.name}"


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc= models.CharField(max_length=5000)
    timestamp=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."




