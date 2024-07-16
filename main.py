import requests
import json
import gspread 
from locality import locality_main
from write_mid_in_sheet import bq_read
from fetch_from_solr import get_lat_lon

SHEET_ID = "1uEudlQ4iGqzIIWkGHkZqOc3VwnPQU8ohyH6vxdqwxII"
SHEET_NAME="locality_details"
URL = "https://www.zomato.com/webroutes/search/home"

def process_gsheet(worksheet, i):
  data_row = worksheet.row_values(i+1)
  locality, city, dish_id = data_row[1], data_row[2], data_row[6]
  lat, lon = get_lat_lon(locality, city)
  print(lat, lon)
  data, z_url = locality_main(lat, lon)
  return z_url, data, dish_id

def modify_url(url, dishv2_id):
    base_url = url.split('?')[0] + '?' #step-1
    if "dine-out" in base_url:
        base_url = base_url.replace("dine-out", "delivery") #step-2
    modified_url = f"{base_url}dishv2_id={dishv2_id}" #step-3
    
    return modified_url

def modify_payload(data, dish_id):
  payload = {
  "context": "delivery",
  "filters": "{\"searchMetadata\":{\"previousSearchParams\":\"{\\\"PreviousSearchId\\\":\\\"30b6284e-d0d6-4ee5-934e-c0bda92f5a4f\\\",\\\"PreviousSearchFilter\\\":[\\\"{\\\\\\\"category_context\\\\\\\":\\\\\\\"delivery_home\\\\\\\"}\\\",\\\"\\\",\\\"{\\\\\\\"universal_dish_ids\\\\\\\":[\\\\\\\"this_dish_id\\\\\\\"]}\\\"]}\",\"postbackParams\":\"{\\\"processed_chain_ids\\\":[],\\\"shown_res_count\\\":9,\\\"search_id\\\":\\\"30b6284e-d0d6-4ee5-934e-c0bda92f5a4f\\\"}\",\"totalResults\":33,\"hasMore\":true,\"getInactive\":false},\"dineoutAdsMetaData\":{},\"appliedFilter\":[{\"filterType\":\"category_sheet\",\"filterValue\":\"delivery_home\",\"isHidden\":true,\"isApplied\":true,\"postKey\":\"{\\\"category_context\\\":\\\"delivery_home\\\"}\"},{\"filterType\":\"universal_dish_id\",\"filterValue\":\"this_dish_id\",\"isApplied\":true,\"postKey\":\"{\\\"universal_dish_ids\\\":[\\\"this_dish_id\\\"]}\"}],\"urlParamsForAds\":{}}"
}
  payload.update(data["locationDetails"])
  payload = json.dumps(payload)
  payload_dict = json.loads(payload)
  filters_str = payload_dict["filters"]
  updated_filters_str = filters_str.replace('this_dish_id', dish_id)
  
  payload_dict["filters"] = updated_filters_str
  m_payload = json.dumps(payload_dict)
  payload = json.dumps(json.loads(m_payload), indent=4)
  return payload

def header_data(ref_url):
  headers = {
  'accept': '*/*',
  'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  'content-type': 'application/json',
  'cookie': 'fre=0; rd=1380000; zl=en; fbtrack=513594a2a8bf4e72576d650214168b2b; _gcl_au=1.1.1370679383.1720095163; _fbp=fb.1.1720095164179.887767891355335593; _ga_VEX4KRY429=GS1.2.1720095799.1.1.1720095827.32.0.0; _ga_MKWDDHF203=GS1.2.1720095847.1.1.1720095979.60.0.0; _ga_9M0GN487BK=GS1.2.1720095735.1.1.1720097159.60.0.0; uspl=true; _gid=GA1.2.712235039.1721027407; _ga_3NH52KS4KE=GS1.2.1721027409.3.1.1721028516.47.0.0; expab=1; dpr=2; _ga_ZVRNMB4ZQ5=GS1.2.1721033604.5.1.1721035868.53.0.0; fbcity=6; ltv=6; lty=6; locus=%7B%22addressId%22%3A0%2C%22lat%22%3A17.366%2C%22lng%22%3A78.476%2C%22cityId%22%3A6%2C%22ltv%22%3A6%2C%22lty%22%3A%22city%22%2C%22fetchFromGoogle%22%3Afalse%2C%22dszId%22%3A1514%2C%22fen%22%3A%22Hyderabad%22%7D; PHPSESSID=ed73cb291a9c277f204026ff4b9fff64; csrf=fefade6b3f239903b0b8aaa206e53733; ak_bmsc=D30A3357B24964A0C0D2D1D4FC96629C~000000000000000000000000000000~YAAQnGPUF+diN7aQAQAAHeQDvRjKyyQJu4yuPH5YQfv+TaNMCFvmFbO0teKBosj/xgUBr7yJE2L+/3+UcTATWXM1OsyqXfKPzbxWnynyYqMO91IOYoPiSPoz3YrrucuQiOQOobPWvJ1wvXdsoxmaXXGet55C20yad2/Ocyi5IkWmZi2u5AIpKOFyfx79bbSk9ug7otZmmDYMHiIu7wotaWVYWR8lGqJ7ImXkRsImRboydJ/yR7zRyvYGCru6SoKWSMXxjrEz23m/b3Ur9OlWPPRhhKhXMoFvnLmLrIRt8BPdfkrMAgkZgnXWaq4vOwtnSErgtgWiNzIv/aFPmUB9ftCEcF40ZZS7nPazQk+T1Z4Un1wyHhP6/uU54kevbLkbTd9DeZRn; _gat_global=1; _gat_city=1; _gat_country=1; _ga_2XVFHLPTVP=GS1.1.1721158067.15.1.1721158078.49.0.0; _ga=GA1.1.1905381440.1720095163; _abck=71FA1397BF05EE82EB0FC5EC01F3D7DC~-1~YAAQnGPUFwFlN7aQAQAAZhsEvQx92ZHR+F+Cq1bFGvwMbo+xw6zBHxVSZKSUITiuc3imY/Oq4QUu3/zkqNtT4YkYZEPeow9CWfttxSMl483IDrcfHGog1NYt9v6sy4t+wn8OPKdjppS9iRAX274mMODJkoDaB8V49UhxTo+/+I6MzbmeWcfl1cd13I468biFk0EV1914uROhIyt7SbCed9kewSuRFZIUdQeooPIKnq93T3yaYHGA/BOW7ILQ7jV0weISvi62PBzGCNLd3ScYOFdcnWQy48j2zKqPbNkxE6h/ol808jmgozfttUDiIPXzp6tMOKERgTj6FO8d8V2o4xfNso70IFmpfZhCM8P9G9NQtKEoRr4wMPPUHJjIOHfpHiWMFGkDOfHQQ+kI~-1~-1~-1; _ga_X6B66E85ZJ=GS1.2.1721158067.10.1.1721158079.48.0.0; AWSALBTG=2Hb8OoezaXlxlalcgaRiOaKt3gO9DV4zClTZwK8lwAFmE8C0wut/IuE4/lcE031NxnQOhYAyqWRKRowQi33NLco/lWOy9d/lHL8lyJvtuZ0JSPh18HpHLyOeI+flcdD8CnGurV5WVeSuOrg3eyVbO9E0MUnDkvdz+aAwYmMLblPe; AWSALBTGCORS=2Hb8OoezaXlxlalcgaRiOaKt3gO9DV4zClTZwK8lwAFmE8C0wut/IuE4/lcE031NxnQOhYAyqWRKRowQi33NLco/lWOy9d/lHL8lyJvtuZ0JSPh18HpHLyOeI+flcdD8CnGurV5WVeSuOrg3eyVbO9E0MUnDkvdz+aAwYmMLblPe; _ga_6HC28B0H9G=GS1.2.1721158067.3.1.1721158079.48.0.0; csrf=7a6f1f7cbc5180f421abf0ae85966298; fre=0; rd=1380000; AWSALBTG=ygGY2cWhq6hUB/VaH1PH0gwIiNxZLkEK1MXUk4eIHYGtPT3an0ZkRcRzOKll795hV3tOgY09uX5RNh9+r9zlxOOlK9/eVBBOJzkXMvVsDG/LQsboK9SYnlRX3e1lgPRRyvLf1T+2iFwbNtFUjDr9KlSTK9u0fCtWstl0tsyeEINX; AWSALBTGCORS=ygGY2cWhq6hUB/VaH1PH0gwIiNxZLkEK1MXUk4eIHYGtPT3an0ZkRcRzOKll795hV3tOgY09uX5RNh9+r9zlxOOlK9/eVBBOJzkXMvVsDG/LQsboK9SYnlRX3e1lgPRRyvLf1T+2iFwbNtFUjDr9KlSTK9u0fCtWstl0tsyeEINX',
  'origin': 'https://www.zomato.com',
  'priority': 'u=1, i',
  'referer': ref_url,
  'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
  'x-zomato-csrft': 'fefade6b3f239903b0b8aaa206e53733'
}
  return headers

def write_in_sheet(worksheet, ids, merchant_names, m_info, index):
   response_col1 = worksheet.find('top_merchants_zomato_id').col
   response_col2 = worksheet.find('merchant_names').col
   response_col3 = worksheet.find('merchant_info').col
   ids_str = str(ids)
   merchant_names_str = str(merchant_names)
   m_info_str = str(m_info)
   worksheet.update_cell(index, response_col1, ids_str)
   worksheet.update_cell(index, response_col2, merchant_names_str)
   worksheet.update_cell(index, response_col3, m_info_str)
   
def mains(payload, headers):
  response = requests.request("POST", URL, headers=headers, data=payload)
  data = response.json()
  merchants, ids = [], []
  if response.status_code == 200:
    sections = data.get('sections', {})
    section_search_result = sections.get('SECTION_SEARCH_RESULT', [])
    for item in section_search_result:
        if item.get('type') == 'restaurant':
            info = item.get('info', {})
            name = info.get('name')
            id = info.get('resId')
            if id:
                ids.append(id)
            if name:
              merchants.append(name)
  else:
    print(f"Request failed with status code {response.status_code}")
    merchants[response.status_code] = "Security Error in crawling"
  return ids, merchants

if __name__=="__main__":
    gs = gspread.service_account(filename="/etc/gspread/service_account.json")
    sh = gs.open_by_key(SHEET_ID)
    worksheet = sh.worksheet(SHEET_NAME)
    row_count = len(worksheet.get_all_values())
    for i in range(1, row_count):
      try:
        z_url, data, dish_id = process_gsheet(worksheet, i)
        ref_url = modify_url(z_url, dish_id)
        payload = modify_payload(data, dish_id)
        header = header_data(ref_url)
        ids, merchants = mains(payload, header)
        m_info = bq_read(ids)
        write_in_sheet(worksheet, ids,  merchants, m_info, i+1)
      except:
         continue
      


