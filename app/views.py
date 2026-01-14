from rest_framework import generics
from rest_framework.generics import ListAPIView
from .serializer import ParentCategoryModelSreializer,CategorySerializer
from .models import Category,Product
from .serializer import CategorySerializer, ProductSerializer
from rest_framework.permissions import BasePermission
from .permissions import CanUpdate4Hours
from rest_framework.viewsets import ModelViewSet

class ParentCategoryListApiView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = ParentCategoryModelSreializer

    def get_queryset(self):
        queryset = Category.objects.filter(parent__isnull = True)
        return queryset


class ChildrenCategoryByCategorySlug(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = ParentCategoryModelSreializer


    def get_queryset(self):
        category_slug = self.kwargs['slug']
        queryset = Category.objects.filter(slug=category_slug).first()
        if not queryset:
            return Category.objects.none()
        return queryset.children.all()
    


class ParentCategoryListApiView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(
            parent__isnull=True,
            is_active=True
        ).prefetch_related('children')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ProductViewSet(generics.RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CanUpdate4Hours]



class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related('category').prefetch_related('images')
    serializer_class = ProductSerializer



class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.prefetch_related('images')
    serializer_class = ProductSerializer