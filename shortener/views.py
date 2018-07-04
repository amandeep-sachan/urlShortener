from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.core.cache import cache
import pickle
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from analytics.models import ClickEvent

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

from .forms import SubmitUrlForm
from .models import DjangoURL

# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForm()
        context = {
            "title": "URL Shortener",
            "form": the_form
        }
        return render(request, "shortener/home.html", context)
    def post(self, request, *args, **kwargs):
        form = SubmitUrlForm(request.POST)
        context = {
            "title": "URL Shortener",
            "form": form
        }
        template = "shortener/home.html"

        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            if not "http" in new_url:
                new_url = "http://" + new_url
            obj, created = DjangoURL.objects.get_or_create(url=new_url)
            context = {
                "object": obj,
                "created": created,
            }
            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/already-exists.html"

        return render(request, template, context)

class UrlRedirectView(View):
    def get(self, request,shortcode=None, *args, **kwargs):
        # obj = get_object_or_404(DjangoURL, shortcode = shortcode)
        if shortcode in cache:
            obj = pickle.loads(cache.get(shortcode))
        else:
            obj = get_object_or_404(DjangoURL, shortcode = shortcode)
            cache.set(shortcode, pickle.dumps(obj))
        # print(ClickEvent.objects.create_event(obj))
        return HttpResponseRedirect(obj.url)
