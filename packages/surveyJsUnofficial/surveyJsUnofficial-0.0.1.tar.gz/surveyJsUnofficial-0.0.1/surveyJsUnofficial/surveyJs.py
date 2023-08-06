import requests
import json
class surveyJs:
    def __init__(self, accessKey):
        self.accessKey = accessKey
    
    def changeAccessKey(self, oldKey, newKey):
        if self.accessKey== oldKey:
            self.accessKey == newKey
            print('Access Key Changed to {}'.format(self.accessKey))
        else:
            return ('Please verify the older key sent!!')
        
    def setResultSummaryState(self):
        data = requests.get(f'https://api.surveyjs.io/private/Surveys/setResultSummaryState?accessKey={self.accessKey}')
        data = json.loads(data.content)
        return data
    
    def getResultSummaryState(self, id):
        data = requests.get(f'https://api.surveyjs.io/private/Surveys/getResultSummaryState/{id}?accessKey={self.accessKey}')
        data = json.loads(data.content)
        return data
    
    def getSurveyResults(self, id, start_date= None, end_date= None):
        data = requests.get(f' https://api.surveyjs.io/private/Surveys/getSurveyResults/{id}?accessKey={self.accessKey}&from={start_date}&till={end_date}')
        data = json.loads(data.content)
        return data
    
    def getSurveyPublicResults(self, id, start_date= None, end_date= None):
        data = requests.get(f'https://api.surveyjs.io/private/Surveys/getSurveyPublicResults/{id}?from={start_date}&till={end_date}')
        data = json.loads(data.content)
        return data
    
    def getSurveyInfo(self, id, ownerId= None):
        data = requests.get(f'https://api.surveyjs.io/private/Surveys/getSurveyInfo?accessKey={self.accessKey}&surveyId={id}&ownerId={ownerId}')
        data = json.loads(data.content)
        return data
    
    def getActive(self, ownerId= None):
        data = requests.get(f'https://api.surveyjs.io/private/Surveys/getActive?accessKey={self.accessKey}&ownerId={ownerId}')
        data = json.loads(data.content)
        return data
    
    def createSurvey(self, name, ownerId= None):
        data = requests.get(f'https://api.surveyjs.io/private/Surveys/create?accessKey={self.accessKey}&name={name}&ownerId={ownerId}')
        data = json.loads(data.content)
        return data
    
    def deleteSurvey(self,id):
        data = requests.get(f'https://api.surveyjs.io/private/Surveys/delete/{id}?accessKey={self.accessKey}')
        data = json.loads(data.content)
        return data
    
    def changeJson(self):
        data = requests.get(f'https://api.surveyjs.io/private/Surveys/changeJson?accessKey={self.accessKey}')
        data = json.loads(data.content)
        return data