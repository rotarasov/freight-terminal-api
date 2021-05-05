from django.urls import path

from companies import views

app_name = 'companies'

urlpatterns = [
    path('', views.CompanyListCreateAPIView.as_view(), name='list'),
    path('types/', views.GetCompanyTypesAPIVIew.as_view(), name='types'),
    path('<int:pk>/', views.CompanyRetrieveUpdateDestroyAPIView.as_view(), name='detail'),
    path('<int:pk>/robots/', views.RobotListCreateAPIView.as_view(), name='robot-list'),
    path('<int:company_pk>/robots/<int:robot_pk>/', views.RobotRetrieveUpdateDestroyAPIView.as_view(),
         name='robot-detail'),
    path('<int:company_pk>/robots/<int:robot_pk>/services/', views.ServiceListCreateAPIView.as_view(),
         name='service-list'),
    path('<int:company_pk>/robots/<int:robot_pk>/services/<int:service_pk>/',
         views.ServiceRetrieveUpdateDestroyAPIView.as_view(),
         name='service-detail'),
]
