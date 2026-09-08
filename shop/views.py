from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Laptop, Order, OrderItem, Favorite
from .cart import Cart
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import RegisterForm, ProfileForm

def laptop_list(request):
    laptops = Laptop.objects.all().order_by('-created_at')

    brand = request.GET.get('brand')
    if brand:
        laptops = laptops.filter(brand__iexact=brand)

    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        laptops = laptops.filter(price__gte=price_min)
    if price_max:
        laptops = laptops.filter(price__lte=price_max)

    q = request.GET.get('q')
    if q:
        laptops = laptops.filter(Q(brand__icontains=q) | Q(model_name__icontains=q))

    paginator = Paginator(laptops, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    brands = Laptop.objects.values_list('brand', flat=True).distinct()

    context = {
        'page_obj' : page_obj,
        'brands' : brands,
        'selected_brand' : brand,
        'price_min' : price_min,
        'price_max' : price_max,
        'q' : q,
    }
    return render(request, 'shop/laptop_list.html', context)

def laptop_detail(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    return render(request, 'shop/laptop_detail.html', {'laptop': laptop})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('laptop_list')
    else:
        form = RegisterForm()
    return render(request, 'shop/register.html', {'form': form})

def user_login(request):
    from allauth.socialaccount.models import SocialApp
    google_enabled = SocialApp.objects.filter(provider='google').exists()

    next_url = request.POST.get('next') or request.GET.get('next') or ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(next_url or 'laptop_list')
        else:
            return render(request, 'shop/login.html', {
                'error': 'Неверные имя пользователя или пароль',
                'google_enabled': google_enabled,
                'next': next_url
            })
    return render(request, 'shop/login.html', {'google_enabled': google_enabled, 'next': next_url})

def user_logout(request):
    logout(request)
    return redirect('laptop_list')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'shop/profile.html', {'form':form})

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart.html', {'cart' : cart})

@login_required
def cart_add(request, laptop_id):
    laptop = get_object_or_404(Laptop, id=laptop_id)
    cart = Cart(request)
    cart.add(laptop)
    return redirect('cart_detail')

@login_required
def cart_remove(request, laptop_id):
    laptop = get_object_or_404(Laptop, id=laptop_id)
    cart = Cart(request)
    cart.remove(laptop)
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_price=cart.get_total_price(),
            address=request.POST.get('address', ''),
            phone=request.POST.get('phone', ''),
            notes=request.POST.get('notes', '')
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                laptop=item['laptop'],
                quantity=item['quantity'],
                price=item['price']
            )
        cart.clear()
        return redirect('order_success')
    return render(request, 'shop/checkout.html', {'cart': cart})

def order_success(request):
    return render(request, 'shop/order_success.html')


@login_required
def favorite_add(request, laptop_id):
    laptop = get_object_or_404(Laptop, id=laptop_id)
    Favorite.objects.get_or_create(user=request.user, laptop=laptop)
    return redirect('laptop_detail', pk=laptop_id)

@login_required
def favorite_remove(request, laptop_id):
    laptop = get_object_or_404(Laptop, id=laptop_id)
    Favorite.objects.filter(user=request.user, laptop=laptop).delete()
    return redirect('favorite_list')

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('laptop')
    return render(request, 'shop/favorite_list.html', {'favorites': favorites})


