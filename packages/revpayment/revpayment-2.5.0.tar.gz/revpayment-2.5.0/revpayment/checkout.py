from revpayment.settings import api_settings
from revpayment.models import RedirectState
from django.conf import settings
import requests
import json
import jwt
from jwcrypto.jwt import JWK


class CheckoutSDK:
    payment_classes = (
        ('neweb', api_settings.DEFAULT_NEWEB_CLASS),
        ('ecpay', api_settings.DEFAULT_ECPAY_CLASS),
        ('credit', api_settings.DEFAULT_CREDIT_CLASS),
    )
    handler_class = api_settings.HANDLER_CLASS

    def __init__(self, state):
        self.state = state
        if type(state.cart) is str:
            self.cart = json.loads(state.cart)
        elif type(state.cart) is dict:
            self.cart = state.cart
        else:
            raise TypeError
        self.payment_type = state.payment_type
        self.payment_subtype = state.payment_subtype
        self.buyer = state.buyer

    def get_payment_class(self):
        try:
            payment_class = [
                c[1] for c in self.payment_classes if c[0] == self.payment_type][0]
            return payment_class
        except IndexError:
            raise ValueError('payment_type is not valid')

    def get_payment(self):
        payment_class = self.get_payment_class()
        return payment_class(buyer=self.buyer, payment_subtype=self.payment_subtype, cart=self.cart, order_id=self.state.order_id)

    def before_checkout(self):
        handler = self.handler_class(order=None)
        handler.before_checkout(state=self.state)

    def after_checkout(self):
        handler = self.handler_class(order=None)
        handler.after_checkout(state=self.state)

    def checkout(self):
        state = self.state
        self.before_checkout()
        payment = self.get_payment()
        result = payment.checkout(state)
        self.after_checkout()
        return result

    def callback(self, data):
        payment = self.get_payment()
        order, changed = payment.callback(self.state, data)
        handler = self.handler_class(order=order)
        handler.on_payment_result(changed)
        return f'{self.state.redirect_url}/order?id={order.id}'

    def customer_redirect(self, data):
        payment = self.get_payment()
        order, changed = payment.customer_redirect(self.state, data)
        handler = self.handler_class(order=order)
        handler.on_payment_result(changed)
        return f'{self.state.redirect_url}/order?id={order.id}'


class BaseCertificate:
    default_aud = settings.CLIENT_ID

    def __init__(self, cert):
        self.unverified = jwt.decode(cert, verify=False)
        self.headers = jwt.get_unverified_header(cert)
        self.cert = cert

    def get_order_id(self, sub):
        raise NotImplementedError

    def get_key_url(self):
        iss = self.unverified['iss']
        host = iss.split('.')[0]
        if host[-4:] in ['-stg', '-dev']:
            return 'https://auth-stg.revtel-api.com/v3/certs'
        return 'https://auth.revtel-api.com/v3/certs'

    def get_pub_key(self):
        url = self.get_key_url()
        jwks = requests.get(url).json()['keys']
        key = [jwk for jwk in jwks if jwk['kid'] == self.headers['kid']][0]
        real_key = JWK.from_json(json.dumps(key))
        return real_key.export_to_pem()

    def verify(self):
        pub = self.get_pub_key()
        decoded = jwt.decode(self.cert, algorithms='RS256', key=pub, verify=True, audience=self.default_aud)
        if decoded['typ'] != 'certificate':
            raise

        sub = decoded['sub']
        order_id = self.get_order_id(sub)
        state = RedirectState.objects.get(order_id=order_id)
        return state, sub


class NewebCertificate(BaseCertificate):
    def get_order_id(self, sub):
        return sub['Result']['MerchantOrderNo']


class EcpayCertificate(BaseCertificate):
    def get_order_id(self, sub):
        return sub['MerchantTradeNo']


def check_certificate(cert):
    unverified = jwt.decode(cert, verify=False)
    provider = unverified['provider']
    if provider == 'ecpay':
        cert_class = EcpayCertificate
    elif provider == 'neweb':
        cert_class = NewebCertificate

    certificate = cert_class(cert)
    return certificate.verify()
