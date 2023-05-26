from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from . import admin_serializers
from rest_framework import generics
from maintribe import models
from .paginators import CustomPagination
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

#############################################################   States General API   #####################################################################
# All States List API View
class CreateStates(generics.ListCreateAPIView):
    serializer_class = admin_serializers.CreateStateSerializer
    queryset = models.States.objects.all()

class StatesList(generics.ListCreateAPIView):
    queryset = models.States.objects.all()
    serializer_class = admin_serializers.StateSerializer

#############################################################   Districts General API   #####################################################################
# All Districts List API View
class CreateDistrictsList(generics.ListCreateAPIView):
    serializer_class = admin_serializers.CreateDistrictSerializer
    queryset = models.Districts.objects.all()

class DistrictsList(generics.ListCreateAPIView):
    serializer_class = admin_serializers.DistrictSerializer
    def get_queryset(self):
        state_id = self.kwargs['state_id']
        state = models.States.objects.get(pk=state_id)
        return (models.Districts.objects.filter(state=state))

class AllDistrictsDetailedView(generics.ListAPIView):
    serializer_class = admin_serializers.AllDistrictsDetailedSerializer
    queryset = models.Districts.objects.all()

#############################################################   Mandals General API   #####################################################################
# All Mandals List API View
class CreateMandals(generics.ListCreateAPIView):
    serializer_class = admin_serializers.CreateMandalSerializer
    queryset = models.Mandal.objects.all()

class AllMandalsDetailedView(generics.ListAPIView):
    serializer_class = admin_serializers.AllMandalsDetailSerializer
    queryset = models.Mandal.objects.all()

class MandalsList(generics.ListCreateAPIView):
    serializer_class = admin_serializers.MAndalSerializer
    def get_queryset(self):
        district_id = self.kwargs['district_id']
        district = models.Districts.objects.get(pk=district_id)
        return (models.Mandal.objects.filter(district=district))


#############################################################   Super Admin   #####################################################################
# Super Admin Login View
class SuperAdminLoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        superadmin = models.SuperAdminAcc.objects.filter(username=username, password=password)
        serializer = admin_serializers.SuperAdminAccSerializer(superadmin, many=True)
        if superadmin:
            admin_acc = models.SuperAdminAcc.objects.get(username=username)
            access_token = AccessToken.for_user(admin_acc)
            return Response({
                "status": 200,
                "bool": True,
                "data": serializer.data,
                'token': str(access_token),
            })
        else:
            return Response({
                "bool": False,
                "message": "Invalid Credentials !!!"
            })

#############################################################   Highlight Stories   #####################################################################
# Add New Story
class AddHighlightStories(APIView):
    def post(self,request):
        story_serializer = admin_serializers.HighlightStoriesSerializer(data=request.data)
        if not story_serializer.is_valid():
            return Response({
                'status':400,
                'errors':story_serializer.errors,
                'message':'some error occurred'
            })
        else:
            story_serializer.save()
            return Response({
                'status': 200,
                'data': story_serializer.data,
                'message': 'Story Highlight Added Succesfully'
            })

# Delete Story
class DeleteHighlightStories(APIView):
    def delete(self,request,story_id):
        if not models.HighlightStories.objects.filter(id=story_id):
            return Response({
                "status":400,
                "bool": False,
                "message": "No Story Found With This ID"
            })
        else:
            story = models.HighlightStories.objects.get(pk=story_id)
            story.delete()
            return Response({
                "status": 200,
                "bool": True,
                "message": "Story Deleted Succesfully"
            })

# Particular Story Details
class ParticularHighlightStory(APIView):
    def get(self,request,story_id):
        stories = models.HighlightStories.objects.filter(id=story_id)
        stories_serializer = admin_serializers.HighlightStoriesSerializer(stories,many=True)
        return Response({
            'status': 200,
            'data': stories_serializer.data,
            'message': 'Particular Story Highlight Fetched Succesfully'
        })

# Fetch All Stories
class AllHighlightStories(APIView):
    def get(self, request):
        stories = models.HighlightStories.objects.all()
        stories_serializer = admin_serializers.HighlightStoriesSerializer(stories,many=True)
        return Response({
            "status": 200,
            "data": stories_serializer.data,
            "message": "All Stories Fetched"
        })

# Edit Story
class EditStory(APIView):
    def put(self, request, story_id):
        try:
            obj = models.HighlightStories.objects.get(pk=story_id)
        except models.HighlightStories.DoesNotExist:
            return Response({'error': 'Object does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = admin_serializers.HighlightStoriesSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "data": serializer.data,
                "message": "Story Updated Succesfully"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#############################################################   Banners   #####################################################################
# Create New Banner
class AddBanner(APIView):
    def post(self,request):
        serializer = admin_serializers.BannerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status':200,
                'data':serializer.data,
                'message':'Banners created'
            })
        else:
            return Response({
                'status':400,
                'data':serializer.errors,
                'message':'something went wrong'
            })

# All Banners List
class AllBanner(APIView):
    def get(self,request):
        banners_obj=models.Banners.objects.all()
        serializer=admin_serializers.BannerSerializer(banners_obj,many=True)
        return Response({
            'status':200,
            'data':serializer.data,
            'message':'Banners list fetched'
        })

# Delete Banner
class DeleteBanner(APIView):
    def delete(self,request,banner_id):
        if not models.Banners.objects.filter(id=banner_id):
            return Response({
                "status":400,
                "bool": False,
                "message": "No Banner Found With This ID"
            })
        else:
            banner = models.Banners.objects.get(pk=banner_id)
            banner.delete()
            return Response({
                "status": 200,
                "bool": True,
                "message": "Banner Deleted Succesfully"
            })

# Edit Banner
class EditBanner(APIView):
    def put(self, request, banner_id):
        try:
            obj = models.Banners.objects.get(pk=banner_id)
        except models.Banners.DoesNotExist:
            return Response({'error': 'Object does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = admin_serializers.BannerSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "data": serializer.data,
                "message": "Banner Updated Succesfully"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Particular Banner Details Used To Edit The Banner In Admin Dashboard
class ParticularBannerDetails(APIView):
    def get(self,request,banner_id):
        banner = models.Banners.objects.filter(id=banner_id)
        banner_serializer = admin_serializers.BannerSerializer(banner,many=True)
        return Response({
            'status':400,
            'data':banner_serializer.data,
            'message':'Banner Details Fetched'
        })

#############################################################   Categories   #####################################################################
# Create Category
class AddCategory(APIView):
    def post(self, request):
        serializer = admin_serializers.CategorySerializer(data=request.data)
        if models.Categories.objects.filter(category=request.data['category']):
            return Response({
            'status': 200,
            'bool':False,
            'message': 'Category With This Name Already Exists'
        })
        else:
            if not serializer.is_valid():
                return Response({
                    'status': 403,
                    'errors': serializer.errors,
                    'message': 'some error occurred'
                })
            else:
                serializer.save()
                return Response({
                    'status': 200,
                    'data': serializer.data,
                    'message': 'success'
                })

# All Categories
class AllCategory(APIView):
    def get(self, request):
        category = models.Categories.objects.all()
        category_serializer = admin_serializers.CategorySerializer(category, many=True)
        return Response({
            'status': 200,
            'data': category_serializer.data,
            'message': 'All Categories Fetched'
        })

# Custom Pagination Class
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })

# All Categories List Along With Pagination
class AllCategoryWithPagination(ListAPIView):
    queryset = models.Categories.objects.all()
    serializer_class = admin_serializers.CategorySerializer
    pagination_class = CustomPageNumberPagination

# Particular Category Details
class CategoryDetails(APIView):
    def get(self, request, category_id):
        categories = models.Categories.objects.filter(id=category_id)
        serializer = admin_serializers.CategorySerializer(
            categories, many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'success'
        })

# Edit Category
class EditCategory(APIView):
    def put(self, request, category_id):
        try:
            obj = models.Categories.objects.get(pk=category_id)
        except models.Categories.DoesNotExist:
            return Response({'error': 'Object does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = admin_serializers.CategorySerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "data": serializer.data,
                "message": "Category Updated Succesfully"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete Particular Category
class DeleteCategory(APIView):
    def delete(self, request, category_id):
        category_exist = models.Categories.objects.filter(id=category_id)
        if category_exist:
            categories = models.Categories.objects.get(pk=category_id)
            categories.delete()
            return Response({
                'status': 200,
                'bool': True,
                'message': 'Category Deleted Succesfully'
            })
        else:
            return Response({
                'status': 200,
                'bool': False,
                'message': 'No category exist'
            })

#############################################################   Sub Categories   #####################################################################
# Add New Sub categopry
class SubCategory(APIView):
    def post(self, request):
        if models.SubCategories.objects.filter(sub_category=request.data['sub_category']):
            return Response({
            'status': 200,
            'bool':False,
            'message': 'Sub Category With This Name Already Exists'
        })
        else:
            serializer = admin_serializers.SubCategorySerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'status': 403,
                    'errors': serializer.errors,
                    'message': 'some error occurred'
                })
            else:
                serializer.save()
                return Response({
                    'status': 200,
                    'data': serializer.data,
                    'message': 'success'
                })
                
# Fetch All Sub Categories for particular category
class ParticularCategoriesSubCategoriesList(APIView):
    def get(self, request, cat_id):
        sub_categories = models.SubCategories.objects.filter(category=cat_id)
        serializer = admin_serializers.SubCategorySerializer(
            sub_categories, many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'success'
        })

# Fetch all Categories
class AllSubCategories(APIView):
    def get(self,request):
        sub_categories = models.SubCategories.objects.all()
        serializer = admin_serializers.SubCategoryTableSerializer(
            sub_categories, many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'success'
        })

# Fetch all Sub Categories For Table View
class ParticularCategoriesSubCategoriesTable(APIView):
    def get(self, request, cat_id):
        sub_categories = models.SubCategories.objects.filter(category=cat_id)
        serializer = admin_serializers.SubCategoryTableSerializer(
            sub_categories, many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'success'
        })

# Edit Sub Category
class EditSubCategory(APIView):
    def put(self, request, sub_cat_id):
        try:
            obj = models.SubCategories.objects.get(pk=sub_cat_id)
        except models.SubCategories.DoesNotExist:
            return Response({'error': 'Object does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = admin_serializers.SubCategorySerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "data": serializer.data,
                "message": "Category Updated Succesfully"
            },status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Sub Category
class DeleteSubCategory(APIView):
    def delete(self, request, sub_cat_id):
        if models.SubCategories.objects.filter(id=sub_cat_id):
            sub_categories = models.SubCategories.objects.get(pk=sub_cat_id)
            sub_categories.delete()
            return Response({
                'status': 200,
                'bool': True,
                'message': 'success'
            })
        else:
            return Response({
                'status': 400,
                'bool': False,
                'message': 'success'
            })

#############################################################   Products   #####################################################################
# Add Product Along With Images Prototype-1
# class AddProduct(APIView):
#     def post(self, request):
#         product_serializer = admin_serializers.PrpductSerializer(data=request.data)
#         if not product_serializer.is_valid():
#             return Response({
#                 'status': 400,
#                 'errors': product_serializer.errors,
#                 'message': 'some error occurred'
#             })
#         else:
#             product_serializer.save()
#             images = request.data.getlist('img')
#             serialized_product_id = product_serializer.data['id']
#             for i in images:
#                 img_serializer = admin_serializers.ProductImagesSerializer(data={'product': serialized_product_id, 'image': i})
#                 if img_serializer.is_valid():
#                     img_serializer.save()
#                 else:
#                     return Response({
#                         'status': 300,
#                         'data': img_serializer.errors,
#                         'message': 'Product Added Successfully but not images'
#                     })

#             colors = request.data.getlist('color')
#             for c in colors:
#                 color_serializer = admin_serializers.ProductColorsSerializer(data={'product':serialized_product_id,'color_code':c})
#                 if color_serializer.is_valid():
#                     color_serializer.save()
#                 else:
#                     return Response({
#                         'status': 300,
#                         'data': color_serializer.errors,
#                         'message': 'Product Added Successfully but not colors'
#                     })
#             return Response({
#                 'status': 200,
#                 'data': product_serializer.data,
#                 'message': 'Product Added Successfully'
#             })

# Create API For Adding New Product Protype - 2
class AddProduct(APIView):
    def post(self, request):
        product_serializer = admin_serializers.PrpductSerializer(data=request.data)
        if not product_serializer.is_valid():
            return Response({
                'status': 400,
                'errors': product_serializer.errors,
                'message': 'some error occurred'
            })
        else:
            product_serializer.save()
            return Response({
                'status': 200,
                'data': product_serializer.data,
                'message': 'Product Added Successfully',
                'product_id':product_serializer.data['id']
            })

# Adding Color and corresponding image to particular product
class AddProductImagesColors(APIView):
    def post(self,request):
        product_img_color_serializer = admin_serializers.ProductImageColorSerializer(data=request.data)
        if not product_img_color_serializer.is_valid():
            return Response({
                'status': 400,
                'errors': product_img_color_serializer.errors,
                'message': 'some error occurred'
            })
        else:
            product_img_color_serializer.save()
            return Response({
                'status': 200,
                'data': product_img_color_serializer.data,
                'message': 'Color And Corresponding Image Uploaded Successfully'
            })

# Particular Product All Colors And Images
class ParticularProductColorsAndImages(APIView):
    def get(self,request,product_id):
        product_imgs_colors = models.ProductColorImages.objects.filter(product=product_id)
        product_imgs_colors_serializer = admin_serializers.ProductImageColorSerializer(product_imgs_colors,many=True)
        return Response({
            'status':200,
            'data':product_imgs_colors_serializer.data,
            'message':'Particular Products All Images and Corresponding Colors Fetched'
        })

# Delete Particular Product Color And Image
class DeleteParticularProductImage(APIView):
    def delete(self,request,prod_img_id):
        if models.ProductColorImages.objects.filter(id=prod_img_id):
            prod_img = models.ProductColorImages.objects.get(pk=prod_img_id)
            prod_img.delete()
            return Response({
                'status': 200,
                'bool': True,
                'message': 'success'
            })
        else:
            return Response({
                'status': 400,
                'bool': False,
                'message': 'Not Found'
            })


# All Products
class AllProducts(APIView):
    def get(self, request):
        products = models.Product.objects.all()
        products_serializer = admin_serializers.ProductComplteDetailsSerializer(
            products, many=True)
        return Response({
            'status': 200,
            'data': products_serializer.data,
            'message': 'All Products Fetched'
        })

# Particular Category Products
class ParticularCategoryProducts(APIView):
    def get(self, request, cat_id):
        products = models.Product.objects.filter(category=cat_id)
        products_serializer = admin_serializers.ProductComplteDetailsSerializer(products, many=True)
        return Response({
            'status': 200,
            'data': products_serializer.data,
            'message': 'All Products Fetched'
        })

# Particular Product Details
def ProductDetails(request,product_id):
    my_object = models.Product.objects.get(pk=product_id)
    serialized_data = admin_serializers.ProductComplteDetailsSerializer(my_object).data
    response = Response(serialized_data,content_type='application/json')
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = 'application/json'
    response.renderer_context = {
        'view': ProductDetails,
        'request': request,
    }
    return response

# Edit Product
class EditProduct(APIView):
    def put(self,request,product_id):
        try:
            obj = models.Product.objects.get(pk=product_id)
        except models.Product.DoesNotExist:
            return Response({'error':'Object does not exist'},status=status.HTTP_404_NOT_FOUND)
        serializer = admin_serializers.PrpductSerializer(obj,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "data": serializer.data,
                "message": "Product Updated Succesfully"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete Product API View
class DeleteProduct(APIView):
    def delete(self,request,product_id):
        if models.Product.objects.filter(id=product_id):
            get_product = models.Product.objects.get(pk=product_id)
            get_product.delete()
            return Response({
                'status':200,
                'message':'Product Deleted Succesfully'
            })
        else:
            return Response({
                'status':400,
                'message':'No Product Found With This ID'
            })


# Edit Sub Category
class EditSubCategory(APIView):
    def put(self, request, sub_cat_id):
        try:
            obj = models.SubCategories.objects.get(pk=sub_cat_id)
        except models.SubCategories.DoesNotExist:
            return Response({'error': 'Object does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = admin_serializers.SubCategorySerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "data": serializer.data,
                "message": "Category Updated Succesfully"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

############################################################   Chat With US     ######################################################################
# All Chats Received
class AllUsersInChats(APIView):
    def get(self,request):
        chats = models.ChatWithus.objects.all()
        chats_user_serializer = admin_serializers.ChatWithUsUserDataSerializer(chats,many=True)
        return Response({
            "status": 200,
            "data": chats_user_serializer.data,
            "message": "Users in Chat Fetched"
        })

# Particular Users All Chats
class ParticularUsersChats(APIView):
    def get(self,request,user_id):
        chats = models.ChatWithus.objects.filter(user = user_id)
        chats_user_serializer = admin_serializers.ChatWithUsUserDataSerializer(chats,many=True)
        return Response({
            "status": 200,
            "data": chats_user_serializer.data,
            "message": "Users Chat Fetched"
        })

# Reply To A Chat
class ChatWithUsReply(APIView):
    def post(self,request):
        reply_chat = admin_serializers.ChatWithUsReplySerializer(data=request.data)

        if not reply_chat.is_valid():
            return Response({
                'status': 400,
                'errors': reply_chat.errors,
                'message': 'some error occurred'
            })
        else:
            reply_chat.save()
            return Response({
                'status': 200,
                'data': reply_chat.data,
                'message': 'Chat Reply Sent Successfully'
            })

# # Particular Chat All Replies
class ParticularChatAllReplies(APIView):
    def get(self,request,chat_id):
        chat = models.ChatWithUsReply.objects.filter(userChat_id = chat_id)
        chatReply_serializer = admin_serializers.ChatWithUsReplySerializer(chat,many=True)
        return Response({
            'status':200,
            'data':chatReply_serializer.data,
            'message':'All Replies To Particular Chats Retrieved'
        })

# Particular User Details
class ParticularUserDetails(APIView):
    def get(self,request,user_id):
        user = models.Users.objects.filter(uid=user_id)
        user_serializer = admin_serializers.EndUserSerializer(user,many=True)
        return Response({
            "status": 200,
            "data": user_serializer.data,
            "message": "Users Details Fetched"
        })

#############################################################   Coupons   #####################################################################
# Add Coupons View With Token Authentication
class AddCoupon(APIView):
    # authentication_classes = [CustomAuthentication]
    def post(self,request):
        serializer = admin_serializers.CounponsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 403,
                'errors': serializer.errors,
                'message': 'some error occurred'
            })
        else:
            serializer.save()
            return Response({
                'status': 200,
                'data': serializer.data,
                'message': 'success'
            })


# Fetch All Coupons With Token
class GetCoupons(APIView):
    # authentication_classes = [CustomAuthentication]
    def get(self,request):
        coupons = models.Coupons.objects.all()
        serializer = admin_serializers.CounponsSerializer(coupons,many=True)
        return Response({
            'status': 200,
            'data': serializer.data,
            'message': 'success'
        })

# Get Particular Coupon
def ParticularCouponDetails(request,coupon_id):
    my_object = models.Coupons.objects.get(pk=coupon_id)
    serialized_data = admin_serializers.CounponsSerializer(my_object).data
    response = Response(serialized_data,content_type='application/json')
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = 'application/json'
    response.renderer_context = {
        'view': ProductDetails,
        'request': request,
    }
    return response

# Edit Coupon
class EditCouponDetails(APIView):
    # authentication_classes = [CustomAuthentication]
    def put(self, request, coupon_id):
        try:
            obj = models.Coupons.objects.get(pk=coupon_id)
        except models.Coupons.DoesNotExist:
            return Response({'error': 'Object does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = admin_serializers.CounponsSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "data": serializer.data,
                "message": "Coupon  Updated Succesfully"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Delete Coupon
class DeleteCoupon(APIView):
    # authentication_classes = [CustomAuthentication]
    def delete(self,request,coupon_id):
        coupon_details = models.Coupons.objects.filter(id=coupon_id)
        if coupon_details:
            coupon = models.Coupons.objects.get(pk=coupon_id)
            coupon.delete()
            return Response({
                'status': 200,
                'bool':True,
                'message': 'Coupon Deleted'
            })
        else:
            return Response({
                'status': 200,
                'bool':False,
                'message': 'No Coupon Found'
            })

# Analytics
class MoreInWishlist(APIView):
    def get(self,request):
        products = models.Product.objects.all().order_by('no_of_wishlists').reverse()
        product_serializer = admin_serializers.ProductComplteDetailsSerializer(products,many=True)
        return Response({
            'status':200,
            'data':product_serializer.data
        })


from userapp import user_serializer

# All Orders
class AllOrders(APIView):
    def get(self,request):
        orders = models.OrderModel.objects.all().reverse()
        orders_serializer = user_serializer.OrderDetailsWithOrderItems(orders,many=True)
        return Response({
            'status':200,
            'data':orders_serializer.data,
            'message':'all orders fetched'
        })

# Particular Order Details
def ParticularOrderDetails(request,order_id):
    my_object = models.OrderModel.objects.get(pk=order_id)
    serialized_data = user_serializer.OrderDetailsWithOrderItems(my_object).data
    response = Response(serialized_data,content_type='application/json')
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = 'application/json'
    response.renderer_context = {
        'view': ProductDetails,
        'request': request,
    }
    return response

# Manage Order Status
class ManageOrder(APIView):
    def put(self, request, order_id):
        try:
            obj = models.OrderModel.objects.get(pk=order_id)
        except models.OrderModel.DoesNotExist:
            return Response({'error': 'Object does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = user_serializer.OrdersSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "data": serializer.data,
                "message": "Order Status Updated Succesfully"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HurryUpProducts(APIView):
    def get(self,request):
        products = models.Product.objects.filter(available_quantity__lt = 10)
        product_serializer = admin_serializers.ProductComplteDetailsSerializer(products,many=True)
        return Response({
            'status':200,
            'data':product_serializer.data,
            'message':'all orders fetched'
        })



