from django.http import JsonResponse
from app.views import Multipleoperation
import json


class BatchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path == '/batch':
            try:
                batch_data = json.loads(request.body)
                if not isinstance(batch_data, list):
                    return JsonResponse({'error': 'Batch request must be a JSON array'}, status=400)
                multiple = Multipleoperation()
                response_data = multiple.process_batch(batch_data)
                return JsonResponse(response_data, safe=False)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        return self.get_response(request)