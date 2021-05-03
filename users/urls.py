from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users import views

app_name = 'users'

urlpatterns = [
    path('', views.UserListCreateAPIView.as_view(), name='list'),
    path('<int:pk>/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name='detail'),
    path('token/', views.CustomTokenObtainPairAPIView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]