from rest_framework import viewsets

from reviews.models import (
    Category, Genre, Title, Reviews, Comment
)


class AuthViewSet(viewsets.ModelViewSet):
    pass


# class UserViewSet(viewsets.ModelViewSet):


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
