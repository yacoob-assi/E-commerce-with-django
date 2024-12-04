from .models import (
    Address,
    CartOrder,
    CartOrderItems,
    Category,
    Product,
    ProductImages,
    Wishlist,
    Vendor,
    ProductReview,
)


def default(request):
    if "wish" in request.session:
        wishes = request.session["wish"]
    else:
        wishes = []
    products = request.session.get("products", [])
    cartProductIds = [product["id"] for product in products]
    wishesLength = wishes
    print(len(products))
    print("ppppppppppppppppppppppppppppp")
    return {
        "categories": Category.objects.all(),
        "cartLength": len(products),
        "cartProducts": products,
        "cartProductIds": cartProductIds,
        "wishLength": len(wishesLength),
    }
