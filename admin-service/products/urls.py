from django.urls import path

from .views import ProductsViewSet, UserAPIView

urlpatterns = [
    path('products/', ProductsViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('products/<str:pk>', ProductsViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),
    path('user', UserAPIView.as_view())
]