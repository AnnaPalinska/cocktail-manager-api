from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ingredient, Cocktail, Review
from .serializers import IngredientSerializer, CocktailSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from django.db.models import Avg


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all().order_by('name')
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_alcoholic']
    search_fields = ['name']


class CocktailViewSet(viewsets.ModelViewSet):
    queryset = Cocktail.objects.annotate(
        average_rating=Avg('reviews__rating')
    ).prefetch_related('recipe_ingredients__ingredient').order_by('-created_at')
    serializer_class = CocktailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'ingredients__name', 'author__username']
    search_fields = ['name', 'instruction']
    ordering_fields = ['name', 'created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)