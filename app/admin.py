from django.contrib import admin
from .models import Category,Product,Image
# Register your models here.

@admin.register(Category)
class CategoryMOdelAdmin(admin.ModelAdmin):
    list_display = ['title','slug']
    prepopulated_fields = {'slug':('title',)}


@admin.register(Product)
class CategoryMOdelAdmin(admin.ModelAdmin):
    list_display = ['name','price']


admin.site.register(Image)
