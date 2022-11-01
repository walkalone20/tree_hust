from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.http import JsonResponse

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return JsonResponse({'0': "Registration successful."})
		return JsonResponse({'-1': "Registration invalid."})