from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls.exceptions import NoReverseMatch


class HandleNoReverseMatchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except NoReverseMatch:
            return redirect('error_500')
        except ObjectDoesNotExist:
            return redirect('error_404')
        return response
