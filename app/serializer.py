from rest_framework import serializers
from .models import Category


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
        fields = (
            'id',
            'title',
            'slug',
            'image',
            'parent',
            'parent_title',
            'children',
        )

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_parent_title(self, obj):
        return obj.parent.title if obj.parent else None
