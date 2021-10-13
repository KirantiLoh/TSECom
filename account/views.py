from django.contrib import auth
from django.contrib.auth.models import User
from django.core import exceptions
from django.shortcuts import redirect, render

from api.views import bought_item_view
from .models import Profile, Cart, Item
from api.models import Product, BoughtItem
from .forms import RegisterForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate

# Create your views here.
@login_required(login_url="login")
def cart_view(request):
    cart = Cart.objects.get(user = request.user)
    items = Item.objects.filter(cart = cart)
    return render(request, 'cart.html', {'cart' : cart, 'items':items})

@login_required(login_url="login")
def profile_view(request):
    profile = Profile.objects.get(user = request.user)
    sold_products = Product.objects.filter(seller = profile).order_by('-sold').order_by('-rating')
    return render(request, 'profile.html', {'profile' : profile, 'sold_products' : sold_products})

def public_profile_view(request, id):
    try:
        profile = Profile.objects.get(id = id)
        sold_products = Product.objects.filter(seller = profile).order_by('-sold').order_by('-rating')
    except ObjectDoesNotExist:
        return redirect('Profile')
    return render(request, 'profile.html', {'profile' : profile, 'sold_products' : sold_products})

@login_required(login_url="login")
def edit_profile_view(request):
    form = EditProfileForm
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            profile = Profile.objects.get(user = request.user)
            user = User.objects.get(username = request.user)
            image = form.cleaned_data['image']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            city = form.cleaned_data['city']
            if image:
                profile.image = image
            elif name:
                user.first_name = name
            elif email:
                user.email = email
            elif city:
                profile.city = city
            profile.save()
            user.save()
            return redirect('Profile')
    return render(request, 'edit_profile.html', {'form' : form})

@login_required(login_url="login")
def add_to_cart(request,id):
    if request.method == "POST":
        product = Product.objects.get(id=id)
        cart = Cart.objects.get(user = request.user)
        amount = request.POST['amount']
        if int(amount) > 0:
            try:
                item = Item.objects.get(product = product)
                item.quantity += int(amount)
                if item.quantity > product.stock:
                    item.quantity = product.stock
                item.subtotal = product.price * item.quantity
                item.save()
                cart.total += item.subtotal
                cart.save()
            except ObjectDoesNotExist:
                item = Item.objects.create(cart = cart, quantity = int(amount), subtotal = product.price * int(amount), product = product)
                item.save()
                cart.total += item.subtotal
                cart.save()
            return redirect('Cart')
        else:
            return redirect('Product', id =id)
    else:
        return redirect('Product', id =id)

def delete_item_from_cart(request, id):
    cart = Cart.objects.get(user = request.user)
    item = Item.objects.get(id = id)
    if item.quantity > 1:
        item.quantity -= 1
        item.subtotal -= item.product.price
        item.save()
        cart.total -= item.product.price
        cart.save()
    else:
        item.delete()
        cart.total -= item.product.price
        cart.save()
    return redirect('Cart')

@login_required(login_url='login')
def checkout(request):
    profile = Profile.objects.get(user=request.user)
    cart = Cart.objects.get(user = request.user)
    balance = profile.balance
    total = cart.total
    if total <= 0:
        return redirect('Cart')
    else:
        diff = balance - total
        if diff < 0:
            return redirect("Checkout Fail")
        else:
            profile.balance = diff
            profile.save()
            items = Item.objects.filter(cart=cart)
            for item in items:
                product = item.product
                product.stock -= item.quantity
                product.sold += item.quantity
                product.seller.balance += total
                product.save()
                try:
                    boughtitem = BoughtItem.objects.get(buyer = profile, product = product)
                    boughtitem.quantity += item.quantity
                except ObjectDoesNotExist:
                    boughtitem = BoughtItem.objects.create(buyer = profile, product = product)
                boughtitem.save()
            items.delete()
            cart.total = 0
            cart.save()
            return redirect("Checkout Success")

def checkout_success_view(request):
    return render(request, 'checkout_success.html')

def checkout_fail_view(request):
    return render(request, 'checkout_fail.html')

def register_view(request):
    form = RegisterForm
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = User.objects.get(username=name)
            profile = Profile.objects.create(user = user, balance = 100000000, city='Jakarta')
            profile.save()
            cart = Cart.objects.create(user=user)
            cart.save()
            log_user = authenticate(request, username=name, password=password)
            login(request, log_user)
            return redirect('Home')
    return render(request, 'registration/register.html', {'form' : form})