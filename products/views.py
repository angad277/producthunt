from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Product
# Create your views here.

def home(request):
    products = Product.objects
    return render(request, 'products/home.html',{'products':products})

@login_required(login_url = "/accounts/signup")
def create(request):
    if request.method == "POST":
        if request.POST.get("title") and request.POST.get("body") and request.POST.get("url") and request.FILES['icon'] and request.FILES['image']:
            product = Product()
            product.title = request.POST.get("title")
            product.body = request.POST.get("body")
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST.get("url")
            else:
                product.url = 'http://' + request.POST.get("url")
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html',{'error':'All fields must be filled.'})
    else:
        return render(request,'products/create.html')

def detail(request, product_id):
    product = get_object_or_404(Product,pk=product_id)
    return render(request, 'products/detail.html',{'product':product})

@login_required(login_url = "/accounts/signup")
def upvote(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product,pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/' + str(product.id))
