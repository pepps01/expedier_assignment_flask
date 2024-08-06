import time
import requests
import hmac
import hashlib
import logging
import json
from dotenv import load_dotenv
import os

class Sumsub():
    load_dotenv() 
    SUMSUB_TEST_BASE_URL="https://api.sumsub.com/"
    SUMSUB_SECRET_KEY =os.getenv("SUMSUB_SECRET_KEY")
    SUMSUB_APP_TOKEN =os.getenv("SUMSUB_APP_TOKEN")
    REQUEST_TIMEOUT= os.getenv("REQUEST_TIMEOUT")
    
    def __init__(self) -> None:
        pass

    def create_applicant(external_user_id, level_name):
        body = {'externalUserId': external_user_id}
        params = {'levelName': level_name}
        headers = {
            'Content-Type': 'application/json',
            'Content-Encoding': 'utf-8'
        }

        
        resp = Sumsub.sign_request(
            requests.Request('POST', Sumsub.SUMSUB_TEST_BASE_URL + '/resources/applicants?levelName=' + level_name,
                            params=params,
                            data=json.dumps(body),
                            headers=headers))
        s = requests.Session()
        response = s.send(resp, timeout=6000)
        applicant_id = (response.json()['id'])
        return applicant_id


    def get_applicant_status(applicant_id):
        url = Sumsub.SUMSUB_TEST_BASE_URL + '/resources/applicants/' + applicant_id + '/requiredIdDocsStatus'
        resp = Sumsub.sign_request(requests.Request('GET', url))
        s = requests.Session()
        response = s.send(resp, timeout=Sumsub.REQUEST_TIMEOUT)
        return response

    def add_document(applicant_id):
        with open('img.jpg', 'wb') as handle:
            response = requests.get('https://fv2-1.failiem.lv/thumb_show.php?i=gdmn9sqy&view', stream=True,
                                    timeout=Sumsub.REQUEST_TIMEOUT)
            if not response.ok:
                logging.error(response)

            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
        payload = {"metadata": '{"idDocType":"PASSPORT", "country":"USA"}'}
        resp = Sumsub.SUMSUB_TEST_BASE_URL.sign_request(
            requests.Request('POST', Sumsub.SUMSUB_TEST_BASE_URL + '/resources/applicants/' + applicant_id + '/info/idDoc',
                            data=payload,
                            files=[('content', open('img.jpg', 'rb'))]
                            ))
        sw = requests.Session()
        response = sw.send(resp, timeout=Sumsub.REQUEST_TIMEOUT)
        return response

    @staticmethod
    def sign_request(request: requests.Request) -> requests.PreparedRequest:
        prepared_request = request.prepare()
        now = int(time.time())
        method = request.method.upper()
        path_url = prepared_request.path_url  # includes encoded query params
        
        body = b'' if prepared_request.body is None else prepared_request.body
        if type(body) == str:
            body = body.encode('utf-8')
        data_to_sign = str(now).encode('utf-8') + method.encode('utf-8') + path_url.encode('utf-8') + body
        # hmac needs bytes
        signature = hmac.new(
            Sumsub.SUMSUB_SECRET_KEY.encode('utf-8'),
            data_to_sign,
            digestmod=hashlib.sha256
        )
        prepared_request.headers['X-App-Token'] = Sumsub.SUMSUB_APP_TOKEN
        prepared_request.headers['X-App-Access-Ts'] = str(now)
        prepared_request.headers['X-App-Access-Sig'] = signature.hexdigest()
        return prepared_request

    @staticmethod
    def get_access_token(external_user_id, level_name):
        # https://developers.sumsub.com/api-reference/#access-tokens-for-sdks
        params = {'userId': external_user_id, 'ttlInSecs': '600', 'levelName': level_name}
        headers = {'Content-Type': 'application/json',
                'Content-Encoding': 'utf-8'
                }
        resp = Sumsub.sign_request(requests.Request('POST', Sumsub.SUMSUB_TEST_BASE_URL + '/resources/accessTokens',
                                            params=params,
                                            headers=headers))
        s = requests.Session()
        response = s.send(resp, timeout=Sumsub.REQUEST_TIMEOUT)
        token = (response.json()['token'])

        return token