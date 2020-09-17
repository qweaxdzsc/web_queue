from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from .. import views


def help(request):
    return HttpResponse('help document')


@csrf_exempt
def api_add(request):
    # print('1')
    add_project = views.AddProject()
    add_project.post(request)
    return HttpResponse('test api1')


def api_history(request):

    return HttpResponse('test api1')


def api_suspend(request):

    return HttpResponse('test api1')