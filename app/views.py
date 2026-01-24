from rest_framework import generics
from rest_framework.generics import ListAPIView
from .serializer import ParentCategoryModelSreializer,CategorySerializer
from .models import Category,Product
from .serializer import CategorySerializer, ProductSerializer
from rest_framework.permissions import BasePermission
from .permissions import CanUpdate4Hours
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.cache import cache



class ParentCategoryListApiView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        cache_key = "parent_categories_active"
        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = Category.objects.filter(
                parent__isnull=True,
                is_active=True
            ).prefetch_related('children')
            cache.set(cache_key, queryset, 60 * 10)  

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context



class ChildrenCategoryByCategorySlug(ListAPIView):
    serializer_class = ParentCategoryModelSreializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        cache_key = f"children_category_{slug}"

        children = cache.get(cache_key)
        if children is None:
            category = Category.objects.filter(slug=slug).first()
            if not category:
                return Category.objects.none()

            children = category.children.all()
            cache.set(cache_key, children, 60 * 10)

        return children

    


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
    serializer_class = ProductSerializer

    def get_queryset(self):
        cache_key = "product_list"
        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = Product.objects.select_related('category').prefetch_related('images')
            cache.set(cache_key, queryset, 60 * 5)

        return queryset




class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.prefetch_related('images')

    def get_object(self):
        pk = self.kwargs['pk']
        cache_key = f"product_detail_{pk}"

        product = cache.get(cache_key)
        if product is None:
            product = super().get_object()
            cache.set(cache_key, product, 60 * 5)  

        return product



class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {"detail": "Logout bajarildi"},
            status=status.HTTP_200_OK
        )