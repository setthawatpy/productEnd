from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def test(request):
    return render(request, "pages/test.html")


def index(request):
    return render(request, "pages/index.html")


def tables(request):
    return render(request, "pages/tables.html")

# Components
@login_required(login_url='login')
def bc_button(request):
    return render(request, "tools/bc_button.html")


@login_required(login_url='login')
def bc_badges(request):
    return render(request, "tools/bc_badges.html")


@login_required(login_url='login')
def bc_breadcrumb_pagination(request):
    return render(request, "tools/bc_breadcrumb-pagination.html")


@login_required(login_url='login')
def bc_collapse(request):
    return render(request, "tools/bc_collapse.html")


@login_required(login_url='login')
def bc_tabs(request):
    return render(request, "tools/bc_tabs.html")


@login_required(login_url='login')
def bc_typography(request):
    return render(request, "tools/bc_typography.html")


@login_required(login_url='login')
def icon_feather(request):
    return render(request, "tools/icon-feather.html")


# Forms and Tables
@login_required(login_url='login')
def form_elements(request):
    return render(request, 'pages/form_elements.html')


@login_required(login_url='login')
def basic_tables(request):
    return render(request, 'pages/tbl_bootstrap.html')

# Chart and Maps


@login_required(login_url='login')
def morris_chart(request):
    return render(request, 'pages/chart-morris.html')


@login_required(login_url='login')
def google_maps(request):
    return render(request, 'pages/map-google.html')

# Authentication


class UserRegistrationView(CreateView):
    template_name = 'accounts/auth-signup.html'
    form_class = RegistrationForm
    success_url = '/accounts/login/'


class UserLoginView(LoginView):
    template_name = 'accounts/auth-signin.html'
    form_class = LoginForm


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/auth-reset-password.html'
    form_class = UserPasswordResetForm


class UserPasswrodResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/auth-password-reset-confirm.html'
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/auth-change-password.html'
    form_class = UserPasswordChangeForm


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    return render(request, 'pages/profile.html')


@login_required(login_url='login')
def sample_page(request):
    return render(request, 'pages/sample-page.html')
