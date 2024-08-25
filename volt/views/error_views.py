import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)


def error_404(request, exception):
    return render(request, "errors/404.html", status=404)


def error_500(request):
    return render(request, "errors/500.html")
