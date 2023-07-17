from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
import datetime
from . import netbox
from .models import Fiber, InterfaceCounters, Temperature




class AboutView(TemplateView):
    template_name = 'jns/main.html'



def search(request):
    
    if request.method == 'POST':
        search_id = request.POST['textfield']
        switch = (InterfaceCounters.objects
                  .filter(switch__exact = search_id)
                  .using('int_reclaim'))
        context = {
            'switch': switch
        }
        
        return render(request, 'jns/reclaim_results.html', context)
    
    else:
        return render(request, 'jns/reclaim.html')



def fiber(request):
    
    if request.method == 'POST':
        search_id = request.POST['textfield']
        bad_interfaces = (Fiber.objects
                          .filter(date__gte=timezone.now()- datetime.timedelta(days=6))
                          .filter(rxlevel__range=(-30, search_id)))
        context = {
            'bad_interfaces': bad_interfaces
        }
     
        return render(request, 'jns/faulty.html', context)
    
    else:
        return render(request, 'jns/faulty_search.html')



def sfp_search(request):
    
    labels_date = []
    data_rxlevels = []
    interface_name = []

    if request.method == 'POST':
        search_id = request.POST['textfield']
        search_id2 = request.POST['textfield2']
        switch = Fiber.objects.filter(switch__exact = search_id)
        
        queryset = (Fiber.objects
                    .filter(switch__exact = search_id)
                    .filter(int_name__exact = search_id2)
                    .order_by('date'))
        
        for switch_name in queryset:
            labels_date.append(switch_name.date)
            data_rxlevels.append(switch_name.rxlevel)
            interface_name.append(switch_name.int_name)
        
        context = {
            'switch' : switch,
            'labels_switch': search_id,
            'labels_date': labels_date,
            'data_rxlevels': data_rxlevels,
            'interface_name': interface_name
        }
        
        return render(request, 'jns/sfp_history_results.html', context)
    
    else:
        return render(request, 'jns/sfp_history.html')



def temp_search(request):
    
    labels_date = []
    data_temp = []
    interface_name = []
    
    if request.method == 'POST':
        search_id = request.POST['textfield']
        search_id2 = request.POST['textfield2']
        search_id3 = request.POST['textfield3']
        switch = Temperature.objects.filter(switch__exact = search_id).using('temperature')
        queryset = (Temperature.objects
                    .filter(switch__exact = search_id)
                    .filter(date__range=[search_id2, search_id3])
                    .order_by('date')
                    .using('temperature'))

        for switch_name in queryset:
            labels_date.append(switch_name.date)
            data_temp.append(switch_name.temperature)
            interface_name.append(switch_name.int_name)
        
        context = {
            'switch': switch,
            'labels_switch': search_id,
            'labels_date': labels_date,
            'data_temp': data_temp,
            'interface_name': interface_name
        }
        
        return render(request, 'jns/temp_history_results.html', context)
    
    else:
        return render(request, 'jns/temp_history.html')



def temp_list(request):
    
    labels_date = []
    data_temp = []
    
    if request.method == 'POST':

        search_id = request.POST['temp_history_submit']

        switch = Temperature.objects.filter(switch__exact = search_id).using('temperature')
        
        queryset = (Temperature.objects
                    .filter(switch__exact = search_id)
                    .order_by('date')
                    .using('temperature'))

        for switch_name in queryset:
            labels_date.append(switch_name.date)
            data_temp.append(switch_name.temperature)
        
        context = {
            'switch': switch,
            'labels_switch': search_id,
            'labels_date': labels_date,
            'data_temp': data_temp,
        }
        
        return render(request, 'jns/temp_history_results.html', context)
    
    else:
        queryset = (Temperature.objects
                    .filter(date__gte=timezone.now()- datetime.timedelta(days=0))
                    .order_by('-temperature')
                    .using('temperature'))
        
        if len(queryset) <= 0:
            
            queryset = (Temperature.objects
                    .filter(date__gte=timezone.now()- datetime.timedelta(days=1))
                    .order_by('-temperature')
                    .using('temperature'))
            
            if len(queryset) <= 0:
            
                queryset = (Temperature.objects
                        .filter(date__gte=timezone.now()- datetime.timedelta(days=3))
                        .order_by('-temperature')
                        .using('temperature'))
    
        context = {
            'switch' : queryset
        }
        
        return render(request, 'jns/temp_list.html', context)



def net_topology(request):

    if request.method == 'POST':
        
        search_id = request.POST['textfield']
        
        api_result, api_data, device_id = netbox.netbox_req(search_id)

        if api_result:
            
            context = {
                'labels_switch': search_id,
                'device_id': device_id,
                'api_data' : api_data,
            }
            
            return render(request, 'jns/netbox_results.html', context)

        else:
            
            context = {
                'error' : "No connections found, please try again or enter a different device."
            }
            
            return render(request, 'jns/netbox.html', context)   
    
    else:
        return render(request, 'jns/netbox.html')
