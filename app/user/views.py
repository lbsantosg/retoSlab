from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """
        Create a new auth token for user.
        If you are authenticating using an username and password as
        standard, it's very easy to just switch this on, you just pass
        in the ObtainAuthToken view directly into our URLs. Because we
        are customizing it slightly we need to just basically import it
        into our views and then extend it within a class and then make
        a few modifications to the class variables. The render class set
        us the render so we can view this endpoint in the browser.
    """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return auth user"""
        return self.request.user
