from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib import messages
from django.db.models import Q
from general.forms import *
from general.models import *


from django.contrib.auth.decorators import login_required

def createShop(request):
    if request.method == "POST":
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "บันทึกข้อมูลร้านสำเร็จ")
            return redirect("shopList")
        else:
            messages.error(request, "บันทึกข้อมูลร้านไม่สำเร็จ")
            return redirect("createShop")
    else:
        form = ShopForm()
    context = {"form": form}
    return render(request, "general/createShop.html", context)


def editShop(request, id):
    if request.method == "POST":
        shop = get_object_or_404(Shop, id=id)
        form = ShopForm(data=request.POST or None, files=request.FILES, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, "อัพเดทข้อมูลร้านสำเร็จ")
            return redirect("shopList")
        else:
            messages.error(request, "อัพเดทข้อมูลร้านล้มเหลว")
            return redirect("editShop")
    else:
        shop = Shop.objects.get(id=id)
        form = ShopForm(instance=shop)
    context = {"form": form, "shop": shop}
    return render(request, "general/editShop.html", context)
    
def deleteShop(request, id):
    shop = get_object_or_404(Shop, id=id)
    shop.delete()
    return redirect("shopList")


def shopList(request):
    shops = Shop.objects.all().order_by('id').reverse()
    count = shops.count()
    context = {"shops": shops, "count": count}
    return render(request, "general/shopList.html", context)


def search_shop(request):
    search = request.GET.get('search')
    if search:
        shop = Shop.objects.filter(title__icontains=search)
        if not shop:
            messages.error(request, 'ไม่พบข้อมูลที่กำลังค้นหา')
            return redirect('shopList')
    else:
        return redirect('shopList')
    context = {'shop': shop}
    return render(request, "general/shopList.html", context)


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
