from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework import renderers


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):  #the data for this is not avaibale in the payload, we extract it from the request object, so we explicitly define how it should be written in. or else client can just lie about the owner in the payload lol
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = SnippetSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(["GET"])
def api_root(request, format = None):
    return Response(
        {"users": reverse("user-list", request = request, format = format),
        "snippets": reverse("snippet-list", request = request, format = format)}
    )

class Highlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)