from rest_framework.generics import ListAPIView
from .serializer import ParentCategoryModelSreializer,CategorySerializer
from .models import Category

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
