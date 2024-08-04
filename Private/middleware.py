from django.utils.deprecation import MiddlewareMixin

from .utils import decode_id, encode_id


class IDEncodingMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'id' in request.GET:
            request.GET = request.GET.copy()
            request.GET['id'] = decode_id(request.GET['id'])

        # if 'id' in request.POST:
        #     request.POST = request.POST.copy()
        #     request.POST['id'] = decode_id(request.POST['id'])

        if 'id' in view_kwargs:
            view_kwargs['id'] = decode_id(view_kwargs['id'])

        return None

    def process_template_response(self, request, response):
        if hasattr(response, 'context_data') and response.context_data:
            for key, value in response.context_data.items():
                if isinstance(value, dict) and 'id' in value:
                    value['id'] = encode_id(value['id'])
                elif hasattr(value, 'id'):
                    value.id = encode_id(value.id)
        return response
