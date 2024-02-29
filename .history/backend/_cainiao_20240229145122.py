import base64
import json
import hashlib
from backend._call import Call


class CAINIAO():
    # env_config = json.load(open(r'backend\SNT\environment.json'))
    # product_config = json.load(open(r'backend\SNT\product_code.json'))
    # tracking_mapping = json.load(open(r'backend\SNT\mapping_tracking.json'))
    # unsuccessful_delivery = json.load(open(r'backend\SNT\mapping_tracking_unsuccessful_delivery.json'))

    env_config = {
        "prod": {
            "domain": "https://clients.postnl.post/v7/api/",
            "callback": "https://de-link.cainiao.com/gateway/link.do",
            "api_key": "7XCcBhwSgbNDgsjPzgW0Md13eZ1wvXEmAAATU8fYpNwx2L5qEeTR4FH69BNIgjI3LtfsXBdBRtOZzvrpr9BURUYYbNV1m3pLRygdt5bat9WqPQMlwrqbepRiBYdjnVbXJyjIXUmaHja8OfTkw012W8f0SMSDYi3VmWjePlw1ufs4LPS9nDpE6jWNErW7wKCCwbi79gT8E6bDgCWXvowFvRPlnCc9zzNNfJgOnA2PkAUXeWETK658tM90rP2pxcAK1pTVRA7s4d2j2hCRhqpHPjmfIe52y5oiyzcMX9fablmj"
        },
        "test": {
            "domain": "https://clients-test.postnl.a02.cldsvc.net/v7/api/",
            "callback": "https://prelink.cainiao.com/gateway/link.do",
            "api_key": "2qQu3xg6e8w13J4uWyJDHp0TmRV2SPZnK7R3IAgfzb3RLIYt5qHjosDN9o6V2fkrBg77czDsTc8DgOHVC7swplLatjX2lLXWRPvCvRB5eDfOc2COUuO6uGgtSM5hzzZ6rUMV1Q19iYUu3PuIHq637gGn4GU0KJVGG99phX0aHcKwNKGQm47V0YNopmm8bWiwrsnFyKzZ3wwl1HiPJjc1xxJxGHyDTk4RlYVZCg0TnF6k4Yj8699D1qxJ8VeG45ImcwLvNeDJNaWuVRbPf8hrfSUkwII8E8ID8pbk5DF7ff5Z"
        }
    }
    product_config = {
        "IMG": {
            "productCode": "IMG",
            "resCode": "DISTRIBUTOR_30874247",
            "laneCode": "L_STANDARD_NLEU_DB_RM",
            "mailBoxItem": None,
            "customsGate": "GATE_30467721",
            "domestic": False,
            "barPrefix": "CK"
        },
        "MGP": {
            "productCode": "MGP",
            "resCode": "DISTRIBUTOR_30874547",
            "laneCode": "L_STANDARD_NLEU_DB_NC",
            "mailBoxItem": None,
            "customsGate": "GATE_30503886",
            "domestic": False,
            "barPrefix": "CH"
        },
        "GRX": {
            "productCode": "GRX",
            "resCode": "DISTRIBUTOR_30874813",
            "laneCode": "L_AE_STANDARD_NLGLOBAL_RM",
            "mailBoxItem": None,
            "customsGate": "GATE_30503886",
            "domestic": False,
            "barPrefix": "LS"
        },
        "PXP": {
            "productCode": "PXP",
            "resCode": "DISTRIBUTOR_30874413",
            "laneCode": "L_AE_STANDARD_NL_SG_NC",
            "mailBoxItem": None,
            "customsGate": "GATE_30503886",
            "domestic": True,
            "barPrefix": "LS"
        },
        "MRX": {
            "productCode": "MRX",
            "resCode": "DISTRIBUTOR_30874367",
            "laneCode": "L_AE_STANDARD_NLEU_NC",
            "mailBoxItem": None,
            "customsGate": "GATE_30503886",
            "domestic": False,
            "barPrefix": "LS"
        },
        "IRX": {
            "productCode": "IRX",
            "resCode": "DISTRIBUTOR_30874723",
            "laneCode": "L_AE_STANDARD_NLEU_BAT",
            "mailBoxItem": None,
            "customsGate": "GATE_30467721",
            "domestic": False,
            "barPrefix": "LS"
        },
        "IGT": {
            "productCode": "IGT",
            "resCode": "DISTRIBUTOR_30874723",
            "laneCode": "L_AE_STANDARD_NLEU_BAT",
            "mailBoxItem": None,
            "customsGate": "GATE_30467721",
            "domestic": False,
            "barPrefix": "LS"
        },
        "XBZ": {
            "productCode": "XBZ",
            "resCode": "DISTRIBUTOR_31037258",
            "laneCode": "L_AE_STANDARD_CC_NL_SG",
            "mailBoxItem": "Y",
            "customsGate": "GATE_30873172",
            "domestic": True,
            "barPrefix": "LS"
        },
        "XPZ": {
            "productCode": "XPZ",
            "resCode": "DISTRIBUTOR_31037258",
            "laneCode": "L_AE_STANDARD_CC_NL_SG",
            "mailBoxItem": "N",
            "customsGate": "GATE_30873172",
            "domestic": True,
            "barPrefix": "LS"
        },
        "UBZ": {
            "productCode": "XBZ",
            "resCode": "DISTRIBUTOR_30875031",
            "laneCode": "L_AE_ECONOMY_NLAIR_BAT",
            "mailBoxItem": "Y",
            "customsGate": "GATE_30467721",
            "domestic": True,
            "barPrefix": "UT"
        },
        "UPZ": {
            "productCode": "XBZ",
            "resCode": "DISTRIBUTOR_30875031",
            "laneCode": "L_AE_ECONOMY_NLAIR_BAT",
            "mailBoxItem": "N",
            "customsGate": "GATE_30467721",
            "domestic": True,
            "barPrefix": "UT"
        },
        "UNISZ": {
            "productCode": "UNISZ",
            "resCode": "DISTRIBUTOR_31166021",
            "laneCode": "L_AE_STANDARD_G3CAYVR",
            "mailBoxItem": "N",
            "customsGate": "GATE_30467721",
            "domestic": True,
            "barPrefix": "SPICA"
        }
    }

    tracking_mapping = {
        "30": "CAINIAO_GLOBAL_LASTMILE_GTMSACCEPT_CALLBACK",
        "32": "CAINIAO_GLOBAL_LASTMILE_GTMSDELIVERYOFFICEARRIVAL_CALLBACK",
        "33": "CAINIAO_GLOBAL_LASTMILE_GTMSDELIVERYOFFICEARRIVAL_CALLBACK",
        "36": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "37": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "71": "CAINIAO_GLOBAL_LASTMILE_GTMS_SC_ARRIVE_CALLBACK",
        "74": "CAINIAO_GLOBAL_LASTMILE_HOOUT_CALLBACK",
        "75": "CAINIAO_GLOBAL_LASTMILE_GTMSSTASIGN_CALLBACK",
        "134": "CAINIAO_GLOBAL_LASTMILE_GTMSACCEPT_CALLBACK",
        "135": "CAINIAO_GLOBAL_LASTMILE_GTMSACCEPT_CALLBACK",
        "173": "CAINIAO_GLOBAL_TRANSIT_ARRIVAL_CALLBACK",
        "199": "CAINIAO_GLOBAL_TRANSIT_ARRIVAL_CALLBACK",
        "301": "CAINIAO_GLOBAL_TRANSIT_DEPARTURE_CALLBACK",
        "1211": "CAINIAO_GLOBAL_LASTMILE_GTMS_SC_ARRIVE_CALLBACK",
        "1259": "CAINIAO_GLOBAL_LASTMILE_GTMSSTASIGN_CALLBACK",
        "1301": "CAINIAO_GLOBAL_TRANSIT_ARRIVAL_CALLBACK",
        "3011": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3025": "CAINIAO_GLOBAL_LASTMILE_GTMSACCEPT_CALLBACK",
        "3032": "CAINIAO_GLOBAL_LASTMILE_GTMSACCEPT_CALLBACK",
        "3034": "CAINIAO_GLOBAL_TRANSIT_ARRIVAL_CALLBACK",
        "3040": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3041": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3042": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3043": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3044": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3045": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3050": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3051": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3053": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3054": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3056": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3057": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3058": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3061": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3062": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3063": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "3116": "CAINIAO_GLOBAL_TRANSIT_ARRIVAL_CALLBACK",
        "5050": "CAINIAO_GLOBAL_LASTMILE_GTMSSTASIGN_CALLBACK",
        "8006": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "8007": "CAINIAO_GLOBAL_LASTMILE_GTMSSIGN_CALLBACK",
        "9010": "CAINIAO_GLOBAL_LASTMILE_UNREACHABLERETURN_CALLBACK",
        "9014": "CAINIAO_GLOBAL_LINEHAUL_UNREACHABLERETURN_ARRIVAL_CALLBACK",
        "9020": "CAINIAO_GLOBAL_LASTMILE_UNREACHABLERETURN_DISCARD_CALLBACK"
    }

    unsuccessful_delivery = {
        "36": "1",
        "1247": "1",
        "3055": "1",
        "9005": "1",
        "9006": "1",
        "8006": "5504",
        "8007": "5504",
        "3058": "5524",
        "3050": "5525",
        "3062": "5525",
        "3054": "5506",
        "3057": "5506",
        "3061": "5506",
        "3063": "5573",
        "3065": "5523",
        "3066": "5548",
        "3053": "5530",
        "3056": "5530",
        "3051": "5507"
    }

    def __init__(self, env, product_code=None):
        self.env = self.env_config[env]
        if product_code:
            self.set_product(product_code)

    def __get_msgType_logisticProvider_id(self, event):
        if event in self.tracking_mapping:
            msg_type = self.tracking_mapping[event]
            if "TRANSIT_ARRIVAL" in msg_type and self.product['domestic']:
                msg_type = "CAINIAO_GLOBAL_LASTMILE_GTMSACCEPT_CALLBACK"
            logistic_provider_id = 'TRAN_STORE_30874862' if 'TRANSIT' in msg_type else self.product[
                'resCode']
            return msg_type, logistic_provider_id
        return None, None

    def __get_data_digest(self, app_json, secretKey="postnl13798642"):
        app_bytes = (app_json + secretKey).encode(encoding='UTF-8')
        md5 = hashlib.md5(app_bytes)
        return base64.b64encode(md5.digest()).decode("UTF-8")

    def set_product(self, product_code):
        product_code = product_code.upper()
        self.product = self.product_config[product_code]
        return

    def tracking_event_callback(self,
                                barcode, lpcode, event, opTime,
                                ):

        event = str(event)
        opCode = self.unsuccessful_delivery[event] if event in self.unsuccessful_delivery else '0'

        obj_logistics_interface = {
            "logisticsOrderCode": lpcode,
            "trackingNumber": barcode,
            "waybillNumber": barcode,
            "opTime": opTime,
            "timeZone": "-8" self.product['res_code']=="DISTRIBUTOR_31166021" else "0",
            "transportType": "2" if event == "9014" else "4",
            "toPortCode": "HKG" if event == "9014" else None,
            "fromPortCode": "AMS" if event == "9014" else None,
            "operator": "postnl",
            "operatorContact": "info@postnl.nl",
            "opCode": opCode,
        }
        str_logistics_interface = json.dumps(obj_logistics_interface)

        msg_type, logistic_provider_id = self.__get_msgType_logisticProvider_id(
            event)

        if logistic_provider_id:
            payload = {
                "logistics_interface": str_logistics_interface,
                "logistic_provider_id": logistic_provider_id,
                "msg_type": msg_type,
                "data_digest": self.__get_data_digest(str_logistics_interface),
                "to_code": ""
            }

            call = Call(
                payload=payload,
                domain=self.env['callback'],
                app_json=False,
                key_str=barcode
            )

            res = call.res
            json_obj = json.loads(res.text)

            return msg_type, str(json_obj['success'] == 'true'), res.text
        return msg_type, 'non-mapped', None
