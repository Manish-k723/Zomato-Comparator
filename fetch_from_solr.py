import requests

def extract_lat_lon(response):
    if 'response' in response and 'docs' in response['response'] and len(response['response']['docs']) > 0:
        latlon = response['response']['docs'][0].get('latlon', '')
        if latlon:
            lat, lon = latlon.split(',')
            return float(lat), float(lon)
    return None, None

def make_solr_call(locality, city):
    base_url = "http://10.140.2.30/solr/entity/select"
    params = {
        'fq': [
            f'city:"{city}"',
            f'name:"{locality}"',
            f'type:"locality"'
        ],
        'indent': 'true',
        'q.op': 'OR',
        'q': '*:*'
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()  # or response.text for raw response
    else:
        response.raise_for_status()

def get_lat_lon(locality, city):
    response = make_solr_call(locality, city)
    lat, lon = extract_lat_lon(response)
    return lat, lon