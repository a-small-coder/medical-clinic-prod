from rest_framework import serializers
from ...models import *


class ProductSerializer(serializers.ModelSerializer):

    completion_time = serializers.SerializerMethodField()
    vendor_code = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    @staticmethod
    def get_completion_time(obj):
        analyze_qs = Analyze.objects.filter(slug=obj.slug)
        if not analyze_qs:
            return None
        analyze = Analyze.objects.get(slug=obj.slug)
        return analyze.time

    @staticmethod
    def get_vendor_code(obj):
        analyze_qs = Analyze.objects.filter(slug=obj.slug)
        if not analyze_qs:
            return None
        analyze = Analyze.objects.get(slug=obj.slug)
        return analyze.vendor_code


class AnalyzeComplexForeignSerializer(serializers.ModelSerializer):
    complex_type = serializers.SerializerMethodField()

    class Meta:
        model = AnalyzeComplex
        fields = ['id', 'title', 'title_min', 'complex_type']

    @staticmethod
    def get_complex_type(obj):
        return ComplexType.objects.get(analyzecomplex=obj).complex_type


class AnalyzeComplexTopServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnalyzeComplex
        fields = ['id', 'title_min', 'preview_description', 'price', 'big_image', 'slug', 'small_image']


# complex all fields with data about analyzes, gender, and complex
class AnalyzeComplexRetrieveSerializer(serializers.ModelSerializer):
    included_analyzes = serializers.SerializerMethodField()
    complex_type = serializers.SerializerMethodField()

    class Meta:
        model = AnalyzeComplex
        fields = '__all__'

    @staticmethod
    def get_included_analyzes(obj):
        return ProductSerializer(Analyze.objects.filter(complex=obj), many=True).data

    @staticmethod
    def get_complex_type(obj):
        return ComplexType.objects.get(analyzecomplex=obj).complex_type


class AnalyzeRetrieveSerializer(serializers.ModelSerializer):

    complex = AnalyzeComplexForeignSerializer()
    search_group = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Analyze
        fields = '__all__'

    @staticmethod
    def get_search_group(obj):
        return SearchGroup.objects.get(analyze=obj).title

    @staticmethod
    def get_content(obj):
        return AnalyzeContentBlockSerializer(AnalyzeContentBlock.objects.filter(analyze=obj), many=True).data


class UnicAnalyzeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Analyze
        fields = ['id', 'title', 'preview_description', 'price', 'slug', 'small_image']


class AnalyzeContentBlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnalyzeContentBlock
        fields = ['id', 'analyze_content_category', 'title',  'text', 'pos']



