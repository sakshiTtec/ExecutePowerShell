# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 23:02:35 2020

@author: 7504560
"""


#these are powershellc commands but could be tweaked in python
#guid = [guid]::NewGuid()
#[createdutc] = [datetime]::UtcNow.ToString("o", [System.Globalization.CultureInfo]::InvariantCulture)
#[expiresutc] = [datetime]::UtcNow.AddMinutes(10).ToString("o", [System.Globalization.CultureInfo]::InvariantCulture)
#[username] -- mark.rubio@ttecnp.com
#[password] -- password

#GetCertificateAndSignaturefromTTFS
import requests
import uuid
import datetime
import configuration
import re

def cert():
    createdutc=datetime.datetime.now(datetime.timezone.utc).isoformat()
    createdutc=createdutc[:-7]+'0Z'
    now = datetime.datetime.now(datetime.timezone.utc)
    expiresutc = (now + datetime.timedelta(minutes = 10)).isoformat()
    expiresutc=expiresutc[:-7]+'0Z'
    guid=str(uuid.uuid4())
    username = configuration.config['sp_user']
    password = configuration.config['sp_password']
    
    url = "https://ttfs.ttecnp.com/adfs/services/trust/2005/usernamemixed"
    
    payload = '<?xml version=\"1.0\" encoding=\"UTF-8\"?><s:Envelope xmlns:s=\"http://www.w3.org/2003/05/soap-envelope\" xmlns:wsse=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd\" xmlns:saml=\"urn:oasis:names:tc:SAML:1.0:assertion\" xmlns:wsp=\"http://schemas.xmlsoap.org/ws/2004/09/policy\" xmlns:wsu=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd\" xmlns:wsa=\"http://www.w3.org/2005/08/addressing\" xmlns:wssc=\"http://schemas.xmlsoap.org/ws/2005/02/sc\" xmlns:wst=\"http://schemas.xmlsoap.org/ws/2005/02/trust\"><s:Header><wsa:Action s:mustUnderstand=\"1\">http://schemas.xmlsoap.org/ws/2005/02/trust/RST/Issue</wsa:Action><wsa:To s:mustUnderstand=\"1\">https://ttfs.ttecnp.com/adfs/services/trust/2005/usernamemixed</wsa:To><wsa:MessageID>'+guid+'</wsa:MessageID><ps:AuthInfo xmlns:ps=\"http://schemas.microsoft.com/Passport/SoapServices/PPCRL\" Id=\"PPAuthInfo\"><ps:HostingApp>Managed IDCRL</ps:HostingApp><ps:BinaryVersion>6</ps:BinaryVersion><ps:UIVersion>1</ps:UIVersion><ps:Cookies></ps:Cookies><ps:RequestParams>AQAAAAIAAABsYwQAAAAxMDMz</ps:RequestParams></ps:AuthInfo><wsse:Security><wsse:UsernameToken wsu:Id=\"user\"><wsse:Username>'+username+'</wsse:Username><wsse:Password>'+password+'</wsse:Password></wsse:UsernameToken><wsu:Timestamp Id=\"Timestamp\"><wsu:Created>'+createdutc+'</wsu:Created><wsu:Expires>'+expiresutc+'</wsu:Expires></wsu:Timestamp></wsse:Security></s:Header><s:Body><wst:RequestSecurityToken Id=\"RST0\"><wst:RequestType>http://schemas.xmlsoap.org/ws/2005/02/trust/Issue</wst:RequestType><wsp:AppliesTo><wsa:EndpointReference><wsa:Address>urn:federation:MicrosoftOnline</wsa:Address></wsa:EndpointReference></wsp:AppliesTo><wst:KeyType>http://schemas.xmlsoap.org/ws/2005/05/identity/NoProofKey</wst:KeyType></wst:RequestSecurityToken></s:Body></s:Envelope>'
    headers = {
      'Content-Type': 'application/soap+xml; charset=utf-8'
    }
    try:
        response = requests.request("POST", url, headers=headers, data = payload)
        # print("***************************")
        res=str(response.text.encode('utf8'))
        result = re.search('<saml:Assertion(.*)</saml:Assertion>', res)
        result= "<saml:Assertion "+ (result.group(1)) +"</saml:Assertion>"
        # print(result)
        return result
    except Exception as e:
        # print(e)
        return "error"
    