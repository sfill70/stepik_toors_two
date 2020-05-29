from django.urls import path
from .views import custom_handler404, MainView, DepartureView, TourView

app_name = 'tours'

urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('departure/<str:departure>/', DepartureView.as_view(), name='departure'),
    path('tour/<int:id>/', TourView.as_view(), name='tour'),
]

handler404 = custom_handler404
