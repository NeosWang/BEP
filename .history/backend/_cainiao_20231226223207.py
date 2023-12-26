import base64
import json
import hashlib
from backend._call import Call


class CAINIAO():
    env_config = json.load(open(r'backend\SNT\environment.json'))
    product_config = json.load(open(r'backend\SNT\product_code.json'))
    tracking_mapping = json.load(open(r'backend\SNT\mapping_tracking.json'))
    unsuccessful_delivery = json.load(open(r'backend\SNT\mapping_tracking_unsuccessful_delivery.json'))

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
        opCode = self.unsuccessful_delivery[event] if event in self.unsuccessful_delivery  else '0'

        obj_logistics_interface = {
            "logisticsOrderCode": lpcode,
            "trackingNumber": barcode,
            "waybillNumber": barcode,
            "opTime": opTime,
            "timeZone": "0",
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

            return msg_type , str(json_obj['success'] == 'true'), res.text
        return msg_type , 'non-mapped', None