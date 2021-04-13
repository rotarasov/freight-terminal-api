from django.urls import path

from devices import views

app_name = 'devices'

urlpatterns = [
    path('', views.DeviceListCreateAPIView.as_view(), name='list'),
    path('<int:pk>/', views.DeviceRetrieveUpdateDestroyAPIView.as_view(), name='detail')
]