from django.shortcuts import render
from django.views.generic import TemplateView

class LivePriceView(TemplateView):
    template_name = 'live2.html'