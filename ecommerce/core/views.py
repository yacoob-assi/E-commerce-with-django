from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Vendor, ProductReview
from taggit.models import Tag
from .forms import reviewForm
from django.http import JsonResponse
from django.db.models import Q, Max, Min
from django.template.loader import render_to_string
import json
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.cache import cache_control


# Create your views here.


def index(request):

    if "wish" in request.session:
        products = request.session["wish"]

    else:
        products = []

    wishes = [product["pid"] for product in products]
    context = {
        "products": Product.objects.filter(product_status="published").order_by("-id"),
        "categories": Category.objects.all(),
        "vendors": Vendor.objects.all(),
        "prices": Product.objects.aggregate(
            max_price=Max("price"), min_price=Min("price")
        ),
        "wishes": wishes,
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def blog_detail(request):
    return render(request, "blog-detail.html")


def blog(request):
    return render(request, "blog.html")


def contact(request):
    return render(request, "contact.html")


def home2(request):
    return render(request, "home-02.html")


def vendor(request):
    products = Vendor.objects.all()
    first_two = products[:2]
    others = products[2:]

    context = {"first_two": first_two, "others": others, "count": products.count()}

    return render(request, "vendor.html", context)


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {"product": product}
    return render(request, "product-detail.html", context)


def product(request, cid):
    category = Category.objects.get(cid=cid)
    category_products = Product.objects.filter(category=category)
    context = {"products": category_products}
    return render(request, "product.html", context)


def shoping_cart(request):
    if "totalCartPrice" in request.session:
        totalCartPrice = request.session["totalCartPrice"]
    else:
        totalCartPrice = 0
        if "products" in request.session:
            for p in request.session["products"]:
                totalCartPrice += float(p["price"])
    return render(
        request,
        "shoping-cart.html",
        {"totalCartPrice": totalCartPrice},
    )


def vendor_products(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor)
    context = {"products": products}
    return render(request, "vendor-products.html", context)


def category_products(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(category=category)
    context = {"products": products}
    return render(request, "category-products.html", context)


def tag_list(request, slug=None):
    products = (Product.objects.filter(product_status="published").order_by("-id"),)

    if slug:
        tag = get_object_or_404(Tag, slug=slug)
        products = Product.objects.filter(tags__in=[tag])
        context = {"products": products, "slug": slug}

    return render(request, "tag-list.html", context)


def reviews(request, pk):
    product = Product.objects.get(pk=pk)
    reviews = product.reviews.all

    context = {
        "product": product,
        "reviews": reviews,
        "form": reviewForm,
        "star1": product.reviews.filter(rating=1).count(),
        "star2": product.reviews.filter(rating=2).count(),
        "star3": product.reviews.filter(rating=3).count(),
        "star4": product.reviews.filter(rating=4).count(),
        "star5": product.reviews.filter(rating=5).count(),
    }

    return render(request, "reviews.html", context)


def save_review(request, pk):
    product = Product.objects.get(pk=pk)
    user = request.user

    review = ProductReview.objects.create(
        product=product,
        user=user,
        review=request.POST["review"],
        rating=request.POST["rating"],
    )
    context = {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,  # Add other fields if needed
        },
        "review": request.POST["review"],
        "rating": request.POST["rating"],
        "star1": product.reviews.filter(rating=1).count(),
        "star2": product.reviews.filter(rating=2).count(),
        "star3": product.reviews.filter(rating=3).count(),
        "star4": product.reviews.filter(rating=4).count(),
        "star5": product.reviews.filter(rating=5).count(),
    }

    return JsonResponse({"bool": True, "context": context})


def search_product(request):
    if "wish" in request.session:
        wishP = request.session["wish"]

    else:
        wishP = []

    query = request.GET["search"]
    products = Product.objects.filter(
        Q(title__icontains=query) | Q(category__title__icontains=query)
    ).order_by("-date")
    wishes = [product["pid"] for product in wishP]
    context = {"products": products, "wishes": wishes}
    return render(request, "search.html", context)


def filter_products(request):
    products = (
        Product.objects.filter(product_status="published").order_by("-id")
    ).distinct()

    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")
    currentval = float(request.GET["current"])
    # maxval=request.GET['max'];
    # minval=request.GET['min'];
    if currentval > 0:
        products = products.filter(price__lte=currentval)

    if len(categories) > 0:
        products = products.filter(category__cid__in=categories).distinct()

    if len(vendors) > 0:
        products = products.filter(vendor__vid__in=vendors).distinct()

    html = render_to_string("filter-products.html", {"products": products})
    return JsonResponse({"data": html})


def addToCart(request):
    id = request.GET["pid"]
    price = request.GET["pPrice"]
    image = request.GET["pImage"]
    title = request.GET["pTitle"]
    quntity = request.GET["pQuntity"]

    product = {
        "id": id,
        "price": price,
        "image": image,
        "title": title,
        "quntity": quntity,
        "totalPrice": price,
    }

    if "totalCartPrice" in request.session:
        request.session["totalCartPrice"] = float(
            request.session["totalCartPrice"]
        ) + float(price)
    else:
        request.session["totalCartPrice"] = price

    if "products" not in request.session:
        request.session["products"] = []

    products = request.session["products"]

    updated = False

    for p in products:
        if p["id"] == id:
            p.update(product)
            updated = True

    if not updated:
        products.append(product)

    request.session["products"] = products
    return JsonResponse({"data": products})


def shoping_list(request):
    if "totalCartPrice" in request.session:
        totalCartPrice = request.session["totalCartPrice"]
    else:
        totalCartPrice = 0

    return render(request, "cart-list.html", {"total": totalCartPrice})


def update_cart(request):
    productsSession = request.session.get("products", [])
    totalCartPrice = request.GET["totalCartPrice"]

    request.session["totalCartPrice"] = totalCartPrice

    products = json.loads(
        request.GET.get("cartProducts", "[]")
    )  # Ensure you parse the data correctly
    for i in range(len(products)):
        pid = products[i]["pid"]
        quntity = products[i]["quntity"]
        totalPrice = products[i]["totalPrice"]

        productsSession[i]["id"] = pid
        productsSession[i]["quntity"] = quntity
        productsSession[i]["totalPrice"] = totalPrice
        # Find the matching product in the session

    request.session["products"] = productsSession
    return JsonResponse({"data": productsSession})


def delete_cart(request):
    pid = request.GET["id"]
    price = float(request.GET["price"])

    cart_products = request.session.get("products", [])
    result = False
    for product in cart_products:

        if pid == product["id"]:
            cart_products.remove(product)
            request.session["totalCartPrice"] = (
                float(request.session["totalCartPrice"]) - price
            )

            result = True

    request.session["products"] = cart_products

    return JsonResponse({"data": result, "length": len(cart_products)})


@login_required
def invoice(request):
    if "totalCartPrice" in request.session:
        totalCartPrice = request.session["totalCartPrice"]
    else:
        totalCartPrice = 0

    host = request.get_host()
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": totalCartPrice,
        "item_name": "Order-Item-No-3",
        "invoice": "INVOICE-NO-3",
        "currency_code": "USD",
        "notify_url": "http://{}{}".format(host, reverse("paypal-ipn")),
        "return_url": "http://{}{}".format(host, reverse("payment-completed")),
        "cancel_url": "http://{}{}".format(host, reverse("payment-filed")),
    }

    paypal_button = PayPalPaymentsForm(initial=paypal_dict)
    if "totalCartPrice" in request.session:
        totalCartPrice = request.session["totalCartPrice"]
    else:
        totalCartPrice = 0
    tax = float(totalCartPrice) / 10
    total = tax + float(totalCartPrice)
    context = {
        "totalPrice": totalCartPrice,
        "username": request.user.username,
        "email": request.user.email,
        "time": datetime.now().strftime("%d %b %Y, %H:%M:%S"),
        "due_date": (datetime.now() + timedelta(days=3)).strftime("%d %b %Y"),
        "tax": tax,
        "total": total,
        "payPalButton": paypal_button,
    }
    return render(request, "invoice.html", context)


def paypal_completed(request):
    if "totalCartPrice" in request.session:
        del request.session["totalCartPrice"]
        del request.session["products"]

    return render(request, "payment_completed.html")


def paypal_failed(request):

    return render(request, "payment_failed.html")


def addToWish(request):

    pid = request.GET["pid"]
    price = request.GET["pPrice"]
    image = request.GET["pImage"]
    title = request.GET["pTitle"]
    quntity = request.GET["pQuntity"]

    product = {
        "pid": pid,
        "price": price,
        "image": image,
        "title": title,
        "quntity": quntity,
        "totalPrice": price,
    }
    inlist = False
    if "wish" not in request.session:
        request.session["wish"] = []

    products = request.session["wish"]
    for p in products:
        if p["pid"] == product["pid"]:
            inlist = True

    if not inlist:
        products.append(product)

    request.session["wish"] = products

    return JsonResponse({"length": len(products)})


def wishListPage(request):
    if "wish" in request.session:
        products = request.session["wish"]

    else:
        products = []

    context = {"wishes": products}
    return render(request, "wishList.html", context)


def remove_wish(request):
    pid = request.GET["pid"]

    if "wish" in request.session:
        products = request.session["wish"]

    else:
        products = []
    for p in products:
        if p["pid"] == pid:
            products.remove(p)

    request.session["wish"] = products
    return JsonResponse({"length": len(products)})
