from rest_framework import filters, viewsets, renderers
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Issue, IssueLemma, LemmaStatus
from .serializers import (
    AuthorSerializer,
    EditorSerializer,
    IssueSerializer,
    IssueLemmaSerializer,
    LemmaStatusSerializer,
)


class AuthorViewset(viewsets.ReadOnlyModelViewSet):
    """Viewset to retrieve Author objects"""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filterset_fields = ["username"]
    permission_classes = [IsAuthenticated]


class IssueViewset(viewsets.ModelViewSet):

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    filter_fields = ["name", "pubDate"]
    permission_classes = [IsAuthenticated]


class IssueLemmaViewset(viewsets.ModelViewSet):

    queryset = IssueLemma.objects.all()
    serializer_class = IssueLemmaSerializer
    filter_fields = ["lemma", "issue", "author", "editor"]
    permission_classes = [IsAuthenticated]


class LemmaStatusViewset(viewsets.ModelViewSet):

    queryset = LemmaStatus.objects.all()
    serializer_class = LemmaStatusSerializer
    filter_fields = ["issuelemma"]
    permission_classes = [IsAuthenticated]