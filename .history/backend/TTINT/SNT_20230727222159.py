import requests
import json

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


test_SNT = "2qQu3xg6e8w13J4uWyJDHp0TmRV2SPZnK7R3IAgfzb3RLIYt5qHjosDN9o6V2fkrBg77czDsTc8DgOHVC7swplLatjX2lLXWRPvCvRB5eDfOc2COUuO6uGgtSM5hzzZ6rUMV1Q19iYUu3PuIHq637gGn4GU0KJVGG99phX0aHcKwNKGQm47V0YNopmm8bWiwrsnFyKzZ3wwl1HiPJjc1xxJxGHyDTk4RlYVZCg0TnF6k4Yj8699D1qxJ8VeG45ImcwLvNeDJNaWuVRbPf8hrfSUkwII8E8ID8pbk5DF7ff5Z"


def barcode_generate(prefix):
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
            verify = False,
        )
    barcode = json.loads(res.text)[
        'data']['barcode_and_rfids'][0]['barcode']
    print(barcode)
    return barcode
