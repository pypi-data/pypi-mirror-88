import json
import uuid
import base64
import requests
import webbrowser
from requests.auth import HTTPDigestAuth

class payUnit:
    """
    Initiates and processes payments
    """
    def __init__(self,data):      
        self.config_data = data
        if data.keys().count('api_key') == 0:
            raise Exception('api_key not present')
        if data.keys().count('user_api') == 0:
            raise Exception('user_api not present')
        if data.keys().count('return_url') == 0:
            raise Exception('return_url not present')
        if data.keys().count('password_api') == 0:
            raise Exception('password_api not present')
        if data.keys().count('mode') == 0:
            raise Exception('sdk mode not present')
        if(data['mode'].lower() != "test" and data['mode'].lower() != "live"):
            raise Exception('Invalid sdk mode')
                 

    def makePayment(self,amount): 
        if(int(amount) <= 0):
            return {"message":"Invalid transaction amount","status":False}
            
        user_api = self.config_data["user_api"]
        password_api = str(self.config_data["password_api"])
        api_key = str(self.config_data["api_key"])  
        auth = user_api+":"+password_api
        environment = str(self.config_data['mode'])
        base64AuthData = base64.b64encode((auth).encode()).decode()
        return_url = str(self.config_data["return_url"])

        test_url = ''
        if(environment.lower() == 'test'):
            test_url = "http://192.168.100.70:5000/api/gateway/initialize"
        elif(environment.lower() == 'live'):
            test_url = "http://192.168.100.70:5000/api/gateway/initialize"
        else:
            return {"message":" Invalid environment mode ","status": False}

        headers = {
            "x-api-key": str(api_key),
            "content-type": "application/json",
            "Authorization": "Basic "+ str(base64AuthData)
        }

        test_body = {
            "description":"A sample description for a reason for a transaction",
            "transaction_id":  str(uuid.uuid1()),
            "total_amount": str(amount),
            "return_url": str(self.config_data['return_url'])
        }
        # response = requests.post(test_url,auth = HTTPDigestAuth(user_api,password_api),data = json.dumps(test_body),headers = headers)
        try:   
            response = requests.post(test_url,data = json.dumps(test_body),headers = headers)
            response = response.json()
            if(response['body']['status'] == 200):
                webbrowser.open(response['body']['transaction_url'])
                return {"message":"Successfylly initated Transaction","status":True}
        except:
            
            return {"message":"Oops, an error occured, Payment gateway could not be found","status":False}
 