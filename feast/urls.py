# from django.urls import path
# from .views import *



# urlpatterns = [
#         # Authentication Routes
#     path('signup/',signup_view, name='signup'),
#     path('signin/',signin_view, name='signin'),
#     path('signout/',signout_view, name='signout'),
    
    # Home Route
    # path('',home_view, name='home'),
    
    # Meal Selection Flow
    # path('categories/',meal_categories, name='meal_categories'),
    # path('categories/<int:category_id>/items/',menu_items, name='menu_items'),
    # path('order/<int:menu_item_id>/',order_meal, name='order_meal'),
    
    # Balance Management
    # path('balance/top-up/',top_up_balance, name='top_up'),
    # path('expenses/',expense_history, name='expense_history'),
# ]
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.homeview, name='home'),
#     # path('signup/', views.student_signup, name='student_signup'),
#     # path('signup/success/', views.signup_success, name='signup_success'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('', views.welcome_view, name='welcome'),
]