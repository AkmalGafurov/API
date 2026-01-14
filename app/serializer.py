from rest_framework import serializers
from .models import Category,Product, Image



class ParentCategoryModelSreializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ()


class ChildCategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'slug',
            'image',
        )

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class CategorySerializer(serializers.ModelSerializer):
    children = ChildCategorySerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    parent_title = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'slug',
            'image',
            'parent',
            'parent_title',
            'is_active',
            'children'
        ]

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_parent_title(self, obj):
        return obj.parent.title if obj.parent else None


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True) 
    image_count = serializers.SerializerMethodField()    

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'images', 'image_count']

    def get_image_count(self, obj):
        return obj.images.count()