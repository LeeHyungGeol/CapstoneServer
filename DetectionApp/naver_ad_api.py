import urllib.request
import json



def getAdvertisement(query_list):

    client_id= 'mibzCc7PHbQ0Oyo9rqti'
    client_secret= 'a2HGywvUmd'
    query_list = query_list

    adv_results = list()
    for query in query_list:

        query = urllib.parse.quote(query)
        print(query)

        url = 'https://openapi.naver.com/v1/search/shop.json?query=' + query +'&sort=sim'
        print(url)

        request = urllib.request.Request(url)
        request.add_header('X-Naver-Client-Id', client_id)
        request.add_header('X-Naver-Client-Secret', client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body= response.read()
            body = response_body.decode('utf-8')
            data = json.loads(body)
            items = data['items']

            for item in items:
                adv_results.append({

                    'title' : item['title'],
                    'link' : item['link'],
                    'image' : item['image'],
                    'lprice' : item['lprice'],
                    'hprice' : item['hprice']
                })
                break

        else:
            print("Error Code:" + rescode)

    print('size: ', len(adv_results))
    print('result: ', adv_results)

    return adv_results