# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.template.loader import render_to_string
from rest_framework.reverse import reverse
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from core.models import User
from django.contrib.auth import login, logout
import random
from rest_framework.decorators import authentication_classes, permission_classes
from core.tasks import send_mail
from dashboard.models import UserProfile


@authentication_classes([])
@permission_classes([])
class SignUp(APIView):
    parser_classes = (FormParser,)

    def post(self, request):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        mobile = request.data.get("mobile")
        gender = request.data.get("gender")
        if User.objects.filter(email=email):
            return JsonResponse({
                'error': True
            })
        else:
            User.objects.create(first_name=first_name, last_name=last_name, email=email, phone_number=mobile, gender=gender)
            return JsonResponse({
                'success': True,
                'token_page': reverse('dashboard:get_token', request=request)
            })


@authentication_classes([])
@permission_classes([])
class GetToken(APIView):
    parser_classes = (FormParser,)

    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            if user:
                ascii_letters = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                activation_key = ''.join(random.choice(ascii_letters) for i in range(16))
                print activation_key
                user_profile, create = UserProfile.objects.get_or_create(user=user)
                user_profile.token = activation_key
                user_profile.save()
                data = {'user': user, 'activation_key': activation_key}
                email_template = render_to_string("send_email.html", data)
                send_mail("Login Authentication", email_template, user.email, [user.email])
                return JsonResponse({
                    'success': True,
                    'login_page': reverse('dashboard:sign-in', request=request)
                })
        except User.DoesNotExist:
            return JsonResponse({
                'error': True
            })


@authentication_classes([])
@permission_classes([])
class SignIn(APIView):
    parser_classes = (FormParser,)

    def post(self, request):
        token = request.data.get("token")
        try:
            get_token = UserProfile.objects.get(token=token)
            if get_token:
                login(request, get_token.user)
                return JsonResponse({
                    'success': True,
                    'dashboard_page': reverse('dashboard:dashboard-view', request=request)
                })
        except User.DoesNotExist:
            return JsonResponse({
                'error': True
            })


class Dashboard(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser,)

    def post(self, request):
        logout(request)
        return JsonResponse({
            'success': True
        })


class LogOut(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (FormParser,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        logout(request)
        return JsonResponse({
            'success': True,
            'login_page': reverse('dashboard:get_token', request=request)
        })
