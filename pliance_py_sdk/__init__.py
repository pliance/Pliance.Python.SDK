import requests
import jwt
import datetime

class ClientFactory:
    def __init__(self, secret, issuer, url, cert=None):
        self.secret = secret
        self.issuer = issuer
        self.url = url
        self.cert = cert

    def create(self, givenName, subject):
        return PlianceClient(self, givenName, subject)

    def executePost(self, endpoint, data, givenName, subject):
        token = self.__getJwt(givenName, subject)
        headers={'Authorization': 'Bearer ' + token, 'User-Agent': 'Pliance.Py.SDK:VERSION'}
        response = requests.post(f'{self.url}{endpoint}', headers=headers, verify=True, cert=self.cert, json=data)

        if response.status_code / 100 != 2:
            raise ApiException(response.status_code)

        return response.json()

    def executePut(self, endpoint, data, givenName, subject):
        token = self.__getJwt(givenName, subject)
        headers={'Authorization': 'Bearer ' + token, 'User-Agent': 'Pliance.Py.SDK:VERSION'}
        response = requests.put(f'{self.url}{endpoint}', headers=headers, verify=True, cert=self.cert, json=data)

        if response.status_code / 100 != 2:
            raise ApiException(response.status_code)

        return response.json()

    def executeGet(self, endpoint, givenName, subject, payload=None):
        token = self.__getJwt(givenName, subject)
        headers={'Authorization': 'Bearer ' + token, 'User-Agent': 'Pliance.Py.SDK:VERSION'}
        response = requests.get(f'{self.url}{endpoint}', headers=headers, verify=True, cert=self.cert, params=payload)

        if response.status_code / 100 != 2:
            raise ApiException(response.status_code)

        return response.json()


    def executeDelete(self, endpoint, payload, givenName, subject):
        token = self.__getJwt(givenName, subject)
        headers={'Authorization': 'Bearer ' + token, 'User-Agent': 'Pliance.Py.SDK:VERSION'}
        response = requests.delete(f'{self.url}{endpoint}', headers=headers, verify=True, cert=self.cert, params=payload)

        if response.status_code / 100 != 2:
            raise ApiException(response.status_code)
                
        return response.json()

    def __getJwt(self, givenName, subject):
        token = jwt.encode(
            {
                'iat': datetime.datetime.utcnow(),
                'nbf': datetime.datetime.utcnow(),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300),
                'aud': 'pliance.io',
                'iss': self.issuer,
                'given_name': givenName,
                'sub': subject
            }, self.secret, algorithm='HS256')
        return token

class PlianceClient:
    def __init__(self, factory, givenName, subject):
        self.factory = factory
        self.givenName = givenName
        self.subject = subject

    # @inject: methods
    def archive_company(self, command):
    	return self.__executePost('api/CompanyCommand/Archive', command)

    def archive_company_v2(self, command):
    	return self.__executePost('api/CompanyV2Command/Archive', command)

    def archive_person(self, command):
    	return self.__executePost('api/PersonCommand/Archive', command)

    def batch_register_person(self, command):
    	return self.__executePut('api/PersonCommand/Batch', command)

    def classify_company_hit(self, command):
    	return self.__executePost('api/CompanyCommand/Classify', command)

    def classify_company_v2_link(self, command):
    	return self.__executePost('api/CompanyV2Command/ClassifyLink', command)

    def classify_company_v2_match(self, command):
    	return self.__executePost('api/CompanyV2Command/Classify', command)

    def classify_person_hit(self, command):
    	return self.__executePost('api/PersonCommand/Classify', command)

    def company_data(self, request):
    	return self.__executeGet('api/CompanyQuery/CompanyData', request)

    def delete_company(self, command):
    	return self.__executeDelete('api/CompanyCommand', command)

    def delete_company_v2(self, command):
    	return self.__executeDelete('api/CompanyV2Command', command)

    def delete_person(self, command):
    	return self.__executeDelete('api/PersonCommand', command)

    def delete_webhook_delivery_failure(self, command):
    	return self.__executeDelete('api/WebhookCommand', command)

    def get_company_report(self, request):
    	return self.__executeGet('api/ReportQuery/CompanyReport', request)

    def get_general_report(self, request):
    	return self.__executeGet('api/ReportQuery/GeneralReport', request)

    def get_person_report(self, request):
    	return self.__executeGet('api/ReportQuery/PersonReport', request)

    def get_webhook(self, request):
    	return self.__executeGet('api/WebhookQuery', request)

    def list_companies(self, request):
    	return self.__executeGet('api/CompanyQuery/List', request)

    def list_companies_v2(self, query):
    	return self.__executeGet('api/CompanyV2Query/List', query)

    def list_persons(self, request):
    	return self.__executeGet('api/PersonQuery/List', request)

    def list_webhook_delivery_failures(self, query):
    	return self.__executeGet('api/WebhookQuery/DeliveryFailures', query)

    def ping(self, request):
    	return self.__executeGet('api/Ping', request)

    def poke(self, query):
    	return self.__executePost('api/WebhookQuery/Poke', query)

    def register_company(self, command):
    	return self.__executePut('api/CompanyCommand', command)

    def register_company_v2(self, command):
    	return self.__executePut('api/CompanyV2Command', command)

    def register_person(self, command):
    	return self.__executePut('api/PersonCommand', command)

    def save_webhook(self, command):
    	return self.__executePut('api/WebhookCommand', command)

    def search_company(self, request):
    	return self.__executeGet('api/CompanyQuery/Search', request)

    def search_person(self, request):
    	return self.__executeGet('api/PersonQuery/Search', request)

    def unarchive_company(self, command):
    	return self.__executePost('api/CompanyCommand/Unarchive', command)

    def unarchive_company_v2(self, command):
    	return self.__executePost('api/CompanyV2Command/Unarchive', command)

    def unarchive_person(self, command):
    	return self.__executePost('api/PersonCommand/Unarchive', command)

    def view_company(self, request):
    	return self.__executeGet('api/CompanyQuery', request)

    def view_company_v2(self, query):
    	return self.__executeGet('api/CompanyV2Query', query)

    def view_person(self, request):
    	return self.__executeGet('api/PersonQuery', request)

    def watchlist_company(self, request):
    	return self.__executeGet('api/WatchlistQuery/Company', request)

    def watchlist_company_v2(self, request):
    	return self.__executeGet('api/WatchlistQuery/CompanyV2', request)

    def watchlist_company_v2_link(self, request):
    	return self.__executeGet('api/WatchlistQuery/CompanyV2Link', request)

    def watchlist_person(self, request):
    	return self.__executeGet('api/WatchlistQuery', request)

    def watchlist_person_v2(self, request):
    	return self.__executeGet('api/WatchlistQuery/v2', request)

    # @inject: !methods

    ## Internal
    def __executeGet(self, endpoint, payload=None):
        result = self.factory.executeGet(endpoint, self.givenName, self.subject, payload=payload)
        
        return self.__throw_on_error(result)

    def __executePut(self, endpoint, data):
        result = self.factory.executePut(endpoint, data, self.givenName, self.subject)
        
        return self.__throw_on_error(result)

    def __executePost(self, endpoint, data):
        result = self.factory.executePost(endpoint, data, self.givenName, self.subject)
        
        return self.__throw_on_error(result)

    def __executeDelete(self, endpoint, data):
        result = self.factory.executeDelete(endpoint, data, self.givenName, self.subject)
        
        return self.__throw_on_error(result)

    def __throw_on_error(self, payload):
        if not payload['success']:
            raise ApiException(payload['message'])

        return payload

class ApiException(Exception):
    pass