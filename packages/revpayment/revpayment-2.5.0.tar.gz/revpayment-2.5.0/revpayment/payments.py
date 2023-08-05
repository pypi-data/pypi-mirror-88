import requests
import json
from django.utils import timezone
from django.shortcuts import redirect
from django.http import HttpResponse
from datetime import datetime
from revpayment.settings import api_settings
from revpayment.logistics import LogisticsSDK


class BasePayment:
    URL = f'https://payment.revtel-api.com/{api_settings.PAYMENT_VERSION}'
    STAGE_URL = f'https://payment-stg.revtel-api.com/{api_settings.PAYMENT_VERSION}'
    PATH = None
    DEBUG = api_settings.DEBUG
    API_KEY = api_settings.CLIENT_SECRET
    WEB_HOST = api_settings.WEB_HOST
    API_HOST = api_settings.API_HOST
    order_class = api_settings.ORDER_CLASS
    handler_class = api_settings.HANDLER_CLASS
    payment_type = 'base'

    def __init__(self, cart, buyer, order_id, payment_subtype='default'):
        self.cart = cart
        self.payment_subtype = payment_subtype
        self.buyer = buyer
        self.order_id = order_id

    @property
    def host(self):
        if self.DEBUG:
            return self.STAGE_URL
        return self.URL

    def gen_order_id(self):
        return self.order_id

    def get_url(self):
        url = self.host
        return url + self.PATH

    def build_data(self, data):
        raise NotImplementedError

    def cvs_cod_checkout(self, state):
        cart = json.loads(state.cart)
        items = cart['items']
        config = cart['config']
        calc = cart['calculations']
        order = self.order_class.objects.create(cart=state.cart,
                                                id=state.order_id,
                                                title=items[0]['name'],
                                                receiver_email=config['email'],
                                                receiver_name=config['name'],
                                                receiver_phone=config.get('email', ''),
                                                receiver_address=config.get('address', ''),
                                                payment_type=state.payment_type,
                                                payment_subtype=state.payment_subtype,
                                                buyer=self.buyer,
                                                amount=calc['amount'],
                                                )
        changed = {'__created': True}
        hander = self.handler_class(order=order)
        hander.on_payment_result(changed)
        sdk = LogisticsSDK(order=order)
        sdk.create_logistics()
        return order

    def checkout(self, state):
        if self.payment_subtype == 'cvs_cod':
            order = self.cvs_cod_checkout(state)
            return redirect(f'{self.WEB_HOST}/order?id={order.id}')
        data = self.build_data(state)
        resp = requests.post(url=self.get_url(), json=data, headers={
            'Content-Type': 'application/json',
            'x-api-key': self.API_KEY
        })
        resp.raise_for_status()
        resp_json = resp.json()
        return redirect(resp_json['url'])

    def map_callback_data(self, data):
        raise NotImplementedError

    def callback(self, state, data):
        config = json.loads(state.cart)['config']
        items = json.loads(state.cart)['items']
        mapped = self.map_callback_data(data)
        changed = {'__created': False}
        if 'id' not in mapped:
            raise ValueError('id is required in mapped data')
        try:
            order = self.order_class.objects.get(
                id=mapped['id']
            )
            del mapped['id']
            for k, v in mapped.items():
                if getattr(order, k) != v:
                    changed[k] = v
                    changed['_' + k] = getattr(order, k)
                setattr(order, k, v)
            order.save()
        except:
            order = self.order_class.objects.create(
                **mapped,
                cart=state.cart,
                title=items[0]['name'],
                receiver_email=config['email'],
                receiver_name=config['name'],
                receiver_phone=config.get('email', ''),
                receiver_address=config.get('address', ''),
                payment_type=state.payment_type,
                payment_subtype=state.payment_subtype,
                payment_transaction_detail=json.dumps(
                    data, ensure_ascii=False),
                buyer=self.buyer,
                order_type=state.order_type
            )
            changed = mapped
            changed['__created'] = True

        state.order_id = order.id
        state.save()
        return order, changed

    def map_redirect_data(self, data):
        raise NotImplementedError

    def customer_redirect(self, state, data):
        config = json.loads(state.cart)['config']
        items = json.loads(state.cart)['items']
        mapped = self.map_redirect_data(data)
        changed = {'__created': False}
        if 'id' not in mapped:
            if not state.order_id:
                raise ValueError('state order_id is null')
            mapped['id'] = state.order_id
        try:
            order = self.order_class.objects.get(
                id=mapped['id']
            )
            del mapped['id']
            for k, v in mapped.items():
                if getattr(order, k) != v:
                    changed[k] = v
                    changed['_' + k] = getattr(order, k)
                setattr(order, k, v)
            order.save()
        except:
            order = self.order_class.objects.create(
                **mapped,
                payment_type=self.payment_type,
                payment_redirect_detail=json.dumps(data, ensure_ascii=False),
                cart=state.cart,
                title=items[0]['name'],
                receiver_email=config['email'],
                receiver_name=config['name'],
                receiver_phone=config.get('email', ''),
                receiver_address=config.get('address', ''),
                buyer=self.buyer
            )
            changed = mapped
            changed['__created'] = True

        state.order_id = order.id
        state.save()
        return order, mapped


class NewebPayment(BasePayment):
    PATH = '/newebpay/request'
    payment_type = 'neweb'
    PAYMENT_TABLE = {
        'default': {
            'CREDIT': 1,
            'CVSCOM': 0,
            'BARCODE': 1,
            'CVS': 1,
            'WEBATM': 1,
            'VACC': 1,
        },
        'credit': {
            'CREDIT': 1,
            'CVSCOM': 0,
            'BARCODE': 0,
            'CVS': 0,
            'WEBATM': 0,
        },
        'cvs_cod': {
            'CREDIT': 0,
            'CVSCOM': 2,
            'BARCODE': 0,
            'CVS': 0,
            'WEBATM': 0,
        },
        'web_atm': {
            'CREDIT': 0,
            'CVSCOM': 0,
            'BARCODE': 0,
            'CVS': 0,
            'WEBATM': 1,
        },
        'cvs': {
            'CREDIT': 0,
            'CVSCOM': 0,
            'BARCODE': 0,
            'CVS': 1,
            'WEBATM': 0,
        },
        'atm': {
            'VACC': 1,
            'CREDIT': 0,
            'CVSCOM': 0,
            'BARCODE': 0,
            'CVS': 0,
            'WEBATM': 0,
        }
    }

    def build_data(self, state):
        payment_subtype = self.PAYMENT_TABLE[self.payment_subtype]
        cart = self.cart
        items = cart['items']
        now = timezone.now()
        data = {
            'TimeStamp': str(int(now.timestamp())),
            'Amt': int(cart['calculations']['amount']),
            'Email': cart['config']['email'],
            'ItemDesc': items[0]['name'],
            'MerchantOrderNo': self.gen_order_id(),
            'CREDIT': 1,
            'CVSCOM': cart['config'].get('CVSCOM', 0),
            'BARCODE': 1,
            'CVS': 1,
            'WEBATM': 1,
            **payment_subtype
        }
        return data

    def map_callback_data(self, data):
        return_code = data.get('Status')
        payment_data = {
            'id': data['Result']['MerchantOrderNo'],
            'payment_status': 'success' if return_code == 'SUCCESS' else 'failure',
            'amount': data['Result']['Amt']
        }
        return payment_data

    def map_redirect_data(self, data):
        payload = {}
        if not data.get('Result'):
            return {}
        result = data['Result']
        payment_type = result['PaymentType']
        if data['Status'] == 'SUCCESS':
            payload['id'] = self.order_id
            payload['amount'] = result['Amt'] if type(
                result['Amt']) in [float, int] else int(result['Amt'])
            payload['payment_status'] = 'code_generated'
            payload['pay_deadline'] = result['ExpireDate'] + 'T' + result['ExpireTime']
            if payment_type == 'CVS':
                payload['payment_subtype'] = 'cvs'
                payload['code_no'] = result['CodeNo']
            elif payment_type == 'BARCODE':
                payload['payment_subtype'] = 'barcode'
                payload['barcode_1'] = result['Barcode_1']
                payload['barcode_2'] = result['Barcode_2']
                payload['barcode_3'] = result['Barcode_3']
            elif payment_type == 'VACC':
                payload['payment_subtype'] = 'atm'
                payload['bank_code'] = result['BankCode']
                payload['bank_account'] = result['CodeNo']

        return payload


class EcpayPayment(BasePayment):
    PATH = '/ecpay/request'
    payment_type = 'ecpay'
    PAYMENT_TABLE = {
        'default': {'ChoosePayment': 'ALL'},
        'credit': {'ChoosePayment': 'Credit'},
        'web_atm': {'ChoosePayment': 'WebATM'},
        'atm': {'ChoosePayment': 'ATM'},
        'cvs': {'ChoosePayment': 'CVS'},
        'barcode': {'ChoosePayment': 'BARCODE'},
    }

    def build_data(self, state):
        now = timezone.now()
        payment_subtype = self.PAYMENT_TABLE[self.payment_subtype]
        datetime_str = now.strftime('%Y/%m/%d %H:%M:%S')
        trade_no = self.gen_order_id()
        cart = self.cart
        calc = cart['calculations']
        config = cart['config']
        items = cart['items']
        data = {
            'MerchantTradeNo': trade_no,
            'MerchantTradeDate': datetime_str,
            'TotalAmount': int(calc['amount']),
            'ItemName': '#'.join([item['name'] for item in items]),
            'TradeDesc': 'None',
            'ChoosePayment': 'ALL',
            'InvoiceMark': 'N',
            'BindingCard': 1,
            'MerchantMemberID': self.buyer.payment.uid,
            **payment_subtype
        }

        return {**data}

    def get_payment_type(self, payment_type):
        subtype = 'default'
        if payment_type.startswith('CVS_'):
            subtype = 'cvs'
        elif payment_type.startswith('BARCODE_'):
            subtype = 'barcode'
        elif payment_type.startswith('ATM_'):
            subtype = 'atm'
        elif payment_type.startswith('Credit_'):
            subtype = 'credit'
        return subtype

    def map_callback_data(self, data):
        return_code = data.get('RtnCode')
        cart = self.cart
        payment_data = {
            'amount': cart['calculations']['amount'],
            'payment_status': 'success' if return_code == '1' else 'failure',
            'id': data['MerchantTradeNo'],
        }
        return payment_data

    def map_redirect_data(self, data):
        payment_type = data['PaymentType']
        code = data['RtnCode']
        payload = {
            'amount': data['TradeAmt']
        }
        if payment_type.startswith('CVS_') and code == '10100073':
            payload['payment_status'] = 'code_generated'
            payload['payment_subtype'] = 'cvs'
            payload['code_no'] = data['PaymentNo']
            payload['pay_deadline'] = data['ExpireDate']
        elif payment_type.startswith('BARCODE_') and code == '10100073':
            payload['payment_status'] = 'code_generated'
            payload['payment_subtype'] = 'barcode'
            payload['barcode_1'] = data['Barcode1']
            payload['barcode_2'] = data['Barcode2']
            payload['barcode_3'] = data['Barcode3']
            payload['pay_deadline'] = data['ExpireDate']
        elif payment_type.startswith('ATM_') and code == '2':
            payload['payment_status'] = 'code_generated'
            payload['payment_subtype'] = 'atm'
            payload['bank_code'] = data['BankCode']
            payload['bank_account'] = data['vAccount']
            payload['pay_deadline'] = datetime.strptime(data['ExpireDate'], '%Y/%m/%d')
        return payload


class CreditPayment(BasePayment):
    payment_type = 'credit'

    def map_callback_data(self, data):
        return {
            'id': self.gen_order_id(),
            **data
        }

    def checkout(self, state):
        buyer = self.buyer
        cart = self.cart
        calc = cart['calculations']
        if buyer.credit < calc['amount']:
            raise

        buyer.credit -= calc['amount']
        buyer.save()

        payload = {
            'amount': calc['amount'],
            'payment_status': 'success',
        }
        order, changed = self.callback(state, payload)
        return redirect(f'{self.WEB_HOST}/order?id={order.id}')

    def static_payment_result_page(self, order):
        return HttpResponse('<html> \
                        <head> \
                            <title>PaymentResult</title> \
                        </head> \
                        <body> \
                            <div> \
                                <h2>PaymentStatus</h2>\
                                <h3>{}</h3>\
                            </div> \
                        </body>\
                    </html>'.format(order.payment_status),
                            content_type='text/html')
