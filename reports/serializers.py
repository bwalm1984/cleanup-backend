class ReportListSerializer(serializers.ModelSerializer):
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
            'description',
            'photo_count',
            'created_at',
        ]

    def get_photo_count(self, obj):
        return obj.photos.count()