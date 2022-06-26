from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import calculate_visit_duration
from datacenter.models import convert_duration
from datacenter.models import is_visit_strange
from django.utils import timezone
from django.shortcuts import render



def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    passcard_visits = Visit.objects.filter(passcard=passcard)
    
    formatted_passcard_visits = []
    for visit in passcard_visits:
        visit_duration = calculate_visit_duration(visit)
        formatted_visit_duration = convert_duration(visit_duration)
        
        formatted_passcard_visits.append(
            {
                'entered_at': timezone.localtime(visit.entered_at),
                'duration': formatted_visit_duration,
                'is_strange': is_visit_strange(visit_duration),
            },
        )
    context = {
        'passcard': passcard,
        'this_passcard_visits': formatted_passcard_visits,
    }
    return render(request, 'passcard_info.html', context)
