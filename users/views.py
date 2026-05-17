from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import DatabaseError, IntegrityError
from django.urls import reverse
from .forms import RegisterForm, LoginForm


def register_view(request):
    """
    Handles new user registration. 
    If the user is already authenticated, redirects to the dashboard. 
    Otherwise, processes the RegisterForm and logs in the new user upon success.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        except (IntegrityError, DatabaseError):
            messages.error(
                request,
                'Could not create account. Database may be unavailable — check Postgres on Vercel.',
            )
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """
    Manages user login authentication.
    Redirects authenticated users to the dashboard. Validates credentials 
    via LoginForm and initiates a secure session.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request.POST or None, request=request)
    if request.method == 'POST' and form.is_valid():
        try:
            login(request, form.user)
            return redirect('dashboard')
        except DatabaseError:
            messages.error(request, 'Sign in failed. Database connection error.')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """
    Terminates the current user session and redirects to the login page.
    """
    logout(request)
    return redirect('/users/login/')


@login_required
def profile_view(request):
    """
    Renders the profile page for the currently logged-in user.
    Access is restricted to authenticated users only.
    """
    return render(request, 'users/profile.html')