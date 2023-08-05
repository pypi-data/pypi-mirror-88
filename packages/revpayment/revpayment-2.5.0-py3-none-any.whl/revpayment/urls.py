from rest_framework import routers
from .views import CartViewSet, CheckoutView, CallbackView, ClientRedirect, CartView, AddItemView, EditItemView, EditConfigView, DeleteItemView, ClearCartView, CreditView
from revpayment.logistics.views import LogisticCallBack, SelectCVS, CVSCallback
from django.urls import path

router = routers.DefaultRouter(trailing_slash=False)
router.register('cart', CartViewSet, basename='cart')
cart_urls = router.urls

checkout_urlpatterns = [
    path('checkout', CheckoutView.as_view(), name='payment-checkout'),
    path('callback', CallbackView.as_view(), name='payment-callback'),
    path('redirect', ClientRedirect.as_view(), name='payment-redirect'),
    path('credit', CreditView.as_view(), name='payment-credit'),
    path('logistics/callback', LogisticCallBack.as_view(), name='logistic-callback'),
    path('logistics/cvs/select', SelectCVS.as_view(), name='logistic-cvs-select'),
    path('logistics/cvs/callback', CVSCallback.as_view(), name='logistic-cvs-callback'),
]

cart_urlpatterns = [
    path('', CartView.as_view(), name='cart-get'),
    path('clear', ClearCartView.as_view(), name='cart-clear'),
    path('item/add', AddItemView.as_view(), name='cart-add-item'),
    path('item/edit', EditItemView.as_view(), name='cart-edit-item'),
    path('item/delete', DeleteItemView.as_view(), name='cart-delete-item'),
    path('config/edit', EditConfigView.as_view(), name='cart-edit-config'),
]
