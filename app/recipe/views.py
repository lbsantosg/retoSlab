from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient
from recipe import serializers


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """
        Manage tags in the database
        You can add mixins to customize the fucntionality that is
        available for our viewset so you don't have to do the
        standartd model viweset and accept everything because there
        might be some cases where you don't want to allow users to
        do everything and you don't need that feature so ther's no
        point implementing it. So, you can customize it by adding the
        mixins for what you want to do.
    """
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

    def perform_create(self, serializer):
        """
            Create new tag.
            When we do a create object in our viewset this function will
            be invoked and the validated serializer will be in as a serializer
            argument and then we can perform any modifications here that
            we'd like to in our create process.
        """
        serializer.save(user=self.request.user)

class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage ingredients in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')