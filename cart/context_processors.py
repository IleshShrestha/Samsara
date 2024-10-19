from .cart import Cart

def cart(request):
    cart = Cart(request)
    cart_prod, id = cart.get_prods()
    cart_quant = cart.get_quants()
    cart_total = cart.cart_total()
    print(cart_quant)
    print(cart_total)

    return {'cart': cart, 'cart_prod': cart_prod, 'cart_quant': cart_quant, 'cart_total': cart_total}