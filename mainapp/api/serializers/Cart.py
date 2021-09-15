from rest_framework import serializers

from .Analyzes import *


class CustomerSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = '__all__'

    @staticmethod
    def get_user(obj):
        first_name, last_name = obj.user.first_name, obj.user.last_name
        if not (first_name and last_name):
            return obj.user.username
        return ' '.join([first_name, last_name])


class CartItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'qty', 'final_price']


class CartSerializer(serializers.ModelSerializer):

    products = serializers.SerializerMethodField()
    owner = CustomerSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'products', 'qty', 'total_price', 'for_anonymous_user', 'owner', 'in_order']

    @staticmethod
    def get_products(obj):
        return CartItemSerializer(CartItem.objects.filter(cart=obj), many=True).data
