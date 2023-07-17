from django.urls import path

from . import views

app_name = 'jns'
urlpatterns = [
    path('home/', views.TemplateView.as_view(template_name = 'jns/main.html'), name='home'),
    path('faulty/', views.fiber, name='faulty'),
    path('search/', views.search, name='search'),
    path('sfp_search/', views.sfp_search, name='sfp_search'),
    path('temp_search/', views.temp_search, name='temp_search'),
    path('temp_list/', views.temp_list, name='temp_list'),
    path('topology/', views.net_topology, name='topology')
]
