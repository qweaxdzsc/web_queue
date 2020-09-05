from django.shortcuts import render, HttpResponse, redirect
from django.shortcuts import redirect
from app_login import models
import json

# Create your views here.
# def index(request):
#     pass
#     return render(request, 'index.html')


def login(request):
    request.session.clear_expired()
    if request.method == "POST":
        user_auth = {
            'pass': False,
            'error_info': '',
            'authorization': '',
        }
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        account_email = name + '@estra-automotive.com'

        email_check = models.User.objects.filter(email=account_email)
        if not email_check:
            user_auth['error_info'] = '账户错误'
        else:
            pwd_check = email_check.filter(password=pwd)
            if not pwd_check:
                user_auth['error_info'] = '密码错误'
            else:
                user_auth['pass'] = True
                user_auth['authorization'] = pwd_check.first().authorization
                request.session['user_name'] = name
                request.session['authorization'] = pwd_check.first().authorization
        return HttpResponse(json.dumps(user_auth, ensure_ascii=False), content_type="application/json")

    return render(request, 'login.html')


def register(request):
    pass
    return render(request, 'register.html')


def logout(request):
    # request.session.flush()
    request.session.delete(request.session.session_key)
    # request.session.delete("session_key")
    return redirect("/")