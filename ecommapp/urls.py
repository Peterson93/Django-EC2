from ecommapp import views
from django.urls import path


urlpatterns = [
    path('', views.getRoutes, name="getRoutes"),
    path('products/', views.getProductos, name="getproductos"),
    path('product/<str:pk>', views.getProducto, name="getproducto"),
    path('users/login/', views.MyTokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path('users/profile/', views.getUserProfiles, name="getUserProfiles"),
    path('users/', views.getUsers, name="getUsers"),
    path('users/register/', views.registerUser, name="register"),
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name="activate"),
]
