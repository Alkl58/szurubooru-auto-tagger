from requests.auth import HTTPBasicAuth
import lxml.html
import argparse
import requests
import urllib
import time
import json
import bs4
import re

#######################################################################################################################
#       Use Embedded Login / Adress:                                                                                  #
#                                                                                                                     #
embeddedauth = False #set this to "True" to skip command args                                                         #
#                                                                                                                     #
#                                                                                                                     #
booruadresse = "http://website:80/" #Insert here your Public Booru Adress - must be reachable from outside            #
booruloginname = "username" #Booru Username - must have high enough privileges                                        #
booruloinpassw = "password" # Booru User Password                                                                     #
#                                                                                                                     #
#######################################################################################################################

defaulttodanbooru = True #By default searches for the danbooru tags. Setting this to False will result in using the best match tags.

parser = argparse.ArgumentParser(description='Commandline usage of AutoTagger - You can skip username, password and adress, when you edited this Python script by setting "embeddedauth" to "True"')
if embeddedauth == False:
    parser.add_argument("--username", required=True, help="Username of the Account on the Booru")
    parser.add_argument("--password", required=True, help="Password of the Account on the Booru")
    parser.add_argument("--adress", required=True, help="The Adress of the Booru, must be reachable from outside of your network")
parser.add_argument("--mode", type=int, help="1 = Single Post, 2 = Range of Posts - Default: 1")
parser.add_argument("--poststart", required=True, help="Post (start) number - Must be lower than 'post-end' when 'mode = 2'")
parser.add_argument("--postend", help="Post number - Only for 'mode = 2'")
args = parser.parse_args()

if embeddedauth == False:
    booruloginname = args.username
    booruloinpassw = args.password
    booruadresse = args.adress
        
postnummerstart = str(args.poststart)
postnummerende = str(args.postend)
modus = args.mode

if(modus == None):
    modus = 1
        
postnummer = "68" #Automaticly set - don't touch
postversion = "0" #Automaticly set - don't touch



def RequestPostAdresse():
    #Diese Funktion fragt die URL des Bildes ab
    r2 = requests.get(booruadresse + "/api/post/" + postnummer, headers={'Accept':'application/json'}, auth=HTTPBasicAuth(booruloginname, booruloinpassw))
    r3 = r2.json()["contentUrl"]
    r4 = r2.json()["version"]
    addresseTemp = booruadresse + r3
    global postversion
    postversion = r4
    #print(postversion)
    #print(addresseTemp)
    IQDBAbfrage(addresseTemp)

def IQDBAbfrage(url):
    #Diese Funkion lädt das Bild auf IQDB hoch und zieht sich die Tags aus dem "Best-Match" Bild
    res = requests.get('https://iqdb.org/?url=' + url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    #Filter um "nur" <img...> zu filtern
    #
    #Sucht nach danbooru tags
    if(defaulttodanbooru == True):
        elems = soup.select("a[href*=danbooru] > img")
    elif(defaulttodanbooru == False):
        elems = soup.select('#pages > div:nth-child(2) > table:nth-child(1) > tr:nth-child(2) > td > a > img')
    #Entfernt die ersten fünf Elemente, da diese irrelevant sind
    #print(soup)
    #print(elems)
    tags = elems[0].get('title').split()[5:]
    #print(tags)
    UpdateTag(tags)

def UpdateTag(tagsinput):
    #Diese Funktion macht ein Put-Request, um die Tags auf dem Booru zu setzen
    #So muss Tagging aussehen: < 'big_breasts' "," 'sex' >
    taginput = {"version": postversion, "tags": tagsinput}
    tagtemp = json.dumps(taginput)
    r2 = requests.put(booruadresse + "/api/post/" + postnummer, headers={'Accept':'application/json', 'Content-Type': 'application/json'}, auth=HTTPBasicAuth(booruloginname, booruloinpassw), data=tagtemp)
    #print(r2.json())
    #print(taginput)

def PostLoop(start, ende):
    #Loop durch die Posts durch. Kann Problematisch sein, da manche Bilder einfach keine Tags zurückgeben und daher die Funktionen abschmieren
    nekomimis = 0
    catgirls = 1
    nekomimis = int(start)
    catgirls = int(ende)
    global postnummer
    while nekomimis <= catgirls:
        postnummer = str(nekomimis)
        try:
            RequestPostAdresse()
            print("Finished Tagging " + postnummer)
        except:
            global defaulttodanbooru
            defaulttodanbooru = False
            try:
                RequestPostAdresse()
                print("Error with Danbooru, used best match " + postnummer)
                defaulttodanbooru = True
            except:
                print("Error with Post " + postnummer)
            defaulttodanbooru = True
        nekomimis += 1
        time.sleep(10) #Waits 10s after each request, so IQDB won't block you
    print("Finished!")

if(modus == 1):
    postnummer = args.poststart
    RequestPostAdresse()
    print("Finished!")
elif(modus == 2):
    PostLoop(postnummerstart, postnummerende)
