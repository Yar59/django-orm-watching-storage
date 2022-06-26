from django.utils import timezone
from django.shortcuts import render

from datacenter.models import Visit
from datacenter.models import calculate_visit_duration
from datacenter.models import convert_duration
from datacenter.models import is_visit_strange


def storage_information_view(request):
    
    formatted_non_closed_visits = []
    
    non_closed_visits = Visit.objects.filter(leaved_at=None)
    
    for visit in non_closed_visits:
        visitor_name = visit.passcard
        visit_duration = calculate_visit_duration(visit)
        formatted_visit_duration = convert_duration(visit_duration)
        formatted_non_closed_visits.append(
            {
                'who_entered': visitor_name,
                'entered_at': timezone.localtime(visit.entered_at),
                'duration': formatted_visit_duration,
                'is_strange': is_visit_strange(visit_duration)
            }
        )
        
    context = {
        'non_closed_visits': formatted_non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
