from django.urls import path
from . import views

urlpatterns = [
    # Super Admin Login API View
    path("login/",views.SuperAdminLoginView.as_view()),
    # Categories
    path("add-category/",views.AddCategory.as_view()),
    path("all-category/",views.AllCategory.as_view()),
    path("category-details/<int:category_id>/",views.CategoryDetails.as_view()),
    path("edit-category/<int:category_id>/",views.EditCategory.as_view()),
    path("delete-category/<int:category_id>/",views.DeleteCategory.as_view()),
    # Sub Caategories
    path("add-sub-category/",views.SubCategory.as_view()),
    path("particular-category-sub-category-list/<int:cat_id>/",views.ParticularCategoriesSubCategoriesList.as_view()),
    path("particular-category-sub-category-table/<int:cat_id>/",views.ParticularCategoriesSubCategoriesTable.as_view()),
    path("all-sub-categories/",views.AllSubCategories.as_view()),
    path("edit-sub-category/<int:sub_cat_id>/",views.EditSubCategory.as_view()),
    path("delete-sub-category/<int:sub_cat_id>/",views.DeleteSubCategory.as_view()),
    # Products
    path("add-product/",views.AddProduct.as_view()),
    path("add-product-images-colors/",views.AddProductImagesColors.as_view()),
    path("particular-products-images-colors/<int:product_id>/",views.ParticularProductColorsAndImages.as_view()),
    path("all-products/",views.AllProducts.as_view()),
    path("particular-category-products/<int:cat_id>/",views.ParticularCategoryProducts.as_view()),
    path("product-details/<int:product_id>/",views.ProductDetails),
    path("edit-product/<int:product_id>/",views.EditProduct.as_view()),
    path("delete-product-images-colors/<int:prod_img_id>/",views.DeleteParticularProductImage.as_view()),
    path("delete-product/<int:product_id>/",views.DeleteProduct.as_view()),
    # General APIs
    path('states/', views.StatesList.as_view()),
    path('create-states/', views.CreateStates.as_view()),
    path('districts/<int:state_id>/', views.DistrictsList.as_view()),
    path('all-districts/', views.AllDistrictsDetailedView.as_view()),
    path('create-districts/', views.CreateDistrictsList.as_view()),
    path('mandals/<int:district_id>/', views.MandalsList.as_view()),
    path('create-mandals/', views.CreateMandals.as_view()),
    path('all-mandals/', views.AllMandalsDetailedView.as_view()),
    # Stories
    path('add-story/', views.AddHighlightStories.as_view()),
    path('delete-story/<int:story_id>/', views.DeleteHighlightStories.as_view()),
    path('all-stories/', views.AllHighlightStories.as_view()),
    path('edit-story/<int:story_id>/',views.EditStory.as_view()),
    path('particular-story/<int:story_id>/',views.ParticularHighlightStory.as_view()),
    # Banners
    path('add-banner/',views.AddBanner.as_view()),
    path('all-banner/',views.AllBanner.as_view()),
    path('delete-banner/<int:banner_id>/', views.DeleteBanner.as_view()),
    path('edit-banner/<int:banner_id>/', views.EditBanner.as_view()),
    path('particular-banner/<int:banner_id>/',views.ParticularBannerDetails.as_view()),
    # Chats
    path('all-users-in-chats/',views.AllUsersInChats.as_view()),
    path('particular-users-chat/<str:user_id>/',views.ParticularUsersChats.as_view()),
    path('reply-to-chat/',views.ChatWithUsReply.as_view()),
    path('particular-chat-all-replies/<int:chat_id>/',views.ParticularChatAllReplies.as_view()),
    # Users
    path('particular-user-details/<str:user_id>/',views.ParticularUserDetails.as_view()),
    # Coupons
    path("add-coupons/",views.AddCoupon.as_view()),
    path("get-coupons/",views.GetCoupons.as_view()),
    path("get-coupon-details/<int:coupon_id>/",views.ParticularCouponDetails),
    path("edit-coupon-details/<int:coupon_id>/",views.EditCouponDetails.as_view()),
    path("delete-coupon/<int:coupon_id>/",views.DeleteCoupon.as_view()),
    # Analytics
    path("more-in-wishlist/",views.MoreInWishlist.as_view()),
    # All Orders
    path("all-orders/",views.AllOrders.as_view()),
    path("particular-order-details/<int:order_id>/",views.ParticularOrderDetails),
    path("manage-order/<int:order_id>/",views.ManageOrder.as_view()),
    # Hurry up products
    path("products-lessthan-10-quantity/",views.HurryUpProducts.as_view()),
]


