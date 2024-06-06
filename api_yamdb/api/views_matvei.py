from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from reviews.models import (
    Reviews,
    Title
)
from .permissons import AdminOrReadOnly
from .serializers import (
    ReviewsSerializer
)


class ReviewViewSetT(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AdminOrReadOnly
    )

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title=title
        )