from django.contrib import admin
from .models import Stock, Theme, StockTheme

admin.site.register(Stock)
admin.site.register(Theme)
admin.site.register(StockTheme)