# reports/serializers.py
from rest_framework import serializers
from .models import Report, ReportPhoto


class ReportPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportPhoto
        fields = ['id', 'image_url', 'uploaded_at']


class ReportSerializer(serializers.ModelSerializer):
    photos = ReportPhotoSerializer(many=True, read_only=True)
    image_urls = serializers.ListField(
        child=serializers.URLField(),
        write_only=True,
        required=False
    )
    user_display = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id',
            'user_display',
            'latitude',
            'longitude',
            'address',
            'postcode',
            'council_name',
            'council_notified',
            'waste_type',
            'size',
            'description',
            'status',
            'photos',
            'image_urls',
            'created_at',
            'updated_at',
            'cleared_at',
        ]
        read_only_fields = [
            'id',
            'council_name',
            'council_notified',
            'created_at',
            'updated_at',
            'cleared_at',
        ]

    def get_user_display(self, obj):
        if obj.user:
            return obj.user.username
        return 'Anonymous'

    def create(self, validated_data):
        image_urls = validated_data.pop('image_urls', [])
        report = Report.objects.create(**validated_data)
        for url in image_urls:
            ReportPhoto.objects.create(report=report, image_url=url)
        return report


class ReportListSerializer(serializers.ModelSerializer):
    ## Lightweight version for the map view - no photos needed
    photo_count = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id',
            'latitude',
            'longitude',
            'waste_type',
            'size',
            'status',
            'postcode',
            'council_name',
            'photo_count',
            'created_at',
        ]

    def get_photo_count(self, obj):
        return obj.photos.count()