# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render


def sign_up(request):
    return render(request, "sign_up.html")


def get_token(request):
    return render(request, "token.html")


def sign_in(request):
    return render(request, "login.html")


def dashboard_view(request):
    return render(request, "dashboard.html")
