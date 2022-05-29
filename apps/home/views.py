# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http.response import StreamingHttpResponse
from apps.home.camera import VideoCamera
from django.shortcuts import render, redirect
from .models import UsersStudent
from datetime import datetime
from apps.users.models import Vendor
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import json
from django.contrib.auth.models import User


@login_required(login_url="/loginUser/")
def index(request):
    context = {}
    # try:
    p = Vendor.objects.get(EmailID=request.user.username)
    if not p.PasswordReset:
        context['reset'] = True
        return render(request, 'home/passwordchange.html', context)
    # except:
    #     # html_template = loader.get_template('accounts/loginUser.html')
    #     return HttpResponseRedirect(reverse('apps.authentication:login'))
    credential = json.load(open('apps/home/AzureCloudKeys.json'))
    API_KEY = credential['API_KEY']
    ENDPOINT = credential['ENDPOINT']
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))
    q = face_client.person_group_person.get(p.Username, p.person_id)
    if not len(q.persisted_face_ids):
        return render(request, 'home/addimage.html', context)
    html_template = loader.get_template('home/tables.html')
    objects = reversed(UsersStudent.objects.filter(
        Username=request.user.username))
    context['users'] = objects
    if 'form' in request.session:
        context['form'] = 'Marked'
        del request.session['form']
    if 'd' in request.session:
        objects = reversed(UsersStudent.objects.filter(
            Vendor=p.Username, Username=request.user.username, Date=request.session['d']))
        context['users'] = objects
        del request.session['d']
    return render(request, 'home/tables.html', context)
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/loginUser/")
def add(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/icons.html')
    return HttpResponse(html_template.render(context, request))


def main(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/main.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/loginUser/")
def homeprofile(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/profile.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/loginUser/")
def tables(request):
    objects = reversed(UsersStudent.objects.filter(
        Username=request.user.username))
    return render(request, 'home/tables.html', {'users': objects})


def gen(camera):
    while True:
        frame, success = camera.get_frame()
        if(success):
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            break


@login_required(login_url="/loginUser/")
def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


@login_required(login_url="/loginUser/")
def recognize(request):
    video = VideoCamera()
    p = Vendor.objects.get(EmailID=request.user.username)
    name = video.recognize(persongroupid=p.Username)
    if(request.user.username == name):
        context = {}
        context['name'] = name
        k = UsersStudent.objects.filter(
            Username=request.user.username, Date=datetime.now().date())
        if(k):
            if not k[len(k)-1].Out:
                context['In'] = True
            if k[len(k)-1].Mealin:
                context['Mealin'] = True
            if k[len(k)-1].Mealout:
                context['Mealout'] = True
        else:
            context['In'] = False
        return render(request, 'home/attendance.html', context)
    else:
        context = {
            'error_message': "Attendance not marked"}
        return render(request, 'home/icons.html', context)


@login_required(login_url="/loginUser/")
def home(request):
    if 'form' in request.session:
        del request.session['form']
    q = UsersStudent.objects.filter(
        Username=request.user.username, Date=datetime.now().date())
    if 'in' in request.POST:
        now = datetime.now()
        h = Vendor.objects.get(EmailID=request.user.username)
        vendor = h.Username
        q = UsersStudent(Username=request.user.username,
                         Date=datetime.now().date(), In=datetime.now().strftime("%H:%M:%S"), Vendor=vendor)
        q.save()
    elif 'meal' in request.POST:
        p = UsersStudent.objects.filter(
            Username=request.user.username, Date=datetime.now().date())
        if p[len(p)-1].Mealin and not p[len(p)-1].Mealout:
            p = UsersStudent.objects.filter(
                id=p[len(p)-1].id, Username=request.user.username, Date=datetime.now().date())
            p.update(Mealout=datetime.now().strftime("%H:%M:%S"))
        elif p[len(p)-1].Mealin and p[len(p)-1].Mealout:
            h = Vendor.objects.get(EmailID=request.user.username)
            vendor = h.Username
            q = UsersStudent(Username=request.user.username, Date=datetime.now(
            ).date(), Mealin=datetime.now().strftime("%H:%M:%S"), Vendor=vendor)
            q.save()
        else:
            q.update(Mealin=datetime.now().strftime("%H:%M:%S"))
    elif 'out' in request.POST:
        if(q):
            p = UsersStudent.objects.filter(
                Username=request.user.username, Date=datetime.now().date())
            q = UsersStudent.objects.filter(
                id=p[len(p)-1].id, Username=request.user.username, Date=datetime.now().date())
            q.update(Out=datetime.now().strftime("%H:%M:%S"))
    request.session['form'] = 'Marked'
    return redirect('home')


@ login_required(login_url="/loginUser/")
def capture(request):
    p = Vendor.objects.get(EmailID=request.user.username)
    video = VideoCamera()
    name = video.capture(person_id=p.person_id, persongroupid=p.Username)
    if name:
        context = {'segment': 'index'}
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'home/addimages.html', {'error_message': 'Image you captured is not of sufficient quality or no person detected, Try Again'})

@login_required(login_url="/loginUser/")
def passwordchange(request):
    context = {}
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if password1:
                u = User.objects.get(username=request.user.username)
                u.set_password(password1)
                u.save()
                context['reset'] = False
                Vendor.objects.filter(EmailID=request.user.username).update(
                    PasswordReset=True)
            else:
                context['reset'] = True
                context['Passworderror'] = 'Please enter Password'
                return render(request, 'home/passwordchange.html', context)
        else:
            context['reset'] = True
            context['Passworderror'] = 'Password did not not match'
            return render(request, 'home/passwordchange.html', context)
    else:
        context['reset'] = True
        return render(request, 'home/passwordchange.html', context)
    return redirect('home')

@login_required(login_url="/loginUser/")
def filters(request):
    if request.method == 'POST':
        p = Vendor.objects.get(EmailID=request.user.username)
        date = request.POST['date']
        if date:
            dt = datetime.strptime(date, '%m/%d/%Y')
            d = datetime.strftime(dt, "%Y-%m-%d")
            objects = reversed(UsersStudent.objects.filter(
                Vendor=p.Username, Username=request.user.username, Date=d))
        context = {'users': objects}
        request.session['d'] = d
        return redirect('home')
    return redirect('home')
