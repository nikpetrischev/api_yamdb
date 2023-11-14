from permissions import CommentPermission, ReviewPermission
from serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review
from rest_framework import viewsets


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReviewPermission,)

    def get_queryset(self):
        queryset = Review.objects.filter(post=self.kwargs['review_id'])
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (CommentPermission,)

    # def get_queryset(self):
    #     queryset = Comment.objects.filter(post=self.kwargs['post_id'])
    #     return queryset

    def perform_create(self, serializer):
        # title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        # review = get_object_or_404(Review, pk=self.kwargs['title_id'])
        # serializer.save(author=self.request.user, title=title, review=review)
