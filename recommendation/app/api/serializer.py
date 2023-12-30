# from rest_framework import serializers
# from ..models import *

# class RecommendationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recommendation
#         fields = ['id', 'user', 'rec1', 'rec2', 'rec3', 'rec4', 'rec5', 'rec6', 'rec7', 'rec8', 'rec9', 'rec10']
from rest_framework import serializers

class RecommendationSerializer(serializers.Serializer):
    recommendations = serializers.ListField()