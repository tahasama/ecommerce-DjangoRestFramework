# from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path, include
from rest_framework import routers

from .views import (GetUserById, ProductList, ProductRetrieve, UpdateUser, UpdateUserProfile, MyTokenObtainPairView,
                    UserProfile, UserList, createProduct, createProductReview, deleteProduct, deleteUser, getMyOrders, getOrderById, getOrders, getTopProducts, registerUser, AddOrderItems, updateOrderToDelivered, updateOrderToPaid, updateProduct, uploadImage)


urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', GetUserById.as_view()),
    path('users/update/<str:pk>/', UpdateUser.as_view(), name='user-update'),
    path('users/profile/', UserProfile.as_view(),),
    path('users/profile/update/', UpdateUserProfile.as_view(), name='user-update'),
    path('users/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/register/', registerUser.as_view()),
    path('users/delete/<str:pk>/', deleteUser.as_view(), name='user-delete'),
    path('products/', ProductList.as_view()),
    path('products/<int:pk>/', ProductRetrieve.as_view()),
    path('orders/', getOrders.as_view(), name='orders'),
    path('orders/add/', AddOrderItems.as_view(), name='orders-add'),
    path('orders/myorders/', getMyOrders.as_view(), name='myorders'),
    path('orders/<str:pk>/', getOrderById.as_view(), name='user-order'),
    path('orders/<str:pk>/pay/', updateOrderToPaid.as_view(), name='user-order'),
    path('orders/<str:pk>/deliver/', updateOrderToDelivered.as_view(),
         name='order-delivered'),
    path('products/create/', createProduct.as_view(), name="product-create"),
    path('products/upload/', uploadImage.as_view(), name="image-upload"),
    path('products/update/<str:pk>/',
         updateProduct.as_view(), name="product-update"),
    path('products/delete/<str:pk>/',
         deleteProduct.as_view(), name="product-delete"),
    path('products/<str:pk>/reviews/',
         createProductReview.as_view(), name="create-review"),
    path('products/top/', getTopProducts.as_view(), name='top-products'),


]
