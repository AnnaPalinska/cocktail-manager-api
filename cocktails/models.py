from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_alcoholic = models.BooleanField(default=False)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class Cocktail(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    instruction = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cocktails', null=True, blank=True
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='CocktailIngredient', related_name='cocktails'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CocktailIngredient(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='used_in_cocktails')
    amount = models.CharField(max_length=100, help_text="np. 50ml, szczypta")

    class Meta:
        unique_together = ('cocktail', 'ingredient')

    def __str__(self):
        return f"{self.amount} - {self.ingredient.name} w {self.cocktail.name}"


class Review(models.Model):
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #Użytkownik może wystawic tylko 1 ocene dla koktajlu
        unique_together = ('cocktail', 'user')

    def __str__(self):
        return f"{self.user.username} ocenił {self.cocktail.name} na {self.rating}"