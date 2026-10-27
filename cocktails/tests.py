from django.test import TestCase

# Create your tests here.

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Cocktail, Ingredient


class CocktailAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123')
        self.ingredient = Ingredient.objects.create(
            name='Wódka',
            description='Mocny alkohol',
            is_alcoholic=True,
            image_url ='https://images.unsplash.com/photo-1550985543-f47f38aeee65?q=80&w=735&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=NHwxMjA3fDA%3D'
        )
        self.cocktails_url = '/api/cocktails/'

#Proba dodania koktajlu przez niezalogowanego uzytkownika
    def test_create_cocktail_unauthenticated(self):
        data = {
            "name": "Niedozwolony Koktajl",
            "category": "Sour",
            "instruction": "Wymieszaj i przelej",
            "recipe_ingredients": [{"ingredient_id": self.ingredient.id, "amount": "50ml"}]
        }
        response = self.client.post(self.cocktails_url, data, format='json')

        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertEqual(Cocktail.objects.count(), 0)

    def test_create_cocktail_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "Wódka Sour",
            "category": "Sour",
            "instruction": "Wstrząśnij z lodem",
            "recipe_ingredients": [{"ingredient_id": self.ingredient.id, "amount": "50ml"}]
        }
        response = self.client.post(self.cocktails_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cocktail.objects.count(), 1)
        self.assertEqual(Cocktail.objects.get().author, self.user)

#Sprawdzanie filtrow
    def test_filter_cocktails_by_category(self):
        Cocktail.objects.create(name="Margarita", category="Sour", instruction="...", author=self.user)
        Cocktail.objects.create(name="Martini", category="Dry", instruction="...", author=self.user)

        response = self.client.get(self.cocktails_url + '?category=Sour')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Margarita')
