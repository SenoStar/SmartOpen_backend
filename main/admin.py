from django.contrib import admin

from .models import Product, Cooperation, Korzina, ProductKorzina

admin.site.register(Product)
admin.site.register(Cooperation)
admin.site.register(Korzina)
admin.site.register(ProductKorzina)