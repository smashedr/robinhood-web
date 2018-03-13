import json
import logging
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from home.models import ShareData, ConnectData

logger = logging.getLogger('app')


@csrf_exempt
@require_http_methods(['GET'])
def get_positions(request):
    """
    View  /api/positions/
    """
    try:
        _id = request.GET.get('id')
        api_key = request.GET.get('api-key')
        if api_key != settings.CONFIG['app']['api_key']:
            return HttpResponse('Invalid API Key.', status=401)
        if not _id:
            return HttpResponse('Missing Parameter: id', status=400)
        c = ConnectData.objects.get(conn_id=_id)
        s = ShareData.objects.get(share_owner=c.username)
        j = json.loads(s.securities)
        data = {
            'success': True,
            'message': 'Success.',
            'generated_at': s.generated_at.strftime('%c'),
            'results': j,
        }
        return JsonResponse(data)
    except Exception as error:
        logger.exception(error)
        data = {
            'success': False,
            'message': str(error),
        }
        return JsonResponse(data, status=500)


def do_callback(conn_id):
    callback_uri = settings.CONFIG['app']['callback_uri']
    data = {
        'api-key': settings.CONFIG['app']['jank_key'],
        'id': conn_id,
        'connected': True
    }
    r = requests.post(callback_uri, data=data, timeout=10)
    return r
