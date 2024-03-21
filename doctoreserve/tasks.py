# doctoreserve/tasks.py

from celery import shared_task
import requests
from django.core.cache import cache
from datetime import datetime

@shared_task
def fetch_and_compare_data():
    date = datetime.today().strftime('%Y-%m-%d')
    
    response = requests.get(
        'https://www.doctolib.fr/availabilities.json',
        headers={'User-Agent': 'MonUserAgent'},
        params={
            'visit_motive_ids': '215341',
            'agenda_ids': '37160',
            'practice_ids': '12486',
            'telehealth': 'false',
            'limit': '15',
            'start_date': date
        }
    )

    data = response.json()
    last_data = cache.get('last_api_response')

    cache.set('last_api_response', data, timeout=None)  

    if data != last_data:
        print("Un changement a été détecté dans la réponse de l'API.")
        # Effectuez ici des actions supplémentaires en cas de changement

