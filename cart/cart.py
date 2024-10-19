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


    def add(self, product, quantity, size):
        product_id = str(product.id)
        product_qty = quantity
        size = size
        
        
        # comparing the id and the size to see if its in the cart
        # {product id: [[sizes][quantites]]}
        # if already in the cart with prod id and size pass
        if product_id in self.cart and size in self.cart[str(product_id)][0]:
            return False
        
        # want the same product but in a different size
        elif product_id in self.cart:
            self.cart[product_id][0].append(size)
            self.cart[product_id][1].append(quantity)

            
        # product is not in the cart
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            # {product id: [{xs: quant }, {s: quant}]}
            self.cart[product_id] = [[size]]
            self.cart[product_id].append([quantity])

        self.session.modified = True
        return True

    def cart_total(self):

        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        quantities = self.cart
        total = 0

        # {prod: [[size][total_val]]}
        individual_totals = {}
        # {prod: [[size][quant]]}
        for product in products:
            if str(product.id) in products_ids:
                sizes = quantities[str(product.id)][0]
                quant = quantities[str(product.id)][1]
                # [[size], [quant]]
                for i in range(len(sizes)):
                    size = sizes[i]
                    number = quant[i]
                   
                    if product.is_sale:

                        total += product.sale_price * quant[i]

                        if product.id in individual_totals.keys():
                            individual_totals[product.id][0].append(size)
                            individual_totals[product.id][1].append(product.sale_price * number)

                        else:
                            individual_totals[product.id] = [[size], [product.sale_price * number]]

                    else:
                        total += product.price * number
                        if product.id in individual_totals.keys():
                            individual_totals[product.id][0].append(size)
                            individual_totals[product.id][1].append(product.price * number)

                        else:
                            individual_totals[product.id] = [[size], [product.price * number]]
                            

        return total, individual_totals
        
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        
        product_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in = product_ids)
        return [products, product_ids]
    
    def get_quants(self):
        quantites = self.cart
        return quantites
    
    # need to change
    def update(self, product, quantity, size):

        product_id = str(product)
        product_qty = int(quantity)
        size = size
        
        oldcart = self.cart

        #{ prod: [size][quant]}
        index = oldcart[product_id][0].index(size)
        oldcart[product_id][1][index] = product_qty

        self.session.modified = True
        newcart = self.cart
        return newcart
    
    def delete(self, product, size):
        
        product_id = str(product)
        size = size

        # {prod id: [sizes] [quants]}
        # need to make o(1)
        if product_id in self.cart and size in self.cart[product_id][0]:
            index = self.cart[product_id][0].index(size)
            del self.cart[product_id][0][index]
            del self.cart[product_id][1][index]

        self.session.modified = True