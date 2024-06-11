import requests
import json

url = "https://www.zomato.com/webroutes/search/home"
dish_id = input()

payload = json.dumps({
  "context": "delivery",
  "filters": "{\"searchMetadata\":{\"previousSearchParams\":\"{\\\"PreviousSearchId\\\":\\\"88423b3e-84fa-45f7-8858-8da88dbd2df7\\\",\\\"PreviousSearchFilter\\\":[\\\"{\\\\\\\"category_context\\\\\\\":\\\\\\\"delivery_home\\\\\\\"}\\\",\\\"\\\",\\\"{\\\\\\\"universal_dish_ids\\\\\\\":[\\\\\\\"this_dish_id\\\\\\\"]}\\\"]}\",\"postbackParams\":\"{\\\"processed_chain_ids\\\":[312995,301718,18363082,307893,18549270,20688499,18896958,20607897,20479636],\\\"shown_res_count\\\":9,\\\"search_id\\\":\\\"88423b3e-84fa-45f7-8858-8da88dbd2df7\\\"}\",\"totalResults\":2193,\"hasMore\":true,\"getInactive\":false},\"dineoutAdsMetaData\":{},\"appliedFilter\":[{\"filterType\":\"category_sheet\",\"filterValue\":\"delivery_home\",\"isHidden\":true,\"isApplied\":true,\"postKey\":\"{\\\"category_context\\\":\\\"delivery_home\\\"}\"},{\"filterType\":\"universal_dish_id\",\"filterValue\":\"this_dish_id\",\"isApplied\":true,\"postKey\":\"{\\\"universal_dish_ids\\\":[\\\"this_dish_id\\\"]}\"}],\"urlParamsForAds\":{}}",
  "addressId": 0,
  "entityId": 13142,
  "entityType": "point_of_interest",
  "locationType": "poi",
  "isOrderLocation": 1,
  "cityId": 1,
  "latitude": 28.47212217853559,
  "longitude": 77.07168307901549,
  "userDefinedLatitude": 28.47212217853559,
  "userDefinedLongitude": 77.07168307901549,
  "entityName": "Magicpin, Sector 29, Gurugram",
  "orderLocationName": "Magicpin, Sector 29, Gurugram",
  "cityName": "Delhi NCR",
  "countryId": 1,
  "countryName": "India",
  "displayTitle": "Magicpin",
  "o2Serviceable": True,
  "placeId": "10977",
  "cellId": "4110969650425102336",
  "deliverySubzoneId": 10977,
  "placeType": "DSZ",
  "placeName": "Magicpin, Sector 29, Gurugram",
  "isO2City": True,
  "fetchFromGoogle": False,
  "fetchedFromCookie": True,
  "isO2OnlyCity": False,
  "address_template": [],
  "otherRestaurantsUrl": ""
})
headers = {
  'accept': '*/*',
  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  'content-type': 'application/json',
  'cookie': 'fre=0; rd=1380000; zl=en; fbtrack=98b44c0486df4daf1a5552ec8d308bcb; _gcl_au=1.1.2117769391.1715081867; _fbp=fb.1.1715081868855.644539322; PHPSESSID=acc4a3f2102f16b4cf7bd6a1bb18cd5e; csrf=cd1ca4471fba0e95d3737f11c7940bcf; ak_bmsc=8F1132066C836CC8908662F78C88D700~000000000000000000000000000000~YAAQ5ewsF7kWfO6PAQAAfuDBBRgTGcXSapa87Kk49Yo2IWE+fMhycCyPkqOUfjaGrM7W849GKT+LjiNRKWHv9uMhdJEi0eJkldmcYJJMuEczgMw9QWH5qXM5i2m66A6TY9Ov/5Xl4bnSfggFusPmaVZmxBpBcDLN1G5CApLok8td8GqrbT/rwTNbMp8FrloNuS2L/bbl5AV6dC+GTauQKUK7W2ZfBsBCkpkjBA4SbUZMxJ5K57euq4bOXQMH5xLfMY3poBCtfRXjF5mUhzemqToIwLcTXAdqH419v0L2p4e0S1fQ+r+jjBfodylFBXM/vh/VQd4PljPrEDLpXf+wOH25Hly+b0NonbN+Yjp1gykFAgF5rEMWEnkPhz7oTolxBtUCLoJRyBmOEX4=; _gid=GA1.2.2013746435.1718083511; uspl=true; _ga_MKWDDHF203=GS1.2.1718083513.4.1.1718083623.18.0.0; fbcity=1; ltv=13142; lty=13142; locus=%7B%22addressId%22%3A0%2C%22lat%22%3A28.47212217853559%2C%22lng%22%3A77.07168307901549%2C%22cityId%22%3A1%2C%22ltv%22%3A13142%2C%22lty%22%3A%22point_of_interest%22%2C%22fetchFromGoogle%22%3Afalse%2C%22dszId%22%3A10977%7D; _ga_2XVFHLPTVP=GS1.1.1718083513.12.1.1718088424.58.0.0; _ga=GA1.1.1496351972.1715081867; _gat_global=1; _gat_city=1; _gat_country=1; AWSALBTG=Ep95K3WmJu29tYakIkOKtnbwmN42QiJQqo85xVEoSvWmhs/hz3P5Ul6dYeaHJNxBIehdrWJcx28qEw2v+aB531xdUJ4dZSWwizqvViRT0RtchFOu4m939cKcbouBERZg/GKFI+U1DhJxLNqpbdMR9y6xgid/2LTygtiCZBIHcrBY; AWSALBTGCORS=Ep95K3WmJu29tYakIkOKtnbwmN42QiJQqo85xVEoSvWmhs/hz3P5Ul6dYeaHJNxBIehdrWJcx28qEw2v+aB531xdUJ4dZSWwizqvViRT0RtchFOu4m939cKcbouBERZg/GKFI+U1DhJxLNqpbdMR9y6xgid/2LTygtiCZBIHcrBY; _ga_X6B66E85ZJ=GS1.2.1718083513.8.1.1718088429.60.0.0; _ga_3NH52KS4KE=GS1.2.1718087185.6.1.1718088430.60.0.0; fbcity=1; fbtrack=c3f1ac845b16a327919c0959f84f7cbd; fre=0; rd=1380000; zl=en; AWSALBTG=jcLM3/T3WZS8wV52fBrAJAmn2OEqdV4NBpBkuWrgyW6qW5PbjNqATX0rqQQw2Cs6hdFwL2IXIwnp63aqP2n7IOM2JIm4/zvbdCzhrUOE1B+vQMOuSmyvssZsbdbpVqdXKkyEl6DLei3/7T3+ES8btu0r6c8pt13VEp27x0KZFowV; AWSALBTGCORS=jcLM3/T3WZS8wV52fBrAJAmn2OEqdV4NBpBkuWrgyW6qW5PbjNqATX0rqQQw2Cs6hdFwL2IXIwnp63aqP2n7IOM2JIm4/zvbdCzhrUOE1B+vQMOuSmyvssZsbdbpVqdXKkyEl6DLei3/7T3+ES8btu0r6c8pt13VEp27x0KZFowV',
  'origin': 'https://www.zomato.com',
  'priority': 'u=1, i',
  'referer': f'https://www.zomato.com/ncr/delivery?point_of_interest=13142&dishv2_id={dish_id}',
  'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
  'x-zomato-csrft': 'cd1ca4471fba0e95d3737f11c7940bcf'
}

def update_dish_id(payload, new_dish_id):
    payload_dict = json.loads(payload)
    filters_str = payload_dict["filters"]
    updated_filters_str = filters_str.replace('this_dish_id', new_dish_id)
    
    payload_dict["filters"] = updated_filters_str
    
    return json.dumps(payload_dict)

updated_payload = update_dish_id(payload, dish_id)

payload = json.dumps(json.loads(updated_payload), indent=4)

response = requests.request("POST", url, headers=headers, data=payload)
data = response.json()

if response.status_code == 200:
    merchant_names = []
    sections = data.get('sections', {})
    section_search_result = sections.get('SECTION_SEARCH_RESULT', [])
    for item in section_search_result:
        if item.get('type') == 'restaurant':
            info = item.get('info', {})
            name = info.get('name')
            if name:
                merchant_names.append(name)
    for name in merchant_names:
        print(name)
else:
    print(f"Request failed with status code {response.status_code}")
