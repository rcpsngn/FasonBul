from django.http import JsonResponse
from .models import District


def get_districts(request, city_id):
    """AJAX ile şehir seçildiğinde ilçeleri getiren view"""
    districts = District.objects.filter(city_id=city_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)