from store.models import Product


class Cart():
    def __init__(self, request):
        self.session = request.session

        # returning user
        cart = self.session.get('session_key')

        # create one for new users
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart


    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = quantity
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = product_qty

        self.session.modified = True

    def cart_total(self):

        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        quantities = self.cart
        total = 0

        for product in products:

            if str(product.id) in products_ids:
                value = quantities[str(product.id)]

                if product.is_sale:
                    total += product.sale_price * value

                else:
                    total += product.price * value
        

        return total
        
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        
        product_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in = product_ids)
        print("This is the prod ids" + str(product_ids))
        return [products, product_ids]
    
    def get_quants(self):
        quantites = self.cart
        return quantites
    
    def update(self, product, quantity):

        product_id = str(product)
        product_qty = int(quantity)
        
        oldcart = self.cart

        oldcart[product_id] = product_qty

        self.session.modified = True
        newcart = self.cart
        return newcart
    
    def delete(self, product):
        
        product_id = str(product)
        oldcart = self.cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True