import csv
import logging
import os
import sys
from copy import deepcopy
from os import environ
import time
import json 

import requests
import ujson
from urllib.parse import urlencode

logger = logging.getLogger("locality_crawl")
csrf_data = {}

home_url = "https://www.zomato.com"
location_url = "https://www.zomato.com/webroutes/location/get?lat={lat}&lon={lon}"
locality_page_url = "https://www.zomato.com/webroutes/search/applyFilter"
csrf_url = "https://www.zomato.com/webroutes/auth/csrf"

zomato_headers = {
    # 'Host': 'www.zomato.com',
    # 'Origin': 'https://www.zomato.com',
    # 'Referer': 'https://www.zomato.com/',
    'Accept': '*/*',
    'Accept-Language': 'en-gb',
    'Connection': 'keep-alive',
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15'
    'User-Agent': os.getenv("ZOMATO_USER_AGENT", 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'),
    'User-Agent': "PostmanRuntime/7.28.3"
}
feed = {
    "url": "",
    "appid": "crawler-service",
    "crawlid": "locality_crawl_final_1",
    "spiderid": "zomato",
}


user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
]
USER_AGENT = os.environ.get("USER_AGENT", user_agents[2])

def req(
    url,
    method="get",
    params=None,
    data=None,
    json=None,
    files=None,
    headers={},
    timeout=30,
    get_json=False,
    raise_exception=False,
    raise_for_status=True,
    cookies=None,
):
    if "User-Agent" not in headers and "user-agent" not in headers and USER_AGENT:
        headers["User-Agent"] = USER_AGENT
    res = None
    try:
        res = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            files=files,
            headers=headers,
            timeout=timeout,
            cookies=cookies,
        )
        if raise_for_status:
            res.raise_for_status()
        if get_json:
            return res.json(), None
        return res, None
    except Exception as e:
        if raise_exception:
            raise e
        return res, e

crawler_rest_endpoint = environ.get(
    "CRAWLER_REST_ENDPOINT", "http://10.140.0.224:5343/feed"
)

def get_csrf():
    try:
        csrf_data = {}
        response_csrf = requests.request(
            method='GET', url=csrf_url, headers=zomato_headers)
        response_csrf.raise_for_status()
        csrf_data = ujson.loads(response_csrf.text)
        csrf_data["PHPSESSID"] = response_csrf.cookies.get("PHPSESSID")
        # logger.info(f"got csrf data : {csrf_data}")
    except Exception as e:
        logger.error(f"Error while getting csrf: {e}")
        return
    if not csrf_data.get("csrf"):
        logger.errort(f"CSRF not in csrf data: {csrf_data}")
        return
    if not csrf_data.get("PHPSESSID"):
        logger.error(f"PHPSESSID not in csrf data: {csrf_data}")
        return
    return csrf_data


def main():
    csrf_data = get_csrf()
    print(csrf_data)
    locality_list = {}
    # with open('locality_list.csv') as csv_file1:
    #     csv_reader = csv.DictReader(csv_file1, delimiter=',')
    #     for i, row in enumerate(csv_reader):
    #         locality_list[row["id"]]=row
    # with open('locality_zomato.csv') as csv_file2:
    # with open('locality_list.csv') as csv_file2:
    #     csv_reader = csv.DictReader(csv_file2, delimiter=',')
    #     for i, row in enumerate(csv_reader):
    #         if (i+1) % 20 == 0:
    #             time.sleep(300)
    #             # lat=""
    #             # lon=""
    #         # locality = locality_list[row["LOCALITY_ID"]]'
    #         print(i)
    #         print(row)
    lat = 28.47205116 #row["lat"]
    lon = 77.07171601 #row["lon"]
    url = location_url.format(lat=lat, lon=lon)
    response = requests.request(
        method="GET", url=url, headers=zomato_headers)
    data = ujson.loads(response.text)
    print("data", data)
    payload = data.get("locationDetails", {})
    # print(payload)
    # if i % 25 == 0:
    # csrf_data = get_csrf()
    if not csrf_data:
        logger.error('Could not get csrf data')
        return
    headers = zomato_headers.copy()
    headers["x-zomato-csrft"] = csrf_data["csrf"]
    headers["content-type"] = "application/json"
    # cookies = {"PHPSESSID": csrf_data["PHPSESSID"]}
    headers['Cookie'] = f'PHPSESSID={csrf_data["PHPSESSID"]};'
    response = requests.post(
        url=locality_page_url, headers=headers, json=payload)
    data = ujson.loads(response.text)
    json_string = json.dumps(data)
    with open("f.json", "w") as f:
        f.write(json_string)
    url = data.get("pageInfo", {}).get("pageUrl", "")
    if not url:
        logger.error("locality url not found")
        # continue
    feed["url"] = home_url+url
    print("feed", feed)
    print(feed["url"])
    print("crawler: ", crawler_rest_endpoint)
    # res, err = req(crawler_rest_endpoint, method="POST",
    #                 json=feed, get_json=True)
    # print(res)
    # if err:
    #     logger.error(f"error: {err}")
    # else:
    #     logger.info(f"result: {res}")


if __name__ == "__main__":
    sys.exit(main())
