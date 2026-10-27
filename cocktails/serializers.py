from rest_framework import serializers
from .models import Ingredient, Cocktail, CocktailIngredient
from .models import Review

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'description', 'is_alcoholic', 'image_url']


class CocktailIngredientSerializer(serializers.ModelSerializer):
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredient'
    )
    ingredient_name = serializers.ReadOnlyField(source='ingredient.name')

    class Meta:
        model = CocktailIngredient
        fields = ['ingredient_id', 'ingredient_name', 'amount']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'user', 'cocktail', 'rating', 'comment', 'created_at']


class CocktailSerializer(serializers.ModelSerializer):
    recipe_ingredients = CocktailIngredientSerializer(many=True)
    author = serializers.ReadOnlyField(source='author.username')
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Cocktail
        fields = ['id', 'name', 'category', 'instruction', 'author','average_rating', 'recipe_ingredients', 'created_at']

    def get_creator_info(self, obj):
        if not obj.author:
            return "Stworzone przez aplikację"
        if obj.author.is_superuser or obj.author.is_staff:
            return f"Stworzone przez admina: {obj.author.username}"
        return f"Stworzone przez użytkownika: {obj.author.username}"

    def validate_recipe_ingredients(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError("Koktajl musi zawierać przynajmniej jeden składnik")
        return value

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        cocktail = Cocktail.objects.create(**validated_data)
        for item in ingredients_data:
            CocktailIngredient.objects.create(cocktail=cocktail, **item)
        return cocktail

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients', None)
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.instruction = validated_data.get('instruction', instance.instruction)
        instance.save()

        if ingredients_data is not None:
            instance.recipe_ingredients.all().delete()
            for item in ingredients_data:
                CocktailIngredient.objects.create(cocktail=instance, **item)

        return instance