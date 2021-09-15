from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(NavigationCategory)
admin.site.register(SubNavigationCategory)
admin.site.register(ComplexType)
admin.site.register(AnalyzeComplex)
admin.site.register(SearchGroup)
admin.site.register(Analyze)
admin.site.register(AnalyzeContentBlock)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(AboutUsCategory)
admin.site.register(AboutUsContentBlock)
admin.site.register(OurAchievements)
admin.site.register(Order)