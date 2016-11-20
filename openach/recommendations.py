"""Analysis of Competing Hypotheses Django Application RecommendationProvider Implementation.

This uses the django-recommends recommendation engine

For more information, please see:
    https://django-recommends.readthedocs.io/en/latest/
"""
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from recommends.providers import RecommendationProvider
from recommends.providers import recommendation_registry
from .models import Board, Evaluation


class BoardRecommendationProvider(RecommendationProvider):
    """ A class that specifies how to retrieve the various informations for recommendations and similarities"""

    @classmethod
    def get_users(self):
        """ Return all users with evaluations."""
        return User.objects.filter(is_active=True, evaluations__isnull=False).distinct()

    @classmethod
    def get_items(self):
        """ Return items that have been evaluated."""
        return Board.objects.all()

    @classmethod
    def get_ratings(self, obj):
        """ Return all ratings (evaluations) for given item."""
        return Evaluation.objects.filter(board=obj)

    @classmethod
    def get_rating_score(self, rating):
        """ Return the rating score (evaluation value)."""
        return rating.value

    @classmethod
    def get_rating_site(self, rating):
        """ Return the site of the rating."""
        return Site.objects.get_current()

    @classmethod
    def get_rating_user(self, rating):
        """ Return the user who performed the rating (evaluation)."""
        return rating.user

    @classmethod
    def get_rating_item(self, rating):
        """ Return the rated (evaluated) object."""
        return rating.board

recommendation_registry.register(Evaluation, [Board], BoardRecommendationProvider)
