from rest_framework.views import APIView
from rest_framework.response import Response
from ..Main import get_recommendations, get_all

class RecommendationViewSet(APIView):
    def get(self, request, user, format=None):
        recommendations = get_recommendations(user)
        return Response({"recommendations": recommendations})
    
class UserViewSet(APIView):
    def get(self, request, product, format=None):
        users = get_all(product)
        return Response({"users": users})