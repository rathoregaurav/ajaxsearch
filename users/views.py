from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from users.models import job_finder
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('job')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

class jobfinderSerializer(serializers.ModelSerializer):
    class Meta:
        model = job_finder  
        fields = '__all__'

@csrf_exempt
@api_view(['GET', 'POST'])
def show_data(request):
    if request._request.method=="POST":
        print request.data["skills"]
        job_user_data = job_finder.objects.filter(skills__istartswith=request.data["skills"]).all()
        job_data_seri = jobfinderSerializer(job_user_data, many=True)
        return Response({"data":job_data_seri.data, "success": True})
    else:
        job_user_data = job_finder.objects.all()
        job_data_seri = jobfinderSerializer(job_user_data, many=True)
        return Response({"data":job_data_seri.data, "success": True})






