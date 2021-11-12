"""To_Do_List URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from To_Do_List.base.views import change_status
from django.contrib import admin

from django.urls import path
from base import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.sign_up),
    path('', views.index_django),
    path('login/', views.login_request),
    path('home/', views.index_django),
    path('add-todo/', views.add_todo),
    path('logout/', views.signout),
    path('delete_todo/<int:id>/', views.delete_todo, name='delete_todo'),
    path('change_status/<int:id>/<str:status>', views.change_todo),
    path('edit_task/<int:id>', views.edit_task, name='edit_task'),
    path('profile/', views.profile),
    path('view_todo/<int:id>', views.view_todo, name='view_todo'),
    path('search/',views.search_query),
    path('change_password/', views.change_password),
     path('password-reset/',auth_views.PasswordResetView.as_view(template_name='base/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='base/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='base/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='base/password_reset_complete.html'),name='password_reset_complete'),   
    path('index_django/', views.index_django),
    path('venue_pdf/',views.venue_pdf,name='venue_pdf'),
    path('venue_csv/',views.venue_csv,name='venue_csv'),
    path('history/', views.history),
    path('pending/', views.pending),
     path('complete/', views.complete),
]
