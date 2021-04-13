from django.urls import path

from freights import views

app_name = 'freights'

urlpatterns = [
    # Freight
    path('', views.FreightListCreateAPIView.as_view(), name='list'),
    path('<int:pk>/', views.FreightRetrieveUpdateDestroyAPIView.as_view(), name='detail'),

    # Rule
    path('<int:pk>/rules/', views.RuleListCreateAPIView.as_view(), name='rule-list'),
    path('<int:freight_pk>/rules/<int:rule_pk>/', views.RuleRetrieveUpdateDestroyAPIView.as_view(), name='rule-detail'),

    # State
    path('<int:freight_pk>/rules/<int:rule_pk>/states/', views.StateListCreateAPIView.as_view(), name='state-list'),
    path('<int:freight_pk>/rules/<int:rule_pk>/states/<int:state_pk>/',
         views.StateRetrieveUpdateDestroyAPIView.as_view(),
         name='state-detail'),
]