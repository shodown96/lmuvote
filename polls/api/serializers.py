from polls.models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'c_type']


class CategoryDetailSerializer(serializers.ModelSerializer):
    candidates = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'c_type']
    def get_candidates(self, obj):
        return CandidateSerializer(obj.candidate_set.all(), many=True).data

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'department',
            'level',
            'category',
            'cover',
            'get_full_name'
            'get_votes'
            'is_winner'
        ]

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = [
            'id',
            'user',
            'category',
            'candidate',
            'timestamp',
        ]

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, required=True)
    webmail = serializers.EmailField(max_length=200, required=True)
    room_number = serializers.CharField(max_length=4, required=True)
    hall = serializers.CharField(max_length=50, required=True)
    challenge = serializers.CharField(required=True)