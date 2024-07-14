import requests
import json
import gspread 
from locality import locality_main
import os

SHEET_ID = "1uEudlQ4iGqzIIWkGHkZqOc3VwnPQU8ohyH6vxdqwxII"
SHEET_NAME="locality_details"
URL = "https://www.zomato.com/webroutes/search/home"

def process_gsheet():
  gs = gspread.service_account(filename="/etc/gspread/service_account.json")
  sh = gs.open_by_key(SHEET_ID)
  worksheet = sh.worksheet(SHEET_NAME)
  data_row = worksheet.row_values(2)
  lat, lon, dish_id = data_row[1], data_row[2], data_row[4]

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
    'cookie': 'fre=0; rd=1380000; zl=en; fbtrack=513594a2a8bf4e72576d650214168b2b; _gcl_au=1.1.1370679383.1720095163; _fbp=fb.1.1720095164179.887767891355335593; _ga_VEX4KRY429=GS1.2.1720095799.1.1.1720095827.32.0.0; _ga_MKWDDHF203=GS1.2.1720095847.1.1.1720095979.60.0.0; _ga_9M0GN487BK=GS1.2.1720095735.1.1.1720097159.60.0.0; uspl=true; _gid=GA1.2.395819178.1720851974; _ga_ZVRNMB4ZQ5=GS1.2.1720851975.3.1.1720851985.50.0.0; _ga_3NH52KS4KE=GS1.2.1720854275.1.1.1720854286.49.0.0; fbcity=11456; ltv=172913; lty=172913; locus=%7B%22addressId%22%3A0%2C%22lat%22%3A18.4386%2C%22lng%22%3A79.1288%2C%22cityId%22%3A11456%2C%22ltv%22%3A172913%2C%22lty%22%3A%22subzone%22%2C%22fetchFromGoogle%22%3Afalse%2C%22dszId%22%3A38310%7D; PHPSESSID=487ccba788d2a91d6dc72f5bf2f8515e; csrf=c7261272fc8ece1366159e4d1db93ab1; ak_bmsc=371E95F303D94E2CB4111AD594218FDE~000000000000000000000000000000~YAAQlWPUF5wyOZqQAQAA5bJIrRhsusIrmcm3XkRAAqVVxPRYXrcTWS9TN1jSpLYkBPwQ9ML4jz4wodknttbpqR9pKeQgBGk5sLJwFE2BR3KC9PHFUnNtqL4v8QUuCGWJQRUz9ZoexM/XsHkiPq8fMTwrI0BfsWhAveGKbRTWszhRCtf/gcjPVYSPBIOVhNKDRqTyz+295cEAKcCdsd7xyTxadyYVPyAr+3wZ9dN1Uob8o4LHj9dqHmJ1RQIz5HnpDNjseY5PX5a82tcG2LBHSuvS2LW+Ur7waE2FgDf/v2J8zj7FA+y2VGdXcS93wcYakDyB/wFtRjGrUMmqxhf7vHwsu88j0kIBbTkRmBjFYzyhxR6kR0dZrdznVTwqhmM0+BwZn7ST; _gat_global=1; _gat_country=1; _ga_2XVFHLPTVP=GS1.1.1720894142.7.1.1720894154.48.0.0; _ga=GA1.1.1905381440.1720095163; _abck=71FA1397BF05EE82EB0FC5EC01F3D7DC~-1~YAAQlWPUFws1OZqQAQAAWexIrQxCMeVdCGte/1J27JC0blQ1CjdJ1nJ+dhtlyq/gNBwbYReBwvReutHP/t6r4/tbcMDOFg8ybfqrx488k9YJikCfKCSZumVLAdWBLffP93k5s11r/YBg/TFCEUmUAZEOn4e3GNz52oiQL6rDQ02CgdS5BUU5ziS2q7aufpVEUtn1MrxFas+x6F7pPkEMDO5TE8VDR099QiW+pKkhs1GZhk6atcXBKhmMKKVcidFOq49/oMteF3uiePE7fghVwylIm2ELXUvrcI/6Dch9tT0s+KTOyiTOnwhCWSWhjU8uk1jeHsC1L0Z087PfSWjNRt7p2EDqARS/lsLuBmN9cuLUOvQjYUjOx/TubQAOb9aLqpsiCUEYfK1qowLN~-1~-1~-1; AWSALBTG=Q16GmjrPraumI42Wf+P5E8ACWSNqYpL14nDyokPMgUF1RQ7x3bKXBizUOI1RTSgqqQtt5CsitSca/kk81g7IM9RwYBVWukN3oUlChpSwM/PsJtNm4iuIcATCmsbwKqC5/7m60nFdDSIi+gan7IO7MGrKWSX2IDpz7Kxd0tJONynW; AWSALBTGCORS=Q16GmjrPraumI42Wf+P5E8ACWSNqYpL14nDyokPMgUF1RQ7x3bKXBizUOI1RTSgqqQtt5CsitSca/kk81g7IM9RwYBVWukN3oUlChpSwM/PsJtNm4iuIcATCmsbwKqC5/7m60nFdDSIi+gan7IO7MGrKWSX2IDpz7Kxd0tJONynW; _ga_X6B66E85ZJ=GS1.2.1720894142.5.1.1720894156.46.0.0; fre=0; rd=1380000; AWSALBTG=u8pZWS370Ou0J3JzuKgCBTn8H11M0SSTdjAYQJCgf9hEymvyU/vGjQgzbNEIZDfMyEZ1u0Qb3XX/W7+RVBgpN/9pOMdaY3JEz95FDbisF3sQFEBnpS8aS+1AijXaIKmmlc0my2CGIdDr+ShGFuycD5bioMp+K4U7jnbvtcabvWNT; AWSALBTGCORS=u8pZWS370Ou0J3JzuKgCBTn8H11M0SSTdjAYQJCgf9hEymvyU/vGjQgzbNEIZDfMyEZ1u0Qb3XX/W7+RVBgpN/9pOMdaY3JEz95FDbisF3sQFEBnpS8aS+1AijXaIKmmlc0my2CGIdDr+ShGFuycD5bioMp+K4U7jnbvtcabvWNT',
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
    'x-zomato-csrft': 'c7261272fc8ece1366159e4d1db93ab1'
  }
  return headers

def mains(payload, headers):
  response = requests.request("POST", URL, headers=headers, data=payload)
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

if __name__=="__main__":
    z_url, data, dish_id = process_gsheet()
    ref_url = modify_url(z_url, dish_id)
    payload = modify_payload(data, dish_id)
    header = header_data(ref_url)
    mains(payload, header)

