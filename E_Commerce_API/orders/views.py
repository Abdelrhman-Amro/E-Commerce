import stripe
from cart.models import Cart, CartItem
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
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
from users.models import Address

from .models import Order, OrderItem, Payment
from .serializers import OrderItemSerializer, OrderSerializer, PaymentSerializer

CustomUser = get_user_model()

####################################################################
#################### Payment Logic&Endpoints #######################
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(user, line_items, address_id):
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=user.email,
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="http://localhost:8000/api/checkout_success/?session_id={CHECKOUT_SESSION_ID}",
            metadata={
                "user_id": user.user_id,
                "address_id": address_id,
            },
        )
        return Response({"session_url": checkout_session.url})
    except Exception as e:
        print(f"Error creating checkout session: {str(e)}")
        return Response({"error": str(e)}, status=500)


class CheckoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Create a new checkout session and return the URL
        - Logic
            - Check if address_id exists in the body of the request
            - Check if the address_id belongs to the user

            - Get user cart
            - Check if cart not empty
            - Check if cart-items clean

            - Loop over cart items and create line items for checkout session
                - Set product -> price -> quantity
            - Call create_checkout_session with arguments: user_email, line_items, address_id
        """
        #
        address_id = request.data.get("address_id")
        if not address_id:
            return Response({"error": "Address ID is required"}, status=400)

        # Get user cart & address
        address = get_object_or_404(Address, address_id=address_id, user=request.user)
        cart = get_object_or_404(Cart, user=request.user)

        # Check if cart is not empty
        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        # Check if cart items are clean call clean
        for cart_item in cart_items:
            cart_item.clean()

        # Create line items for checkout session
        line_items = []
        for cart_item in cart_items:
            line_items.append(
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": cart_item.product.name,
                        },
                        "unit_amount": int(cart_item.product.price * 100),
                    },
                    "quantity": int(cart_item.cart_item_quantity),
                }
            )
        return create_checkout_session(request.user, line_items, address_id)


@api_view(["GET"])
def checkout_success(request):
    """After Sucess Logic
    - Create new Order with order items
    - Create new payment
    - Clean Cart
    """
    session_id = request.GET.get("session_id")
    if not session_id:
        return Response({"error": "Session ID is required"}, status=400)

    try:
        session = stripe.checkout.Session.retrieve(session_id, expand=["line_items", "payment_intent"])
        user_id = session.metadata["user_id"]

        if session.payment_status != "paid":
            return Response({"error": "Payment not completed"}, status=400)

        user = get_object_or_404(CustomUser, user_id=user_id)
        address = get_object_or_404(Address, address_id=session.metadata["address_id"], user=user)
        cart = get_object_or_404(Cart, user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        total_amount = session.amount_total / 100

        with transaction.atomic():
            # step 1: create order
            order = Order.objects.create(
                user=user,
                shipping_address=address,
                status="preparing",
                total_amount=total_amount,
            )

            # step 2: create order_items -> update product stock -> delete item from cart
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    order_item_quantity=item.cart_item_quantity,
                    unit_price=item.product.price,
                )
                item.product.stock_quantity -= item.cart_item_quantity
                item.product.save()
                item.delete()

            # step 3: Create Payment
            Payment.objects.create(
                order=order,
                amount=total_amount,
                status="completed",
            )

        return Response({"message": "Checkout successful", "order_id": order.order_id}, status=200)
    except stripe.error.StripeError as e:
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


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
