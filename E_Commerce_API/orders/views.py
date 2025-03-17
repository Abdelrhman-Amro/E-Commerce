import stripe
from django.conf import settings
from rest_framework import generics, views, viewsets
from rest_framework.decorators import (
    action,
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Order, OrderItem, Payment
from .serializers import OrderItemSerializer, OrderSerializer, PaymentSerializer

####################################################################
#################### Payment Logic&Endpoints #######################
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(user):
    try:

        checkout_session = stripe.checkout.Session.create(
            billing_address_collection="required",
            # customer_email="customer@example.com",
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "T-shirt",
                        },
                        "unit_amount": 2000,
                    },
                    "quantity": 1,
                },
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "T-shirtxxx",
                        },
                        "unit_amount": 2000,
                    },
                    "quantity": 3,
                },
            ],
            mode="payment",
            success_url="http://localhost:8000/api/checkout_success?session_id={CHECKOUT_SESSION_ID}&address_id={address_id}",
            cancel_url="http://localhost:8000/",
        )
        return Response({"session_url": checkout_session.url})
    except Exception as e:
        print(f"Error creating checkout session: {str(e)}")
        # return str(e)
        return Response({"error": str(e)}, status=500)


class CheckoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Create a new checkout session and return the URL
        """

        return create_checkout_session(request.user)


@api_view(["GET"])
def checkout_success(request):
    """After Sucess Logic
    - Create new Order with order items
    - Clean Cart
    """
    print(request.GET)
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id, expand=["line_items"])
    print(session)
    return Response({"message": "Checkout Success"})


############################################################
#################### Order Endpoints #######################
class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# Order Update and Retrieve
class OrderRetrieveView(generics.RetrieveAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs.get("order_id")
        return OrderItem.objects.filter(order_id=order_id)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
