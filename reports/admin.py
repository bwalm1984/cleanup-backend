# reports/admin.py
from django.contrib import admin
from .models import Report, ReportPhoto

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'waste_type', 'size', 'status', 'postcode', 'council_name', 'created_at']
    list_filter = ['status', 'waste_type', 'size']
    search_fields = ['postcode', 'council_name', 'address']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(ReportPhoto)
class ReportPhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'report', 'uploaded_at']