import requests
import json


def test_company_name(c_name):

    params = {"mkt": "en-US", "q": '\"'+c_name+'\"'}
    headers = {"Ocp-Apim-Subscription-Key": "f5b07e9bcb874baba117bd9d3b9c4c0a"}
    result = requests.get('https://api.cognitive.microsoft.com/bing/v7.0/entities/', params=params, headers=headers)
    data = result.json()
    print("Data = ", json.dumps(data,indent=2))

    tt = None
    n = None
    result = []

    places = data.get("places", None)
    if places is not None:
        values = places.get("value", None)
        if len(values) >= 1:
            for v in values:
                tt = v["_type"]
                n = v["name"]
                result.append((tt, n, v['address']))

    return result


r = test_company_name("Utah Loan Servicing")
print("Result = ", r)