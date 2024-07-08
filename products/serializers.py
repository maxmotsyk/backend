from django.db.models import Avg
from rest_framework import serializers
from .models import Product, ProductDetail, ProductVariation, ProductImage, RecommendProduct
from reviews.models import Review


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = ['id', 'name', 'icon', 'description']


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ['id', 'description', 'img']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'message', 'rating_stars', 'created_by', 'creator_img', 'img']


class RecommendProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendProduct
        fields = ['id', 'name', 'description', 'img', 'price']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    details = ProductDetailSerializer(many=True, read_only=True, source='productdetail_set')
    variations = ProductVariationSerializer(many=True, read_only=True, source='productvariation_set')
    reviews = ReviewSerializer(many=True, read_only=True, source='review_set')
    avg_rating_stars = serializers.SerializerMethodField()
    recommend_products = RecommendProductSerializer(many=True, read_only=True)


    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'discount', 'images',
            'details', 'variations', 'reviews', 'avg_rating_stars', 'recommend_products'
        ]

    def get_avg_rating_stars(self, obj):
        average_rating = Review.objects.filter(product=obj).aggregate(Avg('rating_stars'))['rating_stars__avg']
        return int(average_rating) if average_rating is not None else 0
