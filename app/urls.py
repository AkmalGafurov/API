from django.urls import path
from .views import ParentCategoryListApiView,ChildrenCategoryByCategorySlug

urlpatterns = [
    path('apelsin.uz/', ParentCategoryListApiView.as_view()),
    path('apelsin.uz/category/<slug:slug>/',ChildrenCategoryByCategorySlug.as_view()),
]



