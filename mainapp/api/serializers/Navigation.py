from rest_framework import serializers

from...models import (
    NavigationCategory, SubNavigationCategory,
    )


class NavigationCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = NavigationCategory
        fields = '__all__'


class NavigationCategoryDetailSerializer(serializers.ModelSerializer):

    sub_categories = serializers.SerializerMethodField()
    spoilerActive = serializers.SerializerMethodField()

    class Meta:
        model = NavigationCategory
        fields = '__all__'

    @staticmethod
    def get_sub_categories(obj):
        return SubNavigationCategorySerializer(SubNavigationCategory.objects.filter(navigation_category=obj), many=True).data

    @staticmethod
    def get_spoilerActive(obj):
        return False


class SubNavigationCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubNavigationCategory
        fields = '__all__'


class SubNavigationCategoryRetrieveSerializer(serializers.ModelSerializer):

    navigation_category = NavigationCategorySerializer()

    class Meta:
        model = SubNavigationCategory
        fields = '__all__'