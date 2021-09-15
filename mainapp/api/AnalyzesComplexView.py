# from rest_framework import viewsets, response, status
#
# from .OtherViews import CatalogPagination
# from .serializers.Analyzes import AnalyzeComplexSerializer, AnalyzeComplexTopServicesSerializer
# from ..models import (
#     AnalyzeComplex,
# )
#
#
# class ComplexAnalyzesViewSet(viewsets.ModelViewSet):
#     queryset = AnalyzeComplex.objects.all()
#     serializer_class = AnalyzeComplexSerializer
#     pagination_class = CatalogPagination
#
#
# class ComplexAnalyzesTopServicesViewSet(viewsets.ModelViewSet):
#     queryset = AnalyzeComplex.objects.filter(on_main_page=True)
#     serializer_class = AnalyzeComplexTopServicesSerializer
#
#
# class ComplexAnalyzesTopFiveViewSet(viewsets.ModelViewSet):
#     queryset = AnalyzeComplex.objects.filter(in_top_five_list=True)
#     serializer_class = AnalyzeComplexTopServicesSerializer
