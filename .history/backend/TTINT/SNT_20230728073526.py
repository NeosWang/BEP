import requests
import json
from random import randint
import hashlib
import base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def __random_LP():
    return f"LP{__random_n_digits(14)}"

def __random_CB():
    return f"CB{__random_n_digits(14)}"

def __get_data_digest(app_json, secretKey="postnl13798642"):
    app_bytes = (app_json + secretKey).encode(encoding='UTF-8')
    md5 = hashlib.md5(app_bytes)
    return base64.b64encode(md5.digest()).decode("UTF-8")

def __random_mawb():
    airline = __random_n_digits(3)
    seq = __random_n_digits(7)
    return f"{airline}-{seq}{seq%7}"
def random_mawb():
    airline = __random_n_digits(3)
    seq = __random_n_digits(7)
    return f"{airline}-{seq}{seq%7}"

def __random_n_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)





# region [__barcode_generate]
def __barcode_generate(prefix):
    test_SNT = "2qQu3xg6e8w13J4uWyJDHp0TmRV2SPZnK7R3IAgfzb3RLIYt5qHjosDN9o6V2fkrBg77czDsTc8DgOHVC7swplLatjX2lLXWRPvCvRB5eDfOc2COUuO6uGgtSM5hzzZ6rUMV1Q19iYUu3PuIHq637gGn4GU0KJVGG99phX0aHcKwNKGQm47V0YNopmm8bWiwrsnFyKzZ3wwl1HiPJjc1xxJxGHyDTk4RlYVZCg0TnF6k4Yj8699D1qxJ8VeG45ImcwLvNeDJNaWuVRbPf8hrfSUkwII8E8ID8pbk5DF7ff5Z"

    url = "https://clients-test.postnl.a02.cldsvc.net/v7/api/barcode/generate"

    headers = {
        'api_key': test_SNT,
        "Content-Type": 'application/json'
    }
    payload = {
        "barcode_type": prefix,
        "amount_of_barcodes": 1
    }
    res = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(payload),
        verify=False
    )

    return json.loads(res.text)['data']['barcode_and_rfids'][0]['barcode']
# endregion

# region [__assistlabel_generate]
def __assistlabel_generate():
    test_SNT = "2qQu3xg6e8w13J4uWyJDHp0TmRV2SPZnK7R3IAgfzb3RLIYt5qHjosDN9o6V2fkrBg77czDsTc8DgOHVC7swplLatjX2lLXWRPvCvRB5eDfOc2COUuO6uGgtSM5hzzZ6rUMV1Q19iYUu3PuIHq637gGn4GU0KJVGG99phX0aHcKwNKGQm47V0YNopmm8bWiwrsnFyKzZ3wwl1HiPJjc1xxJxGHyDTk4RlYVZCg0TnF6k4Yj8699D1qxJ8VeG45ImcwLvNeDJNaWuVRbPf8hrfSUkwII8E8ID8pbk5DF7ff5Z"

    url = "https://clients-test.postnl.a02.cldsvc.net/v7/api/assistlabel/generate"

    headers = {
        'api_key': test_SNT,
        "Content-Type": 'application/json'
    }
    payload = {
        "label_type": "ZPL",
        "destination_country_code": "YY"
    }
    res = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(payload),
        verify=False
    )

    return json.loads(res.text)['data']['assist_labels'][0]['barcode']
# endregion

# region [__declare_item_logistics]
def __declare_item_logistics(product, barcode, lpcode, mailbag=None):

    url = "https://clients-test.postnl.a02.cldsvc.net/v7/api/declare/ItemLogistics"

    obj_logistics_interface = {

        "logisticsOrderCode": lpcode,
        "sender": {
            "imID": "aliqatest01",
            "name": "test",
            "phone": "15",
            "zipCode": "510440",
            "address": {
                "country": "China",
                "province": "guang dong sheng",
                "city": "guang zhou shi",
                "district": "bai yun qu",
                "detailAddress": "bai yun hu jie dao~~~test"
            },
            "storeName": "woshizhendexiangxiaoa Store"
        },
        "receiver": {
            "imID": "aliqatest01",
            "name": "test",
            "phone": "90",
            "mobile": "3090",
            "email": "test@hotmail.com",
            "zipCode": "3542AD",
            "address": {
                "country": "ES",
                "province": "North Holland",
                "city": "Hilversum",
                "district": "",
                "detailAddress": "test"
            },
            "areaId": "147"
        },
        "parcel": {
            "weight": "21",
            "weightUnit": "g",
            "suggestedWeight": "150",
            "price": "100",
            "priceUnit": "CENT",
            "bigBagID": mailbag,
            "parcelQuantity": "1",
            "bigBagWeight": "1300",
            "bigBagWeightUnit": "g",
            "priceCurrency": "USD",
            "goodsList": [
                {
                    "productID": "1005003287773002",
                    "name": "Skirts",
                    "cnName": "半身裙",
                    "categoryID": "200000361",
                    "categoryName": "Jeans",
                    "categoryCNName": "半身裙",
                    "categoryFeature": "03",
                    "price": "100",
                    "itemPrice": "0",
                    "priceUnit": "CENT",
                    "priceCurrency": "USD",
                    "declarePrice": "100",
                    "quantity": "1",
                    "url": "http://www.aliexpress.com/item//1005003287773002.html",
                    "productCategory": "Women's Clothing|Jeans",
                    "weight": "10",
                    "weightUnit": "g",
                    "suggestedCNName": "半身裙",
                    "suggestedENName": "Skirts"
                }
            ]
        },
        "customs": {
            "declarePriceTotal": "100"
        },
        "returnParcel": {
            "imID": "aliqatest01",
            "name": "测试",
            "phone": "18267170490",
            "mobile": "18267170490",
            "undeliverableOption": "2",
            "zipCode": "333333",
            "address": {
                "country": "中国",
                "province": "浙江省",
                "city": "杭州市",
                "district": "上城区",
                "detailAddress": "清波街道~~~测试地址，别揽收"
            }
        },
        "trade": {
            "tradeID": "8138625187603669",
            "price": "2156",
            "priceUnit": "CENT",
            "priceCurrency": "USD",
            "purchaseTime": "2023-02-23 18:46:53"
        },
        "outboundTime": "2023-03-01 14:22:48",
        "trackingNumber": barcode,
        "waybillnumber": barcode,
        "preCPResCode": "TRUNK_30757958",
        "currentCPResCode": "DISTRIBUTOR_31037258",
        "nextCPResCode": "",
        "interCPResCode": "DISTRIBUTOR_31037258",
        "routingTrial": "1",
        "bizType": "AE_4PL_STANDARD",
        "cloudPrintData": "{\"encryptedData\":\"AES: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\",\"signature\":\"MD:6iO1XfU7NuLMLjGitNa+fQ==\",\"templateURL\":\"http://cloudprint.cdn.cainiao.com/cloudprint/template/getStandardTemplate.json?template_id=596907\",\"ver\":\"\"}",
        "mailBoxItem": product['mailBoxItem'],
        "laneCode": product['laneCode'],
        "insuranceInfo": "",
        "fromHubResCode": "DISTRIBUTOR_31037258",
        "isConso": "false",
        "transitSortCode": "CC_NL",
        "logisticsAbilities": "[\"PA_DOOR_DELIVERY\",\"PA_CATEGORY_BATTERY\",\"PA_CLEARANCE_PAID\",\"PA_DOOR_PICKUP\"]"
    }

    lpcode = obj_logistics_interface['logisticsOrderCode']

    str_logistics_interface = json.dumps(obj_logistics_interface)
    payload = {
        "data_digest": __get_data_digest(str_logistics_interface),
        "partner_code": product['customs_gate'],
        "from_code": "Bifrost",
        "msg_type": "CAINIAO_GLOBAL_LASTMILE_ASN",
        "msg_id": lpcode,
        "logistics_interface": str_logistics_interface
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    res = requests.post(
        url=url,
        headers=headers,
        data=payload,
        verify=False,
    )
    return {"data":res.text}
# endregion

# region [__declare_item_customs]
def __declare_item_customs(req,product,barcode,lpcode,cbcode,mailbag=None,):

    url = "https://clients-test.postnl.a02.cldsvc.net/v7/api/declare/item"

    feature = {
        "linehaulResCode": "TRUNK_30145010",
        "declarationRole": f"warehouse{'' if product['source_code']=='DISTRIBUTOR_30875031' else 'nooit'}",
        "laneCode": "L_AE_ECONOMY_NLAIR_RM",
        "distributorResCode": product['source_code']
    }
    feature = json.dumps(feature)

    obj_content = {
        "actualTotalFee": "11.182258826765352",
        "appApi": "declare",
        "appType": "2",
        "applyTime": "20220908135506+0200",
        "bagId": mailbag,
        "copNo": cbcode,
        "currency": "EUR",
        "declareCountry": "NL",
        "feature":  feature,
        "featureMap": {
            "linehaulResCode": "TRUNK_30145010",
            "laneCode": "L_AE_ECONOMY_NLAIR_RM",
            "distributorResCode": product['source_code']
        },
        "freight": "0.00000",
        "fromCountry": "CN",
        "goodsValue": "100",
        "grossWeight": str(req["gross_weight_grams"]/1000),
        "guid": "06cc5dc1-0730-4728-9445-a4afe0c2b802",
        "ieFlag": "I",
        "iossNo": "ulh6BfWfQ+0u3wZ37TjwdA==",
        "itemList": [
            {
                "country": "CN",
                "currency": "EUR",
                "featureMap": {},
                "gcode": "5705008099",
                "gmodel": "None",
                "gnum": 1,
                "grossWeight": str(req["gross_weight_grams"]/1000),
                "itemName": "Non-Slip Mat",
                "itemNo": "1005004575464964_1",
                "netWeight": str(req["gross_weight_grams"]/1000),
                "price": "14.03000",
                "productUrl": "http://www.aliexpress.com/item//1005004575464964.html",
                "qty": "1",
                "status": "online",
                "taxRate": "0.22",
                "totalFreight": "0.00000",
                "totalPrice": "14.03000",
                "totalTax": "3.09000",
                "unitFreight": "0.00000",
                "unitTax": "3.09000"
            }
        ],
        "logisticsCode": lpcode,
        "netWeight": str(req["gross_weight_grams"]/1000),
        "orderNo": "",
        "receiverInfo": {
            "name": req['addressee_details']['name'] if 'name' in req['addressee_details'] else "tester",
            "address": req['addressee_details']['address'] if 'address' in req['addressee_details'] else "test addr",
            "city": req['addressee_details']['city'] if 'city' in req['addressee_details'] else "test city",
            "country": req['addressee_details']['country_code'],
            "zipCode": req['addressee_details']['country_code'],
            "email": req['addressee_details']['email'] if 'email' in req['addressee_details'] else "a@b.c",
            "telephone": req['addressee_details']['phone']if 'phone' in req['addressee_details'] else "123456789",
        },
        "senderInfo": {
            "address": "dong sheng jie dao~~~test address",
            "city": "ning bo shi",
            "country": "CN",
            "district": "",
            "mobilePhone": "",
            "name": "N",
            "state": "Xicheng District",
            "telephone": "0031 999 99999",
            "zipCode": "200082",
            "storeName": "Nalta"
        },
        "taxTotal": 1.1,
        "wayBillNo": barcode
    }

    str_content = base64.b64encode(json.dumps(
        obj_content).encode(encoding='ascii')).decode("UTF-8")

    obj_logistics_interface = {
        "bizType": "CUSTOMS_SMALLPACKAGE_NOTIFY",
        "bizKey": cbcode,
        "formatType": "1",
        "content": str_content
    }

    str_logistics_interface = json.dumps(obj_logistics_interface)

    payload = {
        "data_digest": __get_data_digest(str_logistics_interface),
        "partner_code": product['customs_gate'],
        "from_code": "gcsp",
        "msg_type": "GLOBAL_CUSTOMS_DECLARE_NOTIFY",
        "msg_id": "1678781969244",
        "logistics_interface": str_logistics_interface
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    res = requests.post(
        url=url,
        headers=headers,
        data=payload,
        verify=False,
    )
    return {"data":res.text}
    
# endregion

# region [declare_manifest]
def declare_manifest(req):

    url = "https://clients-test.postnl.a02.cldsvc.net/v7/api/declare/item"

    cbcode = __random_CB()
    mawb = __random_mawb()

    parcelList = [{
        "gnum": 1,
        "wayBillNo": item,
        "bagId": __assistlabel_generate(),
        "copNo": cbcode,
    } for item in req['items']]
    
    print(parcelList)
    
    obj_content = {
        "guid": "eb3c71a8-43a4-4fd8-834f-df2046247fa5",
        "appType": "1",
        "appTime": "20221118000000+0800",
        "declareCountry": "CN",
        "clearanceMode": "CFS",
        "arrivePort": "LGG",
        "copNo": cbcode,
        "trafMode": "5",
        "trafName": "FLIHGT",
        "voyageNo": "FT12345",
        "masterWayBill": mawb,
        "grossWeight": "100.000",
        "netWeight": "100.000",
        "bigBagCount": f"{len(set([i['bagId'] for i in  parcelList]))}",
        "eta": "20221114000000+0800",
        "etd": "20221115000000+0800",
        "parcelCount": f"{len(parcelList)}",
        "portCode": "SZX",
        "feature": "",
        "parcelList": parcelList
    }

    print(obj_content)
    str_content = base64.b64encode(json.dumps(
        obj_content).encode(encoding='ascii')).decode("UTF-8")

    obj_logistics_interface = {
        "bizType": "CUSTOMS_MANIFEST_NOTIFY",
        "bizKey": cbcode,
        "formatType": "1",
        "content": str_content
    }

    str_logistics_interface = json.dumps(obj_logistics_interface)

    payload = {
        "data_digest": __get_data_digest(str_logistics_interface),
        "partner_code": "GATE_30503886",
        "from_code": "gccs-overseas",
        "msg_type": "GLOBAL_CUSTOMS_DECLARE_NOTIFY",
        "msg_id": cbcode,
        "logistics_interface": str_logistics_interface,
    }
    
    print(payload)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    res = requests.post(
        url=url,
        headers=headers,
        data=payload,
        verify=False,
    )
    return {"mawb": mawb,
            "data": res.text}
# endregion

# region [declare_item]
def declare_item(req):
    products = {
        'IMG': {
            'source_code': 'DISTRIBUTOR_30874247',
            'mailBoxItem': None,
            'laneCode': "L_STANDARD_NLEU_DB_RM",
            'customs_gate': "GATE_30467721",
            'domestic': False,
            'prefix': 'CK'
        },
        'MGP': {
            'source_code': 'DISTRIBUTOR_30874547',
            'mailBoxItem': None,
            'laneCode': "L_STANDARD_NLEU_DB_NC",
            'customs_gate': "GATE_30503886",
            'domestic': False,
            'prefix': 'CH'
        }
    }
    
    product = products[req['product_code']]
    lpcode = __random_LP()
    cbcode = __random_CB()
    barcode = __barcode_generate(product['prefix'])
    
    data_logistics = __declare_item_logistics(product=product, barcode=barcode, lpcode=lpcode)
    data_customs = __declare_item_customs(req=req, product=product,
                           barcode=barcode, lpcode=lpcode, cbcode=cbcode)

    return{
        "barcode": barcode,
        "LPcode": lpcode,
        "CBcode": cbcode,
        "res_logistcs":data_logistics,
        "res_customs":data_customs
    }
# endregion


declare_manifest({"items":['CK001375438NL']})