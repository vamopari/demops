from django.urls import path
from todos.views import TodoListCreateAPIView, TodoDetailAPIView
from todoapp.organization_middleware import check_api_key
app_name = 'todos'

urlpatterns = [
    path('', TodoListCreateAPIView.as_view(), name="list"),
    path('<int:pk>/', TodoDetailAPIView.as_view(), name="detail"),
]
