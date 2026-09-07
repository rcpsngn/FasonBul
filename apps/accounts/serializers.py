from rest_framework import serializers

from .models import User, Profile, Document, Machine, DocumentAccessRequest


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'name', 'quantity', 'note']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'document_type', 'file', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class ProfileSerializer(serializers.ModelSerializer):
    machines = MachineSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'company_name', 'tax_number', 'address', 'description',
            'is_verified', 'verified_at', 'machines',
        ]
        read_only_fields = ['is_verified', 'verified_at']


class DocumentAccessRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentAccessRequest
        fields = ['id', 'document', 'requester', 'status', 'requested_at', 'responded_at']
        read_only_fields = ['status', 'requested_at', 'responded_at']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone', 'city', 'avatar', 'profile',
        ]
