# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.conf import settings


def index(request):
    '''Home page.'''
    return HttpResponse('hello')
