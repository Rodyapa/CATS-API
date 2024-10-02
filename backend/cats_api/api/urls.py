from api.views import BreedViewSet, CatsViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

api_v1 = DefaultRouter()
api_v1.register('breeds', BreedViewSet, basename='breeds')
api_v1.register('cats', CatsViewSet, basename='cats')

urlpatterns = [
    path('', include(api_v1.urls)),
    path('auth/', include('djoser.urls.jwt'), name='auth'),
]
