from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Leads
from django.contrib.auth import authenticate, login as authlogin, logout as authlogout
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseRedirect
import requests
import threading

def worker(request):
    requests.post('http://127.0.0.1:8000/api/leads/',data =  {"empresa": request.POST.get('empresa')})
    return

    
    
# Create your views here.
@login_required(login_url='/login/')
def homepage(request):

    if request.method == 'POST':
        # manda pra api
        t = threading.Thread(target=worker,args=(request,))
        t.start()
        messages.add_message(request, messages.SUCCESS, ('Buscando a empresa - %s - ' %request.POST.get('empresa')))
        messages.add_message(request, messages.INFO, ("O sistema coleta informações 24 horas por dia, espere até 1 min para obter resultados."))
        return HttpResponseRedirect(reverse('app:leads'))
    return render(request,'homepage/homepage.html')

def leads(request):
    content = {}
    content['empresas'] = Leads.objects.values('empresa').annotate(dcount=Count('empresa')).order_by()
    for empresa in content['empresas']:
        empresa['users'] = Leads.objects.filter(empresa = empresa["empresa"])
    content['all'] = Leads.objects.all()
    return render(request, 'leads/leads.html',{'content':content})


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('app:homepage'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            authlogin(request, user)
            return HttpResponseRedirect(reverse('app:homepage'))
        # messages.add_message(request, messages.Danger, 'Hello world.')
        
    
    return render(request,'login/login.html')

def logout(request):
    authlogout(request)
    return HttpResponseRedirect(reverse('app:login'))