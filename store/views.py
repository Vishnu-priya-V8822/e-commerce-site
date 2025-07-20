from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'store/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})


@login_required(login_url='login')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


@login_required(login_url='login')
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': item_total,
        })
        total += item_total

    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})


@login_required(login_url='login')
def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': item_total,
        })
        total += item_total

    if request.method == 'POST':
        item_list = "\n".join([f"{item['product'].name} × {item['quantity']}" for item in cart_items])
        Order.objects.create(name="Customer", items=item_list, total=total)
        request.session['cart'] = {}  # clear cart
        return redirect('order_success')

    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total': total})


@login_required(login_url='login')
def order_success(request):
    return render(request, 'store/success.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration 
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})
