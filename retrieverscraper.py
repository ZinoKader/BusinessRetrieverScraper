#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import requests
import time
import getpass

username = None
password = None
loginurl = "https://login.e.bibl.liu.se/login?url=http://web.retriever-info.com/services/businessinfo.html"
htmlinfourl = "http://web.retriever-info.com.e.bibl.liu.se/services/businessinfo/displayBusinessInfo?orgnum="
xmlinfourl = "http://web.retriever-info.com.e.bibl.liu.se/services/businessinfo/overview?noQueryInterceptor=false&orgnum="


# SKRIV chcp 65001 i CMD först för att inte få encodingerror (endast Windows)
def getCompanyInfo(orgnum):
    global username
    global password
    global loginurl
    global htmlinfourl
    global xmlinfourl

    if not username:
        username = input("Ditt Liu-ID (ex danba631): ")
    if not password:
        password = getpass.getpass("Ditt LiU-lösenord (inga tecken visas när du skriver): ")
        print("Autentiserad! ---\n\n")

    requestsession = requests.session()
    login_data = { "user" : "zinka766", "pass" : password }
    requestsession.post(loginurl, data=login_data)

    orgnum = str(orgnum)
    htmlinfourl += orgnum
    xmlinfourl += orgnum

    htmlresponse = requestsession.get(htmlinfourl)
    xmlresponse = requestsession.get(xmlinfourl)

    #hämta generell info som företagsnamn osv...
    htmltext = htmlresponse.text.encode("UTF-8")
    soup = BeautifulSoup(htmltext, "html.parser")
    companyname = soup.find("h1", class_="heading company-name").getText()

    #hämta komplex info från XML som likviditet, anställda, etc...
    tree = ET.fromstring(xmlresponse.content)
    overviewtag = tree[0]
    employeetag = overviewtag[14] #element nummer 15 under översikt är anställda
    latestyearemployees = employeetag[0]
    lastyearemployees = employeetag[1]

    #presentera info
    print("Företag: " + companyname)
    print("2015 år anställda: " + latestyearemployees.text)
    print("2014 år anställda: " + lastyearemployees.text)


    """ hämta annan statistik som likviditet osv...
    for child in overviewtag:
        print(child.tag, child.attrib)
    """
