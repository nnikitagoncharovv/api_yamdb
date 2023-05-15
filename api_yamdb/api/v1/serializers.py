from audioop import avg
import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), required=False, many=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')
        
    def get_year(self, obj):
        return dt.datetime.now().year - obj.year



class TitleRetriveSerializer(serializers.ModelSerializer):
#    rating = serializers.SerializerMethodField(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category')  # 'rating'
        
#    def get_rating(self, obj):
#        rate = obj.reviews.aggregate(rating=Avg('score'))
#        if not rate['rating']:
#            return None
#        return int(rate['rating'])
