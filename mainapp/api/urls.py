from django.urls import path
from rest_framework import routers

from .AnalyzeView import *
from .OtherViews import *
from .CartView import *
from .AnalyzesComplexView import *

router = routers.SimpleRouter()
router.register('navigation', NavigationCategoryViewSet, basename='navigation')
router.register('subNavigation', SubNavigationCategoryViewSet, basename='subNavigation')
router.register('best-products', ComplexAnalyzesTopServicesViewSet, basename='best-products')
router.register('best-complex-analyzes', ComplexAnalyzesTopFiveViewSet, basename='best-complex-analyzes')
# router.register('stocks', , basename='stocks')
router.register('about-us', AboutUsCategoryViewSet, basename='about-us')
router.register('catalog/all', ProductsView, basename='all-products')
router.register('catalog/all-analyzes', AnalyzesView, basename='all-analyzes')
router.register('catalog/unic-analyzes', UnicAnalyseViewSet, basename='unic-analyzes')
router.register('catalog/complex-analyzes', ComplexesView, basename='all-complexes')
router.register('analyze-content', AnalyzeContentBlockViewSet, basename='analyze-content-block')
router.register('cart', CartViewSet, basename='cart')
router.register('achievements', OurAchievementsViewSet, basename='achievements')
router.register('auth/users', UserView, basename='users')
router.register('auth/register', RegisterView, basename='registration')
router.register('orders', OrderView, basename='order')
urlpatterns = []
urlpatterns += router.urls
