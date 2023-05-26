from django.db import models
import uuid
from django.db.models import Avg
from decimal import Decimal


# States API
class States(models.Model):
    state_name = models.CharField(max_length=500)
    state_representing_image = models.ImageField(
        upload_to='states/', null=True)
    def __str__(self):
        return str(self.id) + "." + self.state_name
    class Meta:
        verbose_name_plural = "1.States"


# Districts API
class Districts(models.Model):
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    district_name = models.CharField(max_length=500)
    def __str__(self):
        return str(self.id) + "." + self.district_name
    class Meta:
        verbose_name_plural = "2.districts"


# Mandal API
class Mandal(models.Model):
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    mandal_name = models.CharField(max_length=500)
    def __str__(self):
        return str(self.id)+"."+self.mandal_name
    class Meta:
        verbose_name_plural = "3.Mandal"


# UserBase Model
class UserBaseModel(models.Model):
    id = models.CharField(default ="", max_length=500)
    uid = models.UUIDField(primary_key=True, editable=False,default = uuid.uuid4())
    created_date = models.DateField(auto_now_add=True)
    created_time= models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)
    class Meta:
        abstract = True

#############################################################   Super Admin Models   #####################################################################
# Super Admin Account
class SuperAdminAcc(models.Model):
    username = models.CharField(max_length=500)
    password = models.CharField(max_length=500)
    def __str__(self):
        return self.username

# Categories
class Categories(models.Model):
    category = models.CharField(max_length=500)
    category_image = models.ImageField(upload_to="category_images/")
    def __str__(self):
        return self.category

# Sub Categories
class SubCategories(models.Model):
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=500)
    def __str__(self):
        return self.sub_category

# Products
class Product(models.Model):
    # Product Details
    product_title = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategories,on_delete=models.CASCADE,related_name="sub_cat_product")
    sku_code = models.CharField(max_length=500,unique=True)
    thumbnail = models.ImageField(upload_to='product_thumbnail/')
    # Product Sizes And Prices
    # Size -1
    size_lable_1 = models.CharField(max_length=500)
    size_height_1 = models.CharField(max_length=500)
    size_width_1 = models.CharField(max_length=500)
    size_actual_price_1 = models.FloatField()
    size_selling_price_1 = models.FloatField()
    discount_1 = models.FloatField(default=0.0)
    # Size-2
    size_lable_2 = models.CharField(max_length=500,default="")
    size_height_2 = models.CharField(max_length=500,default="")
    size_width_2 = models.CharField(max_length=500,default="")
    size_actual_price_2 = models.FloatField(null=True,default=0.0)
    size_selling_price_2 = models.FloatField(null=True,default=0.0)
    discount_2 = models.FloatField(default=0.0)
    # Size-3
    size_lable_3 = models.CharField(max_length=500,default="")
    size_height_3 = models.CharField(max_length=500,default="")
    size_width_3 = models.CharField(max_length=500,default="")
    size_actual_price_3 = models.FloatField(null=True,default=0.0)
    size_selling_price_3 = models.FloatField(null=True,default=0.0)
    discount_3 = models.FloatField(default=0.0)
    # Size-4
    size_lable_4 = models.CharField(max_length=500,default="")
    size_height_4 = models.CharField(max_length=500,default="")
    size_width_4 = models.CharField(max_length=500,default="")
    size_actual_price_4 = models.FloatField(null=True,default=0.0)
    size_selling_price_4 = models.FloatField(null=True,default=0.0)
    discount_4 = models.FloatField(default=0.0)
    # Size-5
    size_lable_5 = models.CharField(max_length=500,default="")
    size_height_5 = models.CharField(max_length=500,default="")
    size_width_5 = models.CharField(max_length=500,default="")
    size_actual_price_5 = models.FloatField(null=True,default=0.0)
    size_selling_price_5 = models.FloatField(null=True,default=0.0)
    discount_5 = models.FloatField(default=0.0)
    # Product Status
    stock_status = models.CharField(max_length=500,default="Available")
    available_quantity = models.IntegerField(default=1)
    no_of_wishlists = models.IntegerField(default=0)
    no_of_cart = models.IntegerField(default=0)
    no_of_returned = models.IntegerField(default=0)
    no_of_orders = models.IntegerField(default=0)
    # Product Posted Details
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)
    rating = models.FloatField(default=0)
    numReviews = models.IntegerField(default=0)

    def calculate_rating(self):
        ratings = Reviews.objects.filter(product=self)
        if ratings.count() > 0:
            rating_avg = ratings.aggregate(Avg('ratings'))['ratings__avg']
            self.rating = round(rating_avg, 2) if rating_avg else 0.0
            self.numReviews = ratings.count()
        else:
            self.rating = 0.0
            self.numReviews = 0
        self.save()

    @property
    def discount_1(self):
        if self.size_actual_price_1 and self.size_selling_price_1:
            discount = ((self.size_actual_price_1 - self.size_selling_price_1) / self.size_actual_price_1) * 100
            return round(float(discount), 2)
        return 0.0

    @property
    def discount_2(self):
        if self.size_actual_price_2 and self.size_selling_price_2:
            actual_price = Decimal(self.size_actual_price_2)
            selling_price = Decimal(self.size_selling_price_2)
            discount = ((actual_price - selling_price) / actual_price) * 100
            return round(float(discount), 1)
        return 0.0

    @property
    def discount_3(self):
        if self.size_actual_price_3 is not None and self.size_selling_price_3 is not None:
            actual_price = Decimal(self.size_actual_price_3)
            selling_price = Decimal(self.size_selling_price_3)
            discount = ((actual_price - selling_price) / actual_price) * 100
            return round(float(discount), 2)
        return 0.0

    @property
    def discount_4(self):
        if self.size_actual_price_4 is not None and self.size_selling_price_4 is not None:
            actual_price = Decimal(self.size_actual_price_4)
            selling_price = Decimal(self.size_selling_price_4)
            discount = ((actual_price - selling_price) / actual_price) * 100
            return round(float(discount), 2)
        return 0.0

    @property
    def discount_5(self):
        if self.size_actual_price_5 is not None and self.size_selling_price_5 is not None:
            actual_price = Decimal(self.size_actual_price_5)
            selling_price = Decimal(self.size_selling_price_5)
            discount = ((actual_price - selling_price) / actual_price) * 100
            return round(float(discount), 2)
        return 0.0

# Product Images and colors
class ProductColorImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_images')
    image = models.ImageField(upload_to="product_images/")
    color_name = models.CharField(max_length=500)
    color_code = models.CharField(max_length=500)

# Stories
class HighlightStories(models.Model):
    title = models.CharField(max_length=500)
    thumbnail = models.ImageField(upload_to='story_thumbnail/')
    img_video = models.FileField(max_length=500,upload_to='stories/')
    type = models.CharField(max_length=500,default="image")
    # Story Posted Details
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)

# Banners
class Banners(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    banner=models.ImageField(max_length=500,upload_to='banners/')
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategories,on_delete=models.CASCADE)







#############################################################   End User Models   #####################################################################
class UserBaseModel(models.Model):
    id = models.CharField(default ="", max_length=500)
    uid = models.UUIDField(primary_key=True, editable=False,default = uuid.uuid4())
    created_date = models.DateField(auto_now_add=True)
    created_time= models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)
    class Meta:
        abstract = True

# User Model
class Users(UserBaseModel):
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=500,default="")
    phone = models.CharField(max_length=100)
    otp = models.CharField(max_length=10,default="00000")
    profile = models.ImageField(upload_to='profile_pictures/',null=True)
    device_id = models.CharField(max_length=500)
    firebase_id = models.CharField(max_length=250,default="aaa")
    is_verified = models.BooleanField(default=False)

# Address 
class Address(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    state = models.CharField(max_length=500)
    full_name = models.CharField(max_length=500)
    mobile = models.CharField(max_length=500)
    hno = models.CharField(max_length=500)
    area_street = models.CharField(max_length=500)
    alternate_mobile = models.CharField(max_length=500)
    pincode = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    is_home = models.BooleanField(default=True)

# CART
class Cart(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.IntegerField(default=1)
    color = models.CharField(max_length=200)
    is_controller = models.BooleanField(default=False)

# Wishlist
class WishList(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    size = models.IntegerField(default=1)
    color = models.CharField(max_length=200)

# Chat With Us For EndUser
class ChatWithus(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    created_date = models.DateField(auto_now_add=True)
    created_time= models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)

# Replies By Admin To Chat With us
class ChatWithUsReply(models.Model):
    userChat_id = models.ForeignKey(ChatWithus,on_delete=models.CASCADE)
    reply_text = models.CharField(max_length=500)
    created_date = models.DateField(auto_now_add=True)
    created_time= models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)

# Coupons
class Coupons(models.Model):
    coupon_code = models.CharField(max_length=200)
    coupon_description = models.TextField()
    discount_percentage = models.IntegerField()
    min_price_for_coupon_avail = models.IntegerField()
    max_price = models.IntegerField()
    no_of_days_valid = models.CharField(max_length=200)
    no_of_coupons = models.IntegerField()
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)
    def __str__(self):
        return self.coupon_code

# Reviews
class Reviews(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    subject = models.CharField(max_length=500,blank=True)
    description = models.TextField(blank=True)
    ratings = models.IntegerField()
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)

# Order Model
class Order(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    is_coupon_applied = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupons, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.IntegerField()
    payment_method = models.CharField(max_length=200)
    payment_done = models.BooleanField(default=False)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order_status = models.CharField(default="order_placed",max_length=200)
    transaction_id = models.CharField(max_length=250,default='')
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    updated_time = models.TimeField(auto_now=True)

# Orders
class OrderModel(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    is_coupon_applied = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupons,on_delete=models.SET_NULL,null=True)
    total_amount = models.IntegerField()
    payment_method = models.CharField(max_length=200)
    payment_done = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    order_status = models.CharField(default="1",max_length=200)
    is_paid = models.BooleanField(default=False)
    is_order_placed = models.BooleanField(default=True)
    is_order_confirmed = models.BooleanField(default=False)
    is_order_shipped = models.BooleanField(default=False)
    is_order_on_the_way = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    order_placedAt = models.DateTimeField(auto_now=True)
    order_confirmedAt = models.CharField(default="",max_length=200)
    order_shippedAt = models.CharField(default="",max_length=200)
    order_on_the_wayAt = models.CharField(default="",max_length=200)
    order_deliveredAt = models.CharField(default="",max_length=200)
    updatedAt = models.DateTimeField(auto_now_add=True)

# Order Items
class OrderItems(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    order = models.ForeignKey(OrderModel,on_delete=models.CASCADE,related_name="order_items")
    size = models.IntegerField(default=1)
    color = models.CharField(max_length=200)







