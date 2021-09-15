import math
from collections import OrderedDict

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, response, status, filters
from rest_framework.decorators import action
from django.core.paginator import Paginator
from .OtherViews import CatalogPagination
from .serializers.Analyzes import *
from .utils import *
from ..models import *


class ProductsView(viewsets.ModelViewSet):

    queryset = Product.objects.order_by('price')
    serializer_class = ProductSerializer
    pagination_class = CatalogPagination

    @action(methods=['get'], detail=False, url_path='product/(?P<product_id>\d+)')
    def get_product_by_id(self, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['product_id'])
        analyze_qs = Analyze.objects.filter(slug=product.slug)
        if not analyze_qs:
            complex_qs = AnalyzeComplex.objects.filter(slug=product.slug)
            if not complex_qs:
                return response.Response(status=status.HTTP_404_NOT_FOUND)
            return response.Response(AnalyzeComplexRetrieveSerializer(complex_qs[0]).data)
        return response.Response(AnalyzeRetrieveSerializer(analyze_qs[0]).data)

    @action(methods=['post'], detail=False, url_path='filter')
    def get_complex_with_filter(self, *args, **kwargs):
        filter_choices = json.loads(self.request.data['data'])
        print(filter_choices)
        items = []
        for filter_choice in filter_choices:
            print(filter_choice)
            if filter_choice['category'] == 'complex_type':
                items.extend(get_complexes_by_type(filter_choice['categories']))
                # print('\n\n', qss, '\n\n')

            if filter_choice['category'] == 'search_group':
                items.extend(get_analyzes_by_search_group(filter_choice['categories']))
        try:
            page_number = self.request.data['page_number']
        except:
            page_number = 1
        page_size = 4
        # max_page_size = 50
        total_count = math.ceil(len(items) / page_size)

        return response.Response(OrderedDict([
            ('total_count', total_count),
            ('page_size', page_size),
            ('current_page', page_number),
            ('items', items)
        ]))


class ComplexesView(viewsets.ModelViewSet):
    queryset = AnalyzeComplex.objects.order_by('price')
    serializer_class = AnalyzeComplexRetrieveSerializer
    pagination_class = CatalogPagination

    action_to_serializer = {
        "list": ProductSerializer,
        "retrieve": AnalyzeComplexRetrieveSerializer
    }

    def get_serializer_class(self):
        print(self.action)
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )


class ComplexAnalyzesTopServicesViewSet(viewsets.ModelViewSet):
    queryset = AnalyzeComplex.objects.filter(on_main_page=True)
    serializer_class = AnalyzeComplexTopServicesSerializer


class ComplexAnalyzesTopFiveViewSet(viewsets.ModelViewSet):
    queryset = AnalyzeComplex.objects.filter(in_top_five_list=True)
    serializer_class = AnalyzeComplexTopServicesSerializer


class AnalyzesView(viewsets.ModelViewSet):
    queryset = Analyze.objects.order_by('price')
    serializer_class = AnalyzeRetrieveSerializer
    pagination_class = CatalogPagination

    action_to_serializer = {
        "list": ProductSerializer,
        "retrieve": AnalyzeRetrieveSerializer
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )


class UnicAnalyseViewSet(viewsets.ModelViewSet):

    queryset = Analyze.objects.filter(is_unic=True)
    serializer_class = AnalyzeRetrieveSerializer
    pagination_class = CatalogPagination

    action_to_serializer = {
        "list": UnicAnalyzeListSerializer,
        "retrieve": AnalyzeRetrieveSerializer
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )


class AnalyzeContentBlockViewSet(viewsets.ModelViewSet):

    queryset = AnalyzeContentBlock.objects.all()
    serializer_class = AnalyzeContentBlockSerializer
