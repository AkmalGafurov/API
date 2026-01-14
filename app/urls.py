from django.urls import path
from .views import (
    ParentCategoryListApiView,
    ChildrenCategoryByCategorySlug,
    CategoryListCreateView,
    CategoryDetailView,
    ProductListCreateView,
    ProductDetailView,
    ProductViewSet,
)

urlpatterns = [
    path('apelsin.uz/', ParentCategoryListApiView.as_view()),
    path('apelsin.uz/category/<slug:slug>/',ChildrenCategoryByCategorySlug.as_view()),
    path('categories/', CategoryListCreateView.as_view()),
    path('categories/<int:pk>/', CategoryDetailView.as_view()),
    path('products/', ProductListCreateView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),
    path('products/<int:pk>/', ProductViewSet.as_view(), name='product-detail'),
]



