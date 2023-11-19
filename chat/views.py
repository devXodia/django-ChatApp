from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Chat, Message
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core import serializers

@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        print('Recieved data ' + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        new_msg = Message.objects.create(text = request.POST['textmessage'], chat = myChat, author = request.user, receiver = request.user)
        serialized_obj = serializers.serialize('json', [new_msg])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id = 1)
    return render(request, 'chat/index.html', {'messages': chatMessages})


def login_view(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':
        user = authenticate(username = request.POST.get('username'), password = request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect('/chat/')
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})

def reg_view(request):

    if request.method == 'POST':
        pwd = request.POST.get('pwd')
        confirm_pwd = request.POST.get('confirmPwd')
        if pwd != confirm_pwd:
            pwdDontMatch = True
            return render(request, 'auth/register.html', {'redirect': '/login/', 'pwdDontMatch': pwdDontMatch})
        else:
            pwdDontMatch = False
            user = get_user_model().objects.create_user(username=request.POST.get('username'),
                                 password=request.POST.get('pwd'), first_name=request.POST.get('username'))
            return HttpResponseRedirect('/login/')
    return render(request, 'auth/register.html', {'redirect': '/login/', 'pwdDontMatch': False})