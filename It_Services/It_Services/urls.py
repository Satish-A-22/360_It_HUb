"""
URL configuration for It_Services project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views  
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.first,name='first'),
    path('home',views.submit_form,name='form'),
    path('email',views.email,name='email'),
    path('otp',views.otp,name='otp'),
    
    path('itemform', views.submit_service, name='submit_service'),
    path('items', views.service_list, name='service_list'), 

    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('services/<int:pk>/update/', views.update_service, name='update_service'),
    path('services/<int:pk>/delete/', views.delete_service, name='delete_service'),
    path('subscription/<int:pk>/', views.subscription_view, name='subscription_page'),
    path('create-subscription/', views.create_subscription, name='create_subscription'),
    path('razorpay-callback/', views.razorpay_callback, name='razorpay_callback'),
    path('logout',views.log,name='logout'),
    path('success',views.success,name='success'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)