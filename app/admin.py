from django.contrib import admin
from .models import Category
# Register your models here.

@admin.register(Category)
class CategoryMOdelAdmin(admin.ModelAdmin):
    list_display = ['title','slug']
    prepopulated_fields = {'slug':('title',)}