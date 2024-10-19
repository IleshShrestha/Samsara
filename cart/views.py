from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from .cart import Cart
from store.models import Product
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.utils.encoding import smart_str
from django.contrib.auth.models import User
import stripe
import json
import time


stripe.api_key = settings.STRIPE_SECRET_KEY



def cart_summary(request):

    cart = Cart(request)

    #{prod: [size][quant]}
    quantities = cart.get_quants()
    cart_products, prod_ids = cart.get_prods()
    # toal = #, individual = {"id": #}
    total, individual_totals = cart.cart_total()

    print(total)
    for product in cart_products:
        print(product.id)
    return render(request, "cart_summary.html", {"cart_products": cart_products, "cart_quantities": quantities,"individual_totals": individual_totals, "total": total, "prod_ids": prod_ids})


def cart_add(request):
# Get the cart
    cart = Cart(request)
    
	# test for POST
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        size = (request.POST.get('size'))

        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)
        cart_quantity = cart.__len__() 

        # Save to session
        if cart.add(product=product, quantity=product_qty, size=size):

            # Return resonse
            response = JsonResponse({'qty': cart_quantity, 'size': size})


        else:
            messages.error(request, "Item is already in the cart")
            response = JsonResponse({'qty': cart_quantity, 'size': size})
        return response

        


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        size = request.POST.get('size')
        cart.delete(product = product_id, size = size)

        messages.success(request, ("Item was deleted from the cart!"))
        return redirect('cart_summary')


def cart_update(request):
    cart = Cart(request)
    type_of_request = str(request.POST.get("type"))
    if request.POST.get('action') == 'post' and type_of_request == "+":
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        size = str(request.POST.get('size'))
        print(product_id, product_qty, size)
        cart.update(product = product_id, quantity = product_qty, size = size)
        messages.success(request, ("Your cart has been updated!"))
        response = JsonResponse({'qty': product_qty, 'size': size})
        return response
    

    elif request.POST.get('action') == 'post' and type_of_request == "-":
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        size = str(request.POST.get('size'))
        if product_qty == 0:
            response = JsonResponse({'qty': product_qty, 'size': size})
            return response
       
        print(product_id, product_qty, size)
        cart.update(product = product_id, quantity = product_qty, size = size)
        messages.success(request, ("Your cart has been updated!"))
        response = JsonResponse({'qty': product_qty, 'size': size})
        return response
    else:
        pass

# under dev for multiple porducts in cart    
def create_checkout_session(request):
    # if request.method == "POST":
        
        cart = Cart(request)

        cart_quant = cart.get_quants()
        cart_products, prod_ids = cart.get_prods()
        # cart_quant { prod_id : [size] [quant]} cart_prods{[prod objects]}
        # {'product': product price} 
        list_of_prod = {}
        for product in cart_products:

            quantity = cart_quant[str(product.pk)]
            name = product.name
            if product.is_sale:
                list_of_prod[product.id] = [name, int(product.sale_price * 100), quantity ]
            else:
                list_of_prod[product.id] = [name, int(product.price * 100), quantity]
        items = []
        print(list_of_prod)
        for key, value in list_of_prod.items():
            items.append({
                "price_data": {
                    "currency": "usd",
                    "unit_amount": value[1],
                    "product_data":{
                        "name": value[0]
                    },
                },
                "quantity": value[2]
                }) 
    
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=items,
            mode="payment",
            success_url= request.build_absolute_uri(reverse("success")),
            cancel_url=request.build_absolute_uri(reverse("cancel")),
            metadata={"product_ids": cart_quant.keys(), "user_id": request.user.id},
            automatic_tax={'enabled': True},
            shipping_address_collection={"allowed_countries": ["US"]},

        )

        return redirect(session.url, code=303)



@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = smart_str(request.body)
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError:
        return JsonResponse({'error': "Invalidpayload"}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': "Invalid Signature"}, status=400)
      
    return JsonResponse({"status": "success"})



def cancel(request):
    return redirect("cart_summary")

def success(request):
    return redirect("main")
