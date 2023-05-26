from rest_framework import serializers
from maintribe import models
import uuid
import random
from rest_framework.serializers import ValidationError

class EmptyStringIfNullImageField(serializers.ImageField):
    def to_representation(self, value):
        if value is None:
            return ""
        return super().to_representation(value)
    

# End User Serializer
class UserSerializer(serializers.ModelSerializer):
    profile = serializers.ImageField(required=False, allow_null=True, default="")
    firebase_id = serializers.CharField(allow_blank=True)

    class Meta:
        model = models.Users
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'profile' not in data or data['profile'] is None:
            data['profile'] = ''
        return data

    def create(self, validated_data):
        otp_generated = random.randint(10000, 99999)
        phone = validated_data['phone']

        if models.Users.objects.filter(phone=phone).exists():
            user = models.Users.objects.get(phone=phone)
            user.otp = otp_generated
            user.save()
        else:
            user = models.Users.objects.create(
                firebase_id=validated_data['firebase_id'],
                otp=otp_generated,
                name=validated_data['name'],
                email=validated_data['email'],
                phone=validated_data['phone'],
                uid=uuid.uuid4(),
                device_id=validated_data['device_id']
            )
        return user

# Address Serializer
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = "__all__"
    def create(self,validated_data):
        address = models.Address.objects.create(user=validated_data['user'],full_name=validated_data['full_name'],mobile=validated_data['mobile'],hno=validated_data['hno'],area_street=validated_data['area_street'],alternate_mobile=validated_data['alternate_mobile'],pincode =validated_data['pincode'],city=validated_data['city'],state=validated_data['state'],is_home = validated_data['is_home'])
        address.save()
        return address

class AddressDetailedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.Address
        fields ="__all__"
        depth = 2


# CART Serializer
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = "__all__"
    def create(self, validated_data):
        product = models.Product.objects.get(pk=validated_data['product'].id)
        available_quantity = product.available_quantity
        if validated_data['quantity'] <= available_quantity:
            cart = models.Cart.objects.create(color=validated_data['color'],is_controller=validated_data['is_controller'],user=validated_data['user'],product=validated_data['product'],quantity=validated_data['quantity'],size=validated_data['size'])
            cart.save()
            return cart
        else:
            raise ValidationError('Seller Doent Have Enough Stock')
            

# CART Detailed Serializer With User and Product Objects
class CartDetailedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.Cart
        fields = "__all__"
        depth = 2

    def get_user(self, obj):
        user = obj.user
        profile = user.profile or ""  # Check if profile exists, otherwise set it to an empty string
        user_data = UserSerializer(user).data
        user_data['profile'] = profile
        return user_data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_data = representation.get('user')
        if user_data:
            user_data['profile'] = user_data['profile'] or ""  # Set profile field to empty string if it is None
        return representation

# Users Wishlist Serializer
class UserWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WishList
        fields="__all__"
    def create(self,validated_data):
        whishlist = models.WishList.objects.create(color=validated_data['color'],size=validated_data['size'],user=validated_data['user'],product=validated_data['product'])
        whishlist.save()
        return whishlist

# Users Wishlist With Product Images and Product Details
class UserWishListCompleteSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.WishList
        fields = "__all__"
        depth = 2

# Chat With us Serializer for enduser
class ChatWithUsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.ChatWithus
        fields = "__all__"
    def create(self,validated_data):
        chatWithUs = models.ChatWithus.objects.create(user=validated_data['user'],text=validated_data['text'])
        chatWithUs.save()
        return chatWithUs

# End User Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reviews
        fields = "__all__"
    def create(self, validated_data):
        review = models.Reviews.objects.create(user=validated_data['user'], product=validated_data['product'], subject=validated_data['subject'], description=validated_data['description'],ratings=validated_data['ratings'])
        review.save()
        return review

# End User Orders Serializer
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderModel
        fields = "__all__"
    def create(self, validated_data):
        orders = models.OrderModel.objects.create(**validated_data)
        return orders
    
# Serializer for Adding Products To The Order Model
class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.OrderItems
        fields='__all__'
    def create(self,validated_data):
        product = models.Product.objects.get(pk=validated_data['product'].id)
        if product.available_quantity < validated_data['quantity']:
            raise serializers.ValidationError("Not Enough Products")
        else:
            items=models.OrderItems.objects.create(size=validated_data['size'],color=validated_data['color'],quantity=validated_data['quantity'],product=validated_data['product'],order=validated_data['order'])
            product.no_of_orders = product.no_of_orders+1
            product.save()
            items.save()
            return items

# Serializer for handling the product Images
class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductColorImages
        fields = "__all__"
    def create(self, validated_data):
        image_product = models.ProductColorImages.objects.create(product = validated_data['product'],image =validated_data['image'])
        image_product.save()
        return image_product

# Complete Product Serializer
class ProductComplteDetailsSerializer(serializers.ModelSerializer):
    product_images = ProductImagesSerializer(many=True,read_only = True)
    class Meta:
        model = models.Product
        fields = "__all__"
        depth = 1

# All Products With Subcategory
class AllProductsAccordingToSubCategory(serializers.ModelSerializer):
    sub_cat_product = ProductComplteDetailsSerializer(many=True,read_only=True)
    class Meta:
        model = models.SubCategories
        fields = "__all__"
        depth=1

# Product Serializer
class PrpductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"
    def create(self,validated_data):
        product = models.Product.objects.create(width=validated_data['width'],height=validated_data['height'],weight=validated_data['weight'],color=validated_data['color'],font=validated_data['font'],available_quantity=validated_data['available_quantity'],selling_price=validated_data['selling_price'],actual_price=validated_data['actual_price'],sku_code = validated_data['sku_code'],sub_category = validated_data['sub_category'],category = validated_data['category'],description=validated_data['description'],product_title = validated_data['product_title'])
        product.save()
        return product


class OrderItemsDetailedSerializer(serializers.ModelSerializer):
    product = PrpductSerializer()
    class Meta:
        model = models.OrderItems
        fields = "__all__"
        # depth = 2

    

# Detailed Orders Serializer Along With Ordered Items, User, Address, Coupon Objects
class OrderDetailsWithOrderItems(serializers.ModelSerializer):
    order_items = OrderItemsDetailedSerializer(many=True,read_only = True)
    user = UserSerializer()
    address = AddressDetailedSerializer()

    class Meta:
        model = models.OrderModel
        fields = "__all__"
        depth = 2

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'coupon' in representation and representation['coupon'] is None:
            representation['coupon'] = ""
        return representation


# class OrderDetailsWithOrderItems(serializers.ModelSerializer):
#     order_items = OrderItemsDetailedSerializer(many=True,read_only = True)
#     user = UserSerializer()

#     class Meta:
#         model = models.OrderModel
#         fields = "__all__"
#         depth = 2

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         if 'coupon' in representation and representation['coupon'] is None:
#             representation['coupon'] = ""
#         return representation







