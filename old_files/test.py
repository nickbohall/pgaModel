import http.client

conn = http.client.HTTPSConnection("api.datagolf.ca")

payload = ""

headers = {
    'authority': "api.datagolf.ca",
    # 'sec-ch-ua': " Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99",
    'sec-ch-ua-mobile': "?0",
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
    'sec-ch-ua-platform': "Linux",
    'accept': "*/*",
    'sec-fetch-site': "cross-site",
    'sec-fetch-mode': "no-cors",
    'sec-fetch-dest': "script",
    'referer': "https://datagolf.com/",
    'accept-language': "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7"
    }

conn.request("GET", "/dg-api/v1/get_ch_data?callback=callback&course_num=ch_14&_=1653430328619&=", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))