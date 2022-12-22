from django.urls import path
from .views import *

urlpatterns = [
    path('country-pagination/', CountryPagination.as_view()),
    path('state-pagination/', StatePagination.as_view()),
    path('city-pagination/', CityPagination.as_view()),

    path('country/',CountryChanges.as_view()),
    path('country/<int:pk>',CountryChanges.as_view()),

    path('state/',StateChanges.as_view()),
    path('state/<int:pk>',StateChanges.as_view()),

    path('city/',CityChanges.as_view()),
    path('city/<int:pk>',CityChanges.as_view()),
]