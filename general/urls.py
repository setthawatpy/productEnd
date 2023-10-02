from django.urls import path
from admin_datta import views
from django.contrib.auth import views as auth_views
from general import views
from .views import tables

urlpatterns = [
    path('', views.index, name='index'),
    path('createShop', views.createShop, name='createShop'),
    path('editShop/<id>', views.editShop, name='editShop'),
    path('deleteShop/<id>', views.deleteShop, name='deleteShop'),
    path('shopList', views.shopList, name='shopList'),
    path('search_shop', views.search_shop, name='search_shop'),
    
    
    path('test/', views.test, name='test'),
    path('tables/', tables, name='tables'),

    # tools
    path('tools/button/', views.bc_button, name='bc_button'),
    path('tools/badges/', views.bc_badges, name='bc_badges'),
    path('tools/breadcrumb-pagination/', views.bc_breadcrumb_pagination, name='bc_breadcrumb_pagination'),
    path('tools/collapse/', views.bc_collapse, name='bc_collapse'),
    path('tools/tabs/', views.bc_tabs, name='bc_tabs'),
    path('tools/typography/', views.bc_typography, name='bc_typography'),
    path('tools/feather-icon/', views.icon_feather, name='icon_feather'),

    # Forms and Tables
    path('forms/form-elements/', views.form_elements, name='form_elements'),
    path('tables/basic-tables/', views.basic_tables, name='basic_tables'),

    # Chart and Maps
    path('charts/morris-chart/', views.morris_chart, name='morris_chart'),
    path('maps/google-maps/', views.google_maps, name='google_maps'),

    # Authentication
    path('accounts/register/', views.UserRegistrationView.as_view(), name='register'),
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),

    path('accounts/password-change/',
        views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/auth-password-change-done.html'
    ), name="password_change_done"),

    path('accounts/password-reset/',
        views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/',
        views.UserPasswrodResetConfirmView.as_view(), name="password_reset_confirm"
        ),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/auth-password-reset-done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/auth-password-reset-complete.html'
    ), name='password_reset_complete'),

    #
    path('profile/', views.profile, name='profile'),
    path('sample-page/', views.sample_page, name='sample_page'),
]
