from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render
from .models import BoughtItem, Product, Review
from django.db.models import Q
from account.models import Profile, Cart, Item
from .forms import AddProductForm, RestockForm, ReviewForm, EditProductForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

# Create your views here.
def home_view(request):
    products = Product.objects.filter().order_by('-date_added')[:6]
    return render(request, 'home.html', {'products' : products})

def get_started_view(request):
    return render(request, "get_started.html")

def search_result_view(request):
    if request.method == "GET":
        search = request.GET.get('q')
        if search == '':
            products = None
            sellers = None
        sellers = Profile.objects.filter(Q(user__username__icontains=search) | Q(user__first_name__icontains = search)).order_by('-rank')[:1]
        products = Product.objects.filter(Q(name__icontains=search) | Q(desc__icontains=search)).order_by('-sold').order_by('-rating')
    return render(request, 'search_result.html', {'products' : products, 'search' : search, 'sellers' : sellers})

def product_view(request, id):
    product = Product.objects.get(id = id)
    reviews = Review.objects.filter(product = product)
    seller = product.seller
    if request.user == seller.user:
        form = RestockForm
    else:
        form = None
    return render(request, 'product.html', {'product' : product, 'seller' : seller, 'reviews':reviews, "form" : form})

def all_product_view(request):
    products = Product.objects.all().order_by('-sold').order_by('-rating')
    return render(request, 'all_products.html', {'products' : products})

@login_required(login_url="login")
def add_product_view(request):
    form = AddProductForm
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['product_image']
            name = form.cleaned_data['name']
            desc = form.cleaned_data['desc']
            price = form.cleaned_data['price']
            stock = form.cleaned_data['stock']
            profile = Profile.objects.get(user = request.user)
            try:
                product = Product.objects.get(seller=profile, name = name)
                return redirect("Restock", id = product.id)
            except ObjectDoesNotExist:
                product = Product.objects.create(seller=profile, image = image, name = name, desc = desc, price = price, stock=int(stock))
                product.save()
                return redirect('Product', id = product.id)
    return render(request, 'add_product.html', {'form' : form})

@login_required(login_url="login")
def restock_view(request, id):
    try:
        product = Product.objects.get(id = id)
        form = RestockForm
        if request.method == "POST":
            form = RestockForm(request.POST, request.FILES)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                
                if product.stock == 0:
                    product.stock = int(amount)
                else:
                    product.stock += int(amount)
                product.save()
                return redirect('Product', id = product.id)
        return render(request, 'restock.html', {'form' : form, 'product':product})
    except ObjectDoesNotExist:
        return redirect('Checkout Fail')

@login_required(login_url="login")
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('Profile')

@login_required(login_url="login")
def add_review_view(request, id):
    try:
        product = Product.objects.get(id = id)
        profile = Profile.objects.get(user = request.user)
        bought_item = BoughtItem.objects.get(buyer = profile, product=product)
        if product.seller == profile:
            return redirect('Checkout Fail')
        form = ReviewForm
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                rating = int(form.cleaned_data['rating'])
                user_review = form.cleaned_data['review']
                review = Review.objects.create(product=product, review=user_review, rating=rating, reviewer = profile)
                review.save()
                rating = Review.objects.filter(product=product).aggregate(Avg('rating'))
                product.rating = rating['rating__avg']
                product.save()
                return redirect('Product', id = product.id)
        return render(request, 'add_review.html', {'form':form})
    except ObjectDoesNotExist:
        return redirect('Checkout Fail')
    
@login_required(login_url="login")
def bought_item_view(request):
    profile = Profile.objects.get(user=request.user)
    items = BoughtItem.objects.filter(buyer = profile).order_by('-date_bought')
    return render(request, 'bought_items.html', {'items' : items})

@login_required(login_url="login")
def edit_product_view(request, id):
    try:
        profile = Profile.objects.get(user = request.user)
        product = Product.objects.get(seller = profile, id = id)
        form = EditProductForm
        if request.method == "POST":
            form = EditProductForm(request.POST, request.FILES)
            if form.is_valid():
                product_image = form.cleaned_data['product_image']
                name = form.cleaned_data['name']
                desc = form.cleaned_data['desc']
                price = form.cleaned_data['price']
                stock = form.cleaned_data['stock']
                if product_image:
                    product.image = product_image
                elif name:
                    product.name = name
                elif desc:
                    product.desc = desc
                elif price:
                    product.price = int(price)
                elif stock:
                    product.stock += int(stock)
                product.save()
                return redirect('Product', id=id)
        return render(request, "edit_product.html", {"form" : form, "product" : product})
    except ObjectDoesNotExist:
        return redirect("Checkout Fail")

def send_message(request):
    if request.method == 'POST':
        name = request.POST['name']
        name = request.POST['name']
        name = request.POST['name']
        return redirect('Home')
    return HttpResponseForbidden('ONLY POST REQUEST ARE ALLOWED')