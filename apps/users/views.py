from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from .forms import NameForm
from .models import Vendor
import json
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from apps.home.models import UsersStudent
from datetime import datetime
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
# Create your views here.


@login_required(login_url="/login/")
def delete(request):
    if request.method == "POST":
        user = request.POST['user']
        credential = json.load(open('apps/home/AzureCloudKeys.json'))
        API_KEY = credential['API_KEY']
        ENDPOINT = credential['ENDPOINT']
        PERSON_GROUP_ID = str(request.user.username)
        face_client = FaceClient(
            ENDPOINT, CognitiveServicesCredentials(API_KEY))
        a = Vendor.objects.get(EmailID=user)
        face_client.person_group_person.delete(
            person_group_id=PERSON_GROUP_ID, person_id=a.person_id)
        Vendor.objects.get(EmailID=user).delete()
        user = User.objects.filter(username=user)
        user.delete()
        msg1 = 'Employee Deleted Successfully'
        success = True
        objects = reversed(Vendor.objects.filter(
            Username=request.user.username))
        return render(request, 'users/icons.html', {"users": objects, "msg1": msg1, "Success": success})


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    objects = reversed(UsersStudent.objects.filter(
        Vendor=request.user.username))
    return render(request, 'users/tables.html', {'users': objects})


@login_required(login_url="/login/")
def map(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('users/map.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def profile(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('users/profile.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def Maintables(request):
    context = {'segment': 'index'}
    objects = reversed(UsersStudent.objects.filter(
        Vendor=request.user.username))
    return render(request, 'users/tables.html', {'users': objects})


@login_required(login_url="/login/")
def register_user(request):
    msg2 = None
    success = False
    if request.method == "POST":
        username = request.POST['username']
        Name = request.POST['name']
        Dob = request.POST['date']
        Address = request.POST['address']
        Aadhar = request.POST['aadhar']
        Designation = request.POST['designation']
        password = User.objects.make_random_password()
        try:
            user = User.objects.create_user(
                username=username, password=password)
            msg2 = 'Account created'
        except:
            objects = reversed(Vendor.objects.filter(
                Username=request.user.username))
            msg2 = 'User already exists'
            success = True
            return render(request, 'users/icons.html', {'users': objects, "msg": msg, "success": success})
        user.save()
        success = True
        credential = json.load(open('apps/home/AzureCloudKeys.json'))
        API_KEY = credential['API_KEY']
        ENDPOINT = credential['ENDPOINT']

        PERSON_GROUP_ID = str(request.user.username)

        face_client = FaceClient(
            ENDPOINT, CognitiveServicesCredentials(API_KEY))
        user = face_client.person_group_person.create(
            person_group_id=PERSON_GROUP_ID, name=username)
        df = datetime.strptime(Dob, '%m/%d/%Y')
        df = datetime.strftime(df, "%Y-%m-%d")
        q = Vendor(EmailID=username, Username=request.user.username,
                   person_id=user.person_id, Name=Name, Dob=df, Address=Address, AadharCard=Aadhar, Designation=Designation)
        q.save()
        ctx = {
            'user': Name,
            'Vendor': request.user.username,
            'password': password
        }
        message = get_template('users/email.html').render(ctx)
        msg = EmailMessage(
            'Welcome to Attendance Tracker',
            message,
            settings.EMAIL_HOST_USER,
            [username],
            cc=[request.user.email]
        )
        msg.content_subtype = "html"
        msg.send()
        success = True
    objects = reversed(Vendor.objects.filter(
        Username=request.user.username))
    return render(request, 'users/icons.html', {'users': objects, "msg": msg2, "success": success})


@login_required(login_url="/login/")
def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data.get("search")
            objects = Vendor.objects.filter(
                Username=request.user.username, EmailID__contains=str(search))
            context = {'users': objects}
            return render(request, 'users/icons.html', context)
    else:
        form = NameForm()
    return render(request, 'users/icons.html', {'form': form})


@login_required(login_url="/login/")
def filter(request):
    if request.method == 'POST':
        user = request.POST['user']
        date = request.POST['date']
        datefrom = request.POST['datefrom']
        dateto = request.POST['dateto']
        if user:
            objects = reversed(UsersStudent.objects.filter(
                Vendor=request.user.username, Username__contains=str(user)))
            if date:
                dt = datetime.strptime(date, '%m/%d/%Y')
                d = datetime.strftime(dt, "%Y-%m-%d")
                objects = reversed(UsersStudent.objects.filter(
                    Vendor=request.user.username, Username__contains=str(user), Date=d))
            elif datefrom and dateto:
                df = datetime.strptime(datefrom, '%m/%d/%Y')
                dt = datetime.strptime(dateto, '%m/%d/%Y')
                df = datetime.strftime(df, "%Y-%m-%d")
                dt = datetime.strftime(dt, "%Y-%m-%d")
                objects = reversed(UsersStudent.objects.filter(
                    Vendor=request.user.username, Username__contains=str(user), Date__range=[df, dt]))
        elif date:
            dt = datetime.strptime(date, '%m/%d/%Y')
            d = datetime.strftime(dt, "%Y-%m-%d")
            objects = reversed(UsersStudent.objects.filter(
                Vendor=request.user.username, Username__contains=str(user), Date=d))
        elif datefrom and dateto:
            df = datetime.strptime(datefrom, '%m/%d/%Y')
            dt = datetime.strptime(dateto, '%m/%d/%Y')
            df = datetime.strftime(df, "%Y-%m-%d")
            dt = datetime.strftime(dt, "%Y-%m-%d")
            objects = reversed(UsersStudent.objects.filter(
                Vendor=request.user.username, Username__contains=str(user), Date__range=[df, dt]))
        context = {'users': objects}
        return render(request, 'users/tables.html', context)
    return render(request, 'users/tables.html')
