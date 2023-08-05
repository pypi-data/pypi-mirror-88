# Revpayment

This is the common starter project of Revtel's backend payment microservice
## Payment documents

* Ecpay doc: https://drive.google.com/drive/folders/1MtLL9epZS-n-eP4vHeJkSaS4tMuir69h
* NCCC doc: https://drive.google.com/open?id=1ugrP0mAbsQfRSnJ4jiKohsvOXLJL4tfJ

## Microservice setup 

In your dev env install the package, like this:

```bash
source .env/bin/activate
pip install revpayment
```

## Request setup

In your *settings.py* set default class, like this:

```bash
REVPAYMENT = {
    'PRODUCT_CLASS' : 'your product class reference path',
    'PRODUCT_SERIALIZER_CLASS' : 'your product serializer class reference path',
    'BUYER_CLASS' : 'your user class reference path',
    'VERIFY_METHOD' : 'your OAuth verify method class reference path'
    'CLIENT_SECRET': your CLIENT_SECRET,
    'WEB_HOST': your WEB_HOST,
    'API_HOST': your API_HOST,
}
```

Revpayment has some built-in classes, which can also be changed:

```bash
REVPAYMENT = {
    'ORDER_CLASS' : 'your order class reference path',
    'ITEM_CLASS' : 'your item class reference path',
    'CALC_CLASS' : 'your calculation class reference path',
    'CONFIG_CLASS' : 'your config class reference path',
    'HANDLER_CLASS' : 'your handler class reference path',
    'INVOICE_CLASS' : 'your invoice class reference path',
}
```

## Usage

You can launch the API using the package URL:
### url.py
```bash
from revpayment.urls import checkout_urlpatterns, cart_urlpatterns

urlpatterns = [
    *checkout_urlpatterns
    *cart_urlpatterns
]
```

## Custom Your payment handler examples
### Setting the class in setting.py
```bash
REVPAYMENT = {
    'HANDLER_CLASS' : 'your handler class reference path',
}
```

### Subscript product when on_payment_success
```bash
from revpayment.handlers import BaseHandler
from "Your subscription.py path" import Subscription

class OrderHandler(BaseHandler):
    def on_payment_success(self, previous):
        #   Your new code is as follows:
        cart = json.loads(self.order.cart)
        items = cart['items']
        for item in items:
            product = Product.objects.get(id=item['product']['id'])
            Subscription.objects.create(
                owner=self.order.buyer, product=product)
```

### Create Invoice when on_payment_success
```bash
from revpayment.handlers import BaseHandler
from revpayment.invoice import InvoiceSDK

class OrderHandler(BaseHandler):
    def issue_invoice(self):
        sdk = InvoiceSDK(order=self.order, invoice_type='neweb')
        try:
            invoice = sdk.issue_invoice()
            invoice.order = self.order
            invoice.save()
        except Exception as e:
            print(e)

    def on_payment_success(self, previous):
        self.issue_invoice()
```

### Check price when before_checkout
```bash
from revpayment.handlers import BaseHandler

class OrderHandler(BaseHandler):
    def before_checkout(self, state):
        #   Your new code is as follows:
        cart, buyer = self.get_state_meta(state)
        cart = json.load(state.cart)
        if cart['calculations']['amount'] <= 0:
            raise # YourRaiseMessage&Code
```

### Clear cart when on_order_create
```bash
from revpayment.handlers import BaseHandler
from revpayment.carts import Cart

class OrderHandler(BaseHandler):
    #   Your new code is as follows:
    def on_order_create(self):
        cart = Cart(self.order.buyer)
        cart.clear_cart()
```

## Customize the inspection cart before adding products example
### Setting the class in setting.py
```bash
REVPAYMENT = {
    'ITEM_CLASS' : 'your item class reference path',
}
```

### Create your items.py
```bash
from revpayment.items import Item
from "Your subscription.py path" import Subscription


class CustomItem(Item):
    def __init__(self, *args, **kwargs):
        from revpayment.carts import Cart
        super().__init__(*args, **kwargs)
        cart = Cart(self.profile)
        #   Check if the product already exists in the cart
        if any([item for item in cart.cart['items'] if item['product']['id'] == self.product.id]):
            raise # YourRaiseMessage&Code
        #   Check if the product is subscribed 
        if Subscription.objects.filter(product=self.product, owner=self.profile):
            raise # YourRaiseMessage&Code
```
## Django project setup

```bash
npm run config:stg/prod
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```



