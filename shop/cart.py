from decimal import Decimal
from django.conf import settings
from django.apps import apps


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID) or {}

    def add(self, laptop, quantity=1):
        laptop_id = str(laptop.id)
        if laptop_id not in self.cart:
            self.cart[laptop_id] = {'quantity': 0, 'price': str(laptop.price)}
        self.cart[laptop_id]['quantity'] += quantity
        self.save()

    def remove(self, laptop):
        laptop_id = str(laptop.id)
        if laptop_id in self.cart:
            del self.cart[laptop_id]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def __iter__(self):
        Laptop = apps.get_model('shop', 'Laptop')
        laptops = Laptop.objects.filter(id__in=self.cart.keys())
        for laptop in laptops:
            self.cart[str(laptop.id)]['laptop'] = laptop
        for item in self.cart.values():
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def get_total_price(self):
        return sum(Decimal(i['price']) * i['quantity'] for i in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True