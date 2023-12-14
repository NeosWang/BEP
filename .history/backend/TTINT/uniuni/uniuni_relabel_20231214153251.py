import requests
import json
from datetime import datetime



def __connect_uni_ca(barcode, alternative, yyyymmdd, hhmmss):
    myUrl = "https://partners.postnl.post/api/v1/carrier/uniuni/events"

    api_key = "7FHjG3jwd7Tadyy8TFnQg9mFGJYHVhbWhZuCpRXnQp47gNwzUiafcxywC41rFKcT2QriKzmHGYd4PJZpuiZUpEidAOaIHnigsRaq7Cg0vMYygQdgqxwffvAABIR0vjYRSEiHHf2lZNznu1lkNP6dlmR0leyb7ib6TsMmifacQBOQet2JLgRLzs0QqdHtdHvUZErzEJGNwjUsVPrE7w2cnyG3imXTmVNelNb27H3EngLKOzv22eIk11Qkv60ZkwUOZiJk6BAZDXIJvJ25drtodLcN0aMlOy6mc4nmoP2bkaxc"

    order_sn = datetime.now().strftime('%Y%m%d%H%M%S%f')
    payload = [
        {
            "id": 178183394,
            "order_id": 19450505,
            "code": "ORDER_RECEIVED",
            "pathAddr": "UNI DATA CENTER",
            "pathInfo": f"Transshipment completed. Canada Post TNO: {alternative}",
            "pathTime": 1688887857,
            "traceSeq": 0,
            "staff_id": None,
            "scan_lat": None,
            "scan_lng": None,
            "is_updated": 0,
            "operate_warehouse": None,
            "exception": 0,
            "order_sn": order_sn,
            "lat": "43.648241",
            "lng": "-79.3891052",
            "shipper": alternative,
            "state": 217,
            "warehouse": 2,
            "pathAddress": "UNI DATA CENTER",
            "description_en": "Order received",
            "tno": barcode,
            "tracking_number": barcode,
            "data_source": "uniuni",
            "internal_account_number": None,
            "city": "",
            "province": "",
            "country": "CA",
            "postal_code": "",
            "pathTimeGMT": f"{yyyymmdd} {hhmmss}",
            "pathTimeZone": "America/Toronto",
            "pod_images": None,
            "DateAndTime": f"{yyyymmdd}T{hhmmss}+00:00"
        }
    ]

    res = requests.post(
        url=myUrl,
        headers={
            'api_key': api_key,
            'Content-Type': 'application/json'
        },
        data=json.dumps(payload),
    )
    
    status_code = res.status_code
    return status_code if status_code == 200 else res.text

def __get_list(s):
    l = s.split('\n')
    l = [i.replace(' ', '') for i in l if len(i.strip())]
    return [i.split('=') for i in l]


def run(param):
    output = []
    list = __get_list(param['txt'])
    yyyymmdd, hhmmss= param['utc'].split('T')
    for barcode, alternative, in list:
        res =  __connect_uni_ca(barcode, alternative, yyyymmdd=yyyymmdd, hhmmss=hhmmss)
        output.append( f"{barcode}={alternative} : {res}" )    
    return {
        "res" : '\n'.join(output)
    }


