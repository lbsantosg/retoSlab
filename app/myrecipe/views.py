from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag
from myrecipe import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage tags in the database """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only
            When the viewset is invoked from an url it will call
            get_query_set to retrieve these objects and this is
            where we can apply any custom filtering like limiting it
            to the authenticated user so whatever we return will be
            displayed in the API
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')
