from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

from .utils import *
from ..models import *
from .serializers.Navigation import *
from .serializers.Other import *
from ..models import *


class NavigationCategoryViewSet(viewsets.ModelViewSet):

    queryset = NavigationCategory.objects.all()
    serializer_class = NavigationCategorySerializer

    action_to_serializer = {
        "list": NavigationCategoryDetailSerializer,
        "retrieve": NavigationCategoryDetailSerializer,
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )


class SubNavigationCategoryViewSet(viewsets.ModelViewSet):

    queryset = SubNavigationCategory.objects.all()
    serializer_class = SubNavigationCategorySerializer

    action_to_serializer = {
        "list": SubNavigationCategoryRetrieveSerializer,
        "retrieve": SubNavigationCategoryRetrieveSerializer
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )


class CatalogPagination(PageNumberPagination):

    page_size = 4
    page_size_param = 'page_size'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total_count', self.page.paginator.count),
            ('page_size', self.page_size),
            ('current_page', self.page.number),
            ('items', data)
        ]))


class AboutUsCategoryViewSet(viewsets.ModelViewSet):

    queryset = AboutUsCategory.objects.all()
    serializer_class = AboutUsCategorySerializer


class OurAchievementsViewSet(viewsets.ModelViewSet):

    queryset = OurAchievements.objects.filter(in_archive=False)
    serializer_class = OurAchievementsSerializer


class UserView(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=False, url_path='user-data')
    def get_user_data(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            token_key = Token.objects.get(user=user).key
            is_anon = user.username == f'unknown{user.id}'
        else:
            user, token_key = create_new_anon()
            customer = Customer.objects.create(user=user)
            Cart.objects.create(owner=customer, for_anonymous_user=True)
            is_anon = True
        return response.Response({'user': UserSerializer(user).data, 'is_anon': is_anon, 'token': token_key})

    @action(methods=['post'], detail=False, url_path='update_user_data')
    def update_user_date(self, *args, **kwargs):
        user = self.request.user
        customer = Customer.objects.get(user=user)
        customer.first_name = self.request.data['firstName']
        customer.second_name = self.request.data['secondName']
        customer.father_name = self.request.data['fatherName']
        customer.address = self.request.data['adress']
        customer.phone = self.request.data['phoneNumber']
        customer.save()
        user.customer = customer
        user.save()
        return response.Response({'detail': 'success'})

    @action(methods=['post'], detail=False, url_path='change_password')
    def change_password(self, *args, **kwargs):
        user = self.request.user
        user.set_password(self.request.data['password'])
        return response.Response({'detail': 'success'})


class RegisterView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]

    @action(methods=['post'], detail=False)
    def register_user(self, *args, **kwargs):

        userEmail = self.request.data['email']

        user = User.objects.filter(email=userEmail)
        if not user:
            user_id = User.objects.all().last().id
            userfirstname = self.request.data['firstName']
            userlastname = self.request.data['secondName']
            fatherName = self.request.data['fatherName']
            username = f'Пользователь _{user_id}'
            new_user = User.objects.create(
                username=username,
                email=userEmail
            )
            new_user.save()
            new_user.set_password(self.request.data['password'])
            new_user.save()
            customer = Customer.objects.create(
                user=new_user,
                first_name=userfirstname,
                second_name=userlastname,
                father_name=fatherName
            )
            Cart.objects.create(owner=customer)
            Token.objects.get_or_create(user=new_user)
            return response.Response({'detail': 'User successfully register', 'username': username}, status=status.HTTP_200_OK)
        return response.Response({'detail': 'Email уже привязан к другому аккаунту'}, status=status.HTTP_400_BAD_REQUEST)


class OrderView(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(methods=['post'], detail=False, url_path='create')
    def create_order(self, *args, **kwargs):
        customer = Customer.objects.get(user=self.request.user)
        cart_id = self.request.data['cart_id']
        cart = Cart.objects.get(pk=cart_id)
        place_type_key = int(self.request.data['place_type'])  # 0 or 1
        place_type = ADDRESS_TYPE[place_type_key][0]
        place = self.request.data['customer']['address']
        if place_type_key == 0:
            email = self.request.user.email
            full_name = customer.get_full_name
            phone = customer.phone
        else:
            email = self.request.data['customer']['email']
            full_name = self.request.data['customer']['fullName']
            phone = self.request.data['customer']['phone']
        cart.put_in_order()
        Order.objects.create(
            customer=customer,
            cart=cart,
            place_type=place_type,
            place=place,
            email=email,
            customer_full_name=full_name,
            phone=phone
        )
        Cart.objects.create(owner=customer)
        return response.Response({'detail': 'success'}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='current_user_orders')
    def get_user_orders(self, *args, **kwargs):
        customer = Customer.objects.get(user=self.request.user)
        orders = Order.objects.filter(customer=customer)
        if orders:
            return response.Response(OrderSerializer(orders, many=True).data)
        return response.Response({'detail': 'Current user has no orders'}, status=status.HTTP_204_NO_CONTENT)
