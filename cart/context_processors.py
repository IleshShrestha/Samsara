from .cart import Cart

def cart(request):
    cart = Cart(request)
    cart_prod, id = cart.get_prods()
    return {'cart': cart, 'cart_prod': cart_prod}