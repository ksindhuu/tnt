from rest_framework import serializers
from maintribe import models

# States Serializer
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.States
        fields = ['id', 'state_representing_image', 'state_name']
        depth = 1

class CreateStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.States
        fields = ['id', 'state_representing_image', 'state_name']

# District Serializer
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Districts
        fields = '__all__'
        depth = 1

class CreateDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Districts
        fields = '__all__'

class AllDistrictsDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Districts
        fields = '__all__'
        depth=1

# Mandals Serializer
class MAndalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mandal
        fields = '__all__'
        depth = 1

class CreateMandalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mandal
        fields = '__all__'

class AllMandalsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mandal
        fields = '__all__'
        depth = 2

# Super Admin Serializer
class SuperAdminAccSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SuperAdminAcc
        fields = "__all__"


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Categories
        fields = "__all__"
    def create(self,validated_data):
        category = models.Categories.objects.create(category=validated_data['category'],category_image = validated_data['category_image'])
        category.save()
        return category

# Sub Category Serializer
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubCategories
        fields = "__all__"
    def create(self,validated_data):
        sub_category = models.SubCategories.objects.create(category=validated_data['category'],sub_category = validated_data['sub_category'])
        sub_category.save()
        return sub_category

# Sub Category Table Serializer
class SubCategoryTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubCategories
        fields = "__all__"
        depth = 1
    def create(self,validated_data):
        sub_category = models.SubCategories.objects.create(category=validated_data['category'],sub_category = validated_data['sub_category'])
        sub_category.save()
        return sub_category

# Product Serializer
class PrpductSerializer(serializers.ModelSerializer):
    size_width_5 = serializers.CharField(allow_blank=True)
    size_width_4 = serializers.CharField(allow_blank=True)
    size_width_3 = serializers.CharField(allow_blank=True)
    size_width_2 = serializers.CharField(allow_blank=True)
    size_width_1 = serializers.CharField(allow_blank=True)

    size_height_5 = serializers.CharField(allow_blank=True)
    size_height_4 = serializers.CharField(allow_blank=True)
    size_height_3 = serializers.CharField(allow_blank=True)
    size_height_2 = serializers.CharField(allow_blank=True)
    size_height_1 = serializers.CharField(allow_blank=True)

    size_lable_5 = serializers.CharField(allow_blank=True)
    size_lable_4 = serializers.CharField(allow_blank=True)
    size_lable_3 = serializers.CharField(allow_blank=True)
    size_lable_2 = serializers.CharField(allow_blank=True)
    size_lable_1 = serializers.CharField(allow_blank=True)

    class Meta:
        model = models.Product
        fields = "__all__"

    def create(self,validated_data):
        product = models.Product.objects.create(size_selling_price_5=validated_data['size_selling_price_5'],size_selling_price_4=validated_data['size_selling_price_4'],size_selling_price_3=validated_data['size_selling_price_3'],size_selling_price_2=validated_data['size_selling_price_2'],size_selling_price_1=validated_data['size_selling_price_1'],size_actual_price_5=validated_data['size_actual_price_5'],size_actual_price_4=validated_data['size_actual_price_4'],size_actual_price_3=validated_data['size_actual_price_3'],size_actual_price_2=validated_data['size_actual_price_2'],size_actual_price_1=validated_data['size_actual_price_1'],size_width_5=validated_data['size_width_5'],size_width_4=validated_data['size_width_4'],size_width_3=validated_data['size_width_3'],size_width_2=validated_data['size_width_2'],size_width_1=validated_data['size_width_1'],size_height_5=validated_data['size_height_5'],size_height_4=validated_data['size_height_4'],size_height_3=validated_data['size_height_3'],size_height_2=validated_data['size_height_2'],size_height_1=validated_data['size_height_1'],size_lable_5=validated_data['size_lable_5'],size_lable_4=validated_data['size_lable_4'],size_lable_3=validated_data['size_lable_3'],size_lable_2=validated_data['size_lable_2'],size_lable_1=validated_data['size_lable_1'],thumbnail=validated_data['thumbnail'],available_quantity=validated_data['available_quantity'],sku_code = validated_data['sku_code'],sub_category = validated_data['sub_category'],category = validated_data['category'],description=validated_data['description'],product_title = validated_data['product_title'])
        product.save()
        return product

class ProductImageColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductColorImages
        fields = "__all__"
    def create(self, validated_data):
        image_product = models.ProductColorImages.objects.create(product=validated_data['product'], image=validated_data['image'],color_name=validated_data['color_name'],color_code=validated_data['color_code'])
        image_product.save()
        return image_product

class ProductComplteDetailsSerializer(serializers.ModelSerializer):
    product_images = ProductImageColorSerializer(many=True,read_only = True)
    discount_1 = serializers.SerializerMethodField()
    discount_2 = serializers.SerializerMethodField()
    discount_3 = serializers.SerializerMethodField()
    discount_4 = serializers.SerializerMethodField()
    discount_5 = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = "__all__"
        depth = 1

    def get_discount_1(self, obj):
        if obj.size_actual_price_1 and obj.size_selling_price_1:
            discount = ((obj.size_actual_price_1 - obj.size_selling_price_1) / obj.size_actual_price_1) * 100
            return round(discount, 2)
        return 0

    def get_discount_2(self, obj):
        if obj.size_actual_price_2 and obj.size_selling_price_2:
            discount = ((obj.size_actual_price_2 - obj.size_selling_price_2) / obj.size_actual_price_2) * 100
            return round(discount, 2)
        return 0
    
    def get_discount_3(self, obj):
        if obj.size_actual_price_3 and obj.size_selling_price_3:
            discount = ((obj.size_actual_price_3 - obj.size_selling_price_3) / obj.size_actual_price_3) * 100
            return round(discount, 2)
        return 0
    
    def get_discount_4(self, obj):
        if obj.size_actual_price_4 and obj.size_selling_price_4:
            discount = ((obj.size_actual_price_4 - obj.size_selling_price_4) / obj.size_actual_price_4) * 100
            return round(discount, 2)
        return 0

    def get_discount_5(self, obj):
        if obj.size_actual_price_5 and obj.size_selling_price_5:
            discount = ((obj.size_actual_price_5 - obj.size_selling_price_5) / obj.size_actual_price_5) * 100
            return round(discount, 2)
        return 0

class HighlightStoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HighlightStories
        fields = "__all__"
    def create(self, validated_data):
        story = models.HighlightStories.objects.create(thumbnail=validated_data['thumbnail'],title=validated_data['title'],img_video=validated_data['img_video'],type=validated_data['type'])
        story.save()
        return story

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Banners
        fields='__all__'
    def create(self,validated_data):
        Banners=models.Banners.objects.create(sub_category=validated_data['sub_category'],category=validated_data['category'],banner=validated_data['banner'],title=validated_data['title'],description=validated_data['description'])
        Banners.save()
        return Banners

# Serializer for Fetching Chats in all Users
class ChatWithUsUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatWithus
        fields = "__all__"
        depth=1

# Chat With us Serializer for enduser
class ChatWithUsReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatWithUsReply
        fields = "__all__"
    def create(self,validated_data):
        chatWithUs = models.ChatWithUsReply.objects.create(reply_text=validated_data['reply_text'],userChat_id=validated_data['userChat_id'])
        chatWithUs.save()
        return chatWithUs                   

# Serializer For User Details To Access in Admin Dashboard
class EndUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Users
        fields = "__all__"

# Coupon Serializer
class CounponsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coupons
        fields = "__all__"
    def create(self, validated_data):
        coupon = models.Coupons.objects.create(coupon_code=validated_data['coupon_code'],coupon_description=validated_data['coupon_description'],discount_percentage=validated_data['discount_percentage'],min_price_for_coupon_avail=validated_data['min_price_for_coupon_avail'], max_price=validated_data['max_price'], no_of_days_valid=validated_data['no_of_days_valid'], no_of_coupons=validated_data['no_of_coupons'])
        coupon.save()
        return coupon













  





