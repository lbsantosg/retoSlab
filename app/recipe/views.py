from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe
from recipe import serializers


"""
    Return objects for the current authenticated user only.
    Manage attributes forn recipes in the db.
    You can add mixins to customize the functionality that is
    available for our viewset so you don't have to do the
    standard model viweset and accept everything because there
    might be some cases where you don't want to allow users to
    do everything and you don't need that feature so ther's no
    point implementing it. So, you can customize it by adding the
    mixins for what you want to do.
"""


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
            Return objects for the current authenticated user only
            When the viewset is invoked from an url it will call
            get_query_set to retrieve these objects and this is
            where we can apply any custom filtering like limiting it
            to the authenticated user so whatever we return will be
            displayed in the API
        """
        queryset = self.queryset
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', default=0))
        )
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()

    def perform_create(self, serializer):
        """
            Create a new object
            When we do a create object in our viewset this function will
            be invoked and the validated serializer will be in as a serializer
            argument and then we can perform any modifications here that
            we'd like to in our create process.
        """
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Convert a list of string id's to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredients_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredients_ids)
        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """
            This is the function that is called to retrieve the
            serializer class for a particular request. Is this
            funciton that you would use if you wanted to change
            the serializer class for the different actions that
            are available on the recipe viewset.
        """
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    # You can define actions in the viewset, by default it has:
    # get_query_set, get_serializer_class and perform_create. These
    # are all default actions that we override so if we didn't
    # override them then they will just perform the default action
    # that the Django rest framework does. You can actually add
    # custom functions and define them as custom actions by using
    # the @action decorator.

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
