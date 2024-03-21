from django.shortcuts import render
import requests
from datetime import datetime
from django.core.cache import cache
from urllib.parse import urlparse, parse_qs

def home_view(request):
    url_fournie = request.GET.get('url') or request.POST.get('url') or 'Votre URL par défaut ici'
    
    parsed_url = urlparse(url_fournie)
    query_params = parse_qs(parsed_url.query)
    segments = parsed_url.path.split('/')
    practitioner_name = segments[3] if len(segments) > 3 else None
    
    visit_motive_ids = query_params.get('motiveIds[]', [''])[0] if 'motiveIds[]' in query_params else None
    practice_ids = query_params.get('placeId', [''])[0].split('-')[-1] if 'placeId' in query_params else None
    
    data = None
    if practitioner_name and visit_motive_ids and practice_ids:
        draft_url = f'https://www.doctolib.fr/online_booking/draft/new.json?id={practitioner_name}'
        draft_response = requests.get(draft_url, headers={'User-Agent': 'MonUserAgent'})
        draft_data = draft_response.json()

        if 'data' in draft_data and 'agendas' in draft_data['data']:
            agenda_ids = [str(agenda['id']) for agenda in draft_data['data']['agendas']]
            
            response = requests.get(
                'https://www.doctolib.fr/availabilities.json',
                headers={'User-Agent': 'MonUserAgent'},
                params={
                    'visit_motive_ids': visit_motive_ids,
                    'agenda_ids': agenda_ids[0], 
                    'practice_ids': practice_ids,
                    'telehealth': 'false',
                    'limit': '15',
                    'start_date': datetime.today().strftime('%Y-%m-%d')
                }
            )

            data = response.json()
            fetch_and_compare_data(data)
            print(data)
    return render(request, 'home_view.html', {'data': data})

def fetch_and_compare_data(data):
    last_data = cache.get('last_api_response')
    cache.set('last_api_response', data, timeout=None)
    if data != last_data:
        print("Un changement a été détecté dans la réponse de l'API.")
