# reports/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils import timezone
import requests

from .models import Report
from .serializers import ReportSerializer, ReportListSerializer


def lookup_council(postcode):
    try:
        postcode_clean = postcode.replace(' ', '').replace('+', '').upper()
        url = f"https://api.postcodes.io/postcodes/{postcode_clean}"
        response = requests.get(url, timeout=5)
        print(f"Postcodes.io status: {response.status_code}")
        print(f"Postcodes.io response: {response.text}")
        if response.status_code == 200:
            data = response.json()['result']
            return {
                'council_name': data.get('admin_district', ''),
                'county': data.get('admin_county', ''),
                'region': data.get('region', ''),
            }
    except Exception as e:
        print(f"Council lookup error: {e}")
    return {}


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ReportListSerializer
        return ReportSerializer

    def get_queryset(self):
        queryset = Report.objects.all()
        ## Filter by bounding box for map view
        lat_min = self.request.query_params.get('lat_min')
        lat_max = self.request.query_params.get('lat_max')
        lng_min = self.request.query_params.get('lng_min')
        lng_max = self.request.query_params.get('lng_max')
        status_filter = self.request.query_params.get('status')

        if all([lat_min, lat_max, lng_min, lng_max]):
            queryset = queryset.filter(
                latitude__gte=lat_min, latitude__lte=lat_max,
                longitude__gte=lng_min, longitude__lte=lng_max
            )
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

    def perform_create(self, serializer):
        postcode = serializer.validated_data.get('postcode', '')
        council_data = lookup_council(postcode) if postcode else {}
        serializer.save(
            user=self.request.user,
            council_name=council_data.get('council_name', ''),
        )

    @action(detail=True, methods=['post'])
    def mark_cleared(self, request, pk=None):
        ## Lets users mark a report as cleared
        report = self.get_object()
        report.status = Report.STATUS_CLEARED
        report.cleared_at = timezone.now()
        report.save()
        return Response({'status': 'cleared'})

    @action(detail=False, methods=['get'])
    def my_reports(self, request):
        ## Returns only the logged-in user's reports
        reports = Report.objects.filter(user=request.user)
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def council_lookup(self, request):
        ## Standalone postcode lookup for the app
        postcode = request.query_params.get('postcode', '')
        if not postcode:
            return Response(
                {'error': 'postcode required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = lookup_council(postcode)
        return Response(data)

from rest_framework.decorators import api_view

@api_view(['GET'])
def test_postcode(request):
    import requests
    postcode = request.query_params.get('postcode', 'M320JG')
    postcode_clean = postcode.replace(' ', '').replace('+', '').upper()
    url = f"https://api.postcodes.io/postcodes/{postcode_clean}"
    try:
        r = requests.get(url, timeout=10)
        return Response({'status': r.status_code, 'body': r.json(), 'postcode_sent': postcode_clean})
    except Exception as e:
        return Response({'error': str(e)})

