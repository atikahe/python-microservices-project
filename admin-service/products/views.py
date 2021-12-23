import random
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .producer import publish
from .models import Products, User
from .serializers import ProductSerializer

# View using ViewSet
class ProductsViewSet(viewsets.ViewSet):
    def list(self, request): # GET /api/products
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request): # POST /api/products
        # Serialize data
        serializer = ProductSerializer(data=request.data)
        # Validate and save data
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Publish RabbitMQ message
        publish('product_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None): # GET /api/products/<str:pk>
        product = Products.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        # Get product instance
        product = Products.objects.get(id=pk)
        # Format product instance with new data
        serializer = ProductSerializer(instance=product, data=request.data)
        # Validate & save
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Publish RabbitMQ message
        publish('product_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        product = Products.objects.get(id=pk)
        product.delete()
        publish('product_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

# View using APIView
class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'user': user.name
        })