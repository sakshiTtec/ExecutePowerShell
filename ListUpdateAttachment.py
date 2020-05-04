# -*- coding: utf-8 -*-
"""
Created on Fri May  1 13:20:30 2020

@author: 7504560
"""


#Sharepoint Add List Item Example
import requests
url = "https://ttecnp.sharepoint.com/_vti_bin/Lists.asmx"
def updateList(cookie,oracle_id):
    list_item=oracle_id
    payload = '''<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\"><soap:Body><UpdateListItems xmlns=\"http://schemas.microsoft.com/sharepoint/soap/\"><listName>ASD_Master_List_System_Assessment</listName><updates><Batch OnError='Continue'><Method ID=\"1\" Cmd=\"New\"><Field Name=\"Title\">'''+list_item+'''</Field></Method></Batch></updates></UpdateListItems></soap:Body></soap:Envelope>'''
    headers = {
      'SOAPAction': 'http://schemas.microsoft.com/sharepoint/soap/UpdateListItems',
      'Cookie': cookie,
      'Content-Type': 'text/xml; charset=utf-8'
    }
    try:
        response = requests.request("POST", url, headers=headers, data = payload)
        
        if '<ErrorCode>0x00000000</ErrorCode>' in str(response.text.encode('utf8')):
            res= str(response.text.encode('utf8'))
            if ('ows_ID=') in res:
                res=(res.split('ows_ID=')[1].split('ows_ContentType'))[0].replace('"','').replace(' ','')
            return res
    except Exception as e:
        # print(e)
        return "error"
    

def sendAttachment(ows_id,attachment,cookie):
    # print(attachment)
    attachment=attachment.replace("b'","").replace("'","")
    payload = '<?xml version=\"1.0\" encoding=\"utf-8\"?><soap:Envelope xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\"><soap:Body><AddAttachment xmlns=\"http://schemas.microsoft.com/sharepoint/soap/\"><listName>ASD_Master_List_System_Assessment</listName><listItemID>'+ows_id+'</listItemID><fileName>SystemAssessment.txt</fileName><attachment>'+attachment+'</attachment></AddAttachment></soap:Body></soap:Envelope>'
    headers = {
      'SOAPAction': 'http://schemas.microsoft.com/sharepoint/soap/AddAttachment',
      'Cookie': cookie,
      'Content-Type': 'text/xml; charset=utf-8'
    }
    try:
        response = requests.request("POST", url, headers=headers, data = payload)
        # print(response.text.encode('utf8'))
    except Exception as e:
        # print(e)
        return "error"
                                                  