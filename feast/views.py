# from django.shortcuts import render,redirect
# from .models import CustomUser
# from django.contrib import messages
# from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth.decorators import login_required
# import os
# Create your views here.

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.timezone import localdate
from datetime import datetime
from django.utils.timezone import now

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')  # Redirect to your home page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('home')  # Redirect to your home page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('welcome')
login_required
def home_view(request):
    if request.user.is_superuser:
        return render(request, 'admin_home.html')  # Superuser dashboard
    else:
        return render(request, 'student_home.html')  # Student dashboard
def welcome_view(request):
    user=request.user
    # print('user',request.user)
    return render(request,'welcome.html',{'user':user})
# def home_view(request):
#     return render(request, 'feast/home.html')


def menu_list(request):
    menu_items = Menu.objects.all()
    return render(request, 'menu_list.html', {'menu_items': menu_items})

def add_menu_item(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuForm()
    return render(request, 'add_menu.html', {'form': form})

def delete_menu_item(request, item_id):
    item = get_object_or_404(Menu, id=item_id)
    item.delete()
    return redirect('menu_list')


@login_required
def buy_menu_item(request, item_id):
    menu_item = get_object_or_404(Menu, id=item_id)
    
    # Create an order record
    order = Order.objects.create(
        student=request.user,
        menu_item=menu_item,
        total_price=menu_item.price  # Assuming quantity = 1
    )

    return redirect('order_food')  # Redirect to expense tracking


@login_required
def view_expense(request):
    today = localdate()
    month = today.month
    year = today.year

    daily_expense = Order.objects.filter(student=request.user, order_date__date=today).aggregate(Sum('total_price'))['total_price__sum'] or 0
    monthly_expense = Order.objects.filter(student=request.user, order_date__month=month, order_date__year=year).aggregate(Sum('total_price'))['total_price__sum'] or 0

    return render(request, 'expense.html', {'daily_expense': daily_expense, 'monthly_expense': monthly_expense})


@login_required
def order_food(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.student = request.user  # Assign the logged-in student
            order.total_price = order.menu_item.price * order.quantity  # Calculate total cost
            order.save()
            return redirect('view_orders')  # Redirect to the orders page
    else:
        form = OrderForm()

    menu_items = Menu.objects.all()
    return render(request, 'order_food.html', {'form': form, 'menu_items': menu_items})

### **View Orders for the Current Day**
@login_required
def view_orders(request):
    today_orders = Order.objects.filter(student=request.user, order_date=now().date())
    return render(request, 'view_orders.html', {'orders': today_orders})
