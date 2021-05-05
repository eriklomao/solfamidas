from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import CreateUserForm

def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('principal')
		else:
			messages.info(request, 'El usuario o la constraseña son incorrectos')



	return render(request, "login.html", {})


def registerPage(request):

	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'La cuenta ha sido creada con exito')

			return redirect('login')

	return render(request, "register.html", {'form': form})

def logoutUser(request):
	logout(request)
	return redirect('login')