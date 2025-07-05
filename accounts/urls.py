from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view() , name='profile'),
    path('manager', ManagerView.as_view(), name='manager'),
    path('manager/create_product', ProductCreateView.as_view(), name='createProduct'),
    path('manager/delete_product/<int:pk>', ProductDeleteView.as_view(), name='deleteProduct'),
    path('manager/update_product/<int:pk>', ProductUpdateView.as_view(), name='updateProduct'),
    path('manager/create_category', CategoryCreateView.as_view(), name='createCategory'),
    path('manager/delete_category/<int:pk>', CategoryDeleteView.as_view(), name='deleteCategory'),
    path('manager/update_category/<int:pk>', CategoryUpdateView.as_view(), name='updateCategory'),
    path('manager/delete_order/<int:pk>', OrderDeleteView.as_view(), name='deleteOrder'),
    path('manager/update_order/<int:pk>', OrderUpdateView.as_view(), name='updateOrder'),

]