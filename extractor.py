import requests
import json

url = "https://www.zomato.com/webroutes/search/home"
dish_id = int(input())
payload = json.dumps({
  "context": "delivery",
  "filters": "{\"searchMetadata\":{\"previousSearchParams\":\"{\\\"PreviousSearchId\\\":\\\"8c93d6cd-d39f-41c8-866c-c0c4ee13b4cb\\\",\\\"PreviousSearchFilter\\\":[\\\"{\\\\\\\"category_context\\\\\\\":\\\\\\\"delivery_home\\\\\\\"}\\\",\\\"\\\",\\\"{\\\\\\\"universal_dish_ids\\\\\\\":[\\\\\\\"30308\\\\\\\"]}\\\"]}\",\"postbackParams\":\"{\\\"processed_chain_ids\\\":[18349892,300988,147,20483826,312123,305120,18558572,18843927,20644918],\\\"shown_res_count\\\":9,\\\"search_id\\\":\\\"8c93d6cd-d39f-41c8-866c-c0c4ee13b4cb\\\"}\",\"totalResults\":1233,\"hasMore\":true,\"getInactive\":false},\"dineoutAdsMetaData\":{},\"appliedFilter\":[{\"filterType\":\"category_sheet\",\"filterValue\":\"delivery_home\",\"isHidden\":true,\"isApplied\":true,\"postKey\":\"{\\\"category_context\\\":\\\"delivery_home\\\"}\"},{\"filterType\":\"universal_dish_id\",\"filterValue\":\"30308\",\"isApplied\":true,\"postKey\":\"{\\\"universal_dish_ids\\\":[\\\"30308\\\"]}\"}],\"urlParamsForAds\":{}}",
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
  "fetchedFromCookie": False,
  "isO2OnlyCity": False,
  "address_template": [],
  "otherRestaurantsUrl": ""
})

# print(payload)

def update_dish_id(payload, new_dish_id):
    # Load the payload JSON
    payload_dict = json.loads(payload)

    # Parse the filters field which is a JSON string
    filters = json.loads(payload_dict["filters"])

    # Update dish_id in previousSearchParams
    search_metadata = json.loads(filters["searchMetadata"]["previousSearchParams"])
    for i, item in enumerate(search_metadata["PreviousSearchFilter"]):
        if "universal_dish_ids" in item:
            item_dict = json.loads(item)
            item_dict["universal_dish_ids"] = [new_dish_id]
            search_metadata["PreviousSearchFilter"][i] = json.dumps(item_dict)
    filters["searchMetadata"]["previousSearchParams"] = json.dumps(search_metadata)

    # Update dish_id in appliedFilter
    for applied_filter in filters["appliedFilter"]:
        if applied_filter["filterType"] == "universal_dish_id":
            applied_filter["filterValue"] = new_dish_id
            post_key = json.loads(applied_filter["postKey"])
            post_key["universal_dish_ids"] = [new_dish_id]
            applied_filter["postKey"] = json.dumps(post_key)

    # Convert filters back to string and update payload
    payload_dict["filters"] = json.dumps(filters)
    return json.dumps(payload_dict)

# Update the payload with the new dish_id
updated_payload = update_dish_id(payload, dish_id)

# print(updated_payload)
# dish_id = int(input())
headers = {
  'accept': '*/*',
  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  'content-type': 'application/json',
  'cookie': 'fre=0; rd=1380000; zl=en; fbtrack=98b44c0486df4daf1a5552ec8d308bcb; _gcl_au=1.1.2117769391.1715081867; _fbp=fb.1.1715081868855.644539322; PHPSESSID=acc4a3f2102f16b4cf7bd6a1bb18cd5e; csrf=cd1ca4471fba0e95d3737f11c7940bcf; ak_bmsc=8F1132066C836CC8908662F78C88D700~000000000000000000000000000000~YAAQ5ewsF7kWfO6PAQAAfuDBBRgTGcXSapa87Kk49Yo2IWE+fMhycCyPkqOUfjaGrM7W849GKT+LjiNRKWHv9uMhdJEi0eJkldmcYJJMuEczgMw9QWH5qXM5i2m66A6TY9Ov/5Xl4bnSfggFusPmaVZmxBpBcDLN1G5CApLok8td8GqrbT/rwTNbMp8FrloNuS2L/bbl5AV6dC+GTauQKUK7W2ZfBsBCkpkjBA4SbUZMxJ5K57euq4bOXQMH5xLfMY3poBCtfRXjF5mUhzemqToIwLcTXAdqH419v0L2p4e0S1fQ+r+jjBfodylFBXM/vh/VQd4PljPrEDLpXf+wOH25Hly+b0NonbN+Yjp1gykFAgF5rEMWEnkPhz7oTolxBtUCLoJRyBmOEX4=; _gid=GA1.2.2013746435.1718083511; uspl=true; _ga_MKWDDHF203=GS1.2.1718083513.4.1.1718083623.18.0.0; _gat_global=1; _gat_country=1; fbcity=1; ltv=13142; lty=13142; locus=%7B%22addressId%22%3A0%2C%22lat%22%3A28.47212217853559%2C%22lng%22%3A77.07168307901549%2C%22cityId%22%3A1%2C%22ltv%22%3A13142%2C%22lty%22%3A%22point_of_interest%22%2C%22fetchFromGoogle%22%3Afalse%2C%22dszId%22%3A10977%7D; _ga_2XVFHLPTVP=GS1.1.1718083513.12.1.1718083680.24.0.0; _ga=GA1.1.1496351972.1715081867; _gat_city=1; _ga_X6B66E85ZJ=GS1.2.1718083513.8.1.1718083682.21.0.0; _ga_3NH52KS4KE=GS1.2.1718083682.5.0.1718083682.60.0.0; AWSALBTG=PtENTFfjpUeO6U5iTX3EuO67OMzkf6VgX6UPRg87h1SYWZ6P+GyX9Jbvab02ZH3/zaaYeyLrF+rTdQeICQCVrmaMkqWWbzNyeXTiSCvgMSzQsRRwC7hE5WLxG2gqYAedQ3+sWwUyuAM9bnZ0T6YJ+TbALEcZyeqv4M6z5HF0l6kU; AWSALBTGCORS=PtENTFfjpUeO6U5iTX3EuO67OMzkf6VgX6UPRg87h1SYWZ6P+GyX9Jbvab02ZH3/zaaYeyLrF+rTdQeICQCVrmaMkqWWbzNyeXTiSCvgMSzQsRRwC7hE5WLxG2gqYAedQ3+sWwUyuAM9bnZ0T6YJ+TbALEcZyeqv4M6z5HF0l6kU; fbcity=1; fbtrack=c3f1ac845b16a327919c0959f84f7cbd; fre=0; rd=1380000; zl=en; AWSALBTG=PfWrte5V5FdBQpCVifRujhIbwq/emxYOLnvxV61GcihyatH2OnBzdx0vkrBoPSItwzFd2Yvbo5TAEZSfabaMOKGNgQuohh2vwsm+/kKrt7rqQhPYh0t4lxmNOb8ts7/4T5YZG2FGTKLaQwtGnU5EHBNO3aTDaOzXJRMQTjXKgYIG; AWSALBTGCORS=PfWrte5V5FdBQpCVifRujhIbwq/emxYOLnvxV61GcihyatH2OnBzdx0vkrBoPSItwzFd2Yvbo5TAEZSfabaMOKGNgQuohh2vwsm+/kKrt7rqQhPYh0t4lxmNOb8ts7/4T5YZG2FGTKLaQwtGnU5EHBNO3aTDaOzXJRMQTjXKgYIG',
  'origin': 'https://www.zomato.com',
  'priority': 'u=1, i',
  'referer': 'https://www.zomato.com/ncr/delivery?point_of_interest=13142&dishv2_id=30308',
  'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
  'x-zomato-csrft': 'cd1ca4471fba0e95d3737f11c7940bcf'
}

response = requests.request("POST", url, headers=headers, data=updated_payload)

# print(response.text)
print(type(response))
data = response.json()

# print(sec)
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
# json_string = json.dumps(response.text)
# with open("f1.json", "w") as f:
#     f.write(json_string)
# print("completed !")
