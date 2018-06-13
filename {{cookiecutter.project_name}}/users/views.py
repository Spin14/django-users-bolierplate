from rest_framework import views, permissions, mixins, viewsets, status
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import UserCreationSerializer, UserSerializer
from .permissions import IsUser


class CreateUserViewSet(views.APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserCreationSerializer

    def post(self, request, *args, **kwargs):
        views.Response(status=status.HTTP_200_OK)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                data = serializer.data
                data['token'] = token.key
                return views.Response(data, status=status.HTTP_201_CREATED)

        return views.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    model_class = User
    serializer_class = UserSerializer
    permission_classes = (IsUser, )

    lookup_field = 'username'

    queryset = model_class.objects.all()
