# -*- coding: utf-8 -*-
"""
Created on Fri May  1 02:43:04 2020

@author: 7504560
"""

import requests
import re

url = "https://login.microsoftonline.com/rst2.srf"

def binaryToken(AssertionTag):
    payload = '<?xml version=\"1.0\" encoding=\"UTF-8\"?><S:Envelope xmlns:S=\"http://www.w3.org/2003/05/soap-envelope\" xmlns:wsse=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd\" xmlns:wsp=\"http://schemas.xmlsoap.org/ws/2004/09/policy\" xmlns:wsu=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd\" xmlns:wsa=\"http://www.w3.org/2005/08/addressing\" xmlns:wst=\"http://schemas.xmlsoap.org/ws/2005/02/trust\"><S:Header><wsa:Action S:mustUnderstand=\"1\">http://schemas.xmlsoap.org/ws/2005/02/trust/RST/Issue</wsa:Action><wsa:To S:mustUnderstand=\"1\">https://login.microsoftonline.com/rst2.srf</wsa:To><ps:AuthInfo xmlns:ps=\"http://schemas.microsoft.com/LiveID/SoapServices/v1\" Id=\"PPAuthInfo\"><ps:BinaryVersion>5</ps:BinaryVersion><ps:HostingApp>Managed IDCRL</ps:HostingApp></ps:AuthInfo><wsse:Security>'+AssertionTag+'</wsse:Security></S:Header><S:Body><wst:RequestSecurityToken xmlns:wst=\"http://schemas.xmlsoap.org/ws/2005/02/trust\" Id=\"RST0\"><wst:RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</wst:RequestType><wsp:AppliesTo><wsa:EndpointReference><wsa:Address>sharepoint.com</wsa:Address></wsa:EndpointReference></wsp:AppliesTo><wsp:PolicyReference URI=\"MBI\"></wsp:PolicyReference></wst:RequestSecurityToken></S:Body></S:Envelope>'
    headers = {
      'Content-Type': 'application/soap+xml; charset=utf-8'
    }
    try:
        response = requests.request("POST", url, headers=headers, data = payload)
        res=str(response.text.encode('utf8'))
        result = re.search('>t=(.*)</wsse:BinarySecurityToken>', res)
        result= 't='+(result.group(1))
        return result
    except Exception as e:
        # print(e)
        return "error"

def spoidcrl(token):
    url = "https://ttecnp.sharepoint.com/_vti_bin/idcrl.svc/"

    payload  = {}
    headers = {
      'Authorization': 'BPOSIDCRL '+token ,
      'Content-Type': 'application/soap+xml; charset=utf-8'
    }
    # print('BPOSIDCRL '+token)
    try:
        response = requests.request("GET", url, headers=headers, data = payload)
        res=str(response.cookies)
        result = re.search('Cookie (.*) for', res)
        result=(result.group(1))
        return result
    except Exception as e:
        # print(e)
        return "error"