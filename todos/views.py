from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from todos.models import Todo
from todos.permissions import UserIsOwnerTodo
from todos.serializers import TodoSerializer


class TodoListCreateAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    authentication_classes = [OAuth2Authentication]
    def get_queryset(self):
        import pdb
        pdb.set_trace()
        return Todo.objects.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
