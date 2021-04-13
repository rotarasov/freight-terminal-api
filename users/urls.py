from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('', views.UserListCreateAPIView.as_view(), name='list'),
    path('<int:pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='detail'),
]