import json     #Module Json
import log      #Données Login
import time     #Module Time
import tweepy   #Module Twitter
import requests #Module requêtes
import datetime #Module Time II

from rich import print



url = ("https://data.opendatasoft.com/api/records/1.0/search/?dataset=vigilance-meteorologique%40public&q=&rows=96&facet=couleur&facet=crue_valeur&facet=coul_vague&facet=risque_valeur")

############################################################### - LOGIN TWEET - ####################################################################

auth = tweepy.OAuthHandler(log.consumer_key, log.consumer_secret)
auth.set_access_token(log.access_token, log.access_token_secret)
api = tweepy.API(auth)

####################################################################################################################################################

while True:
    print('[bold bright_blue]'+str(datetime.date.today())+' Alert Starting [/bold bright_blue]')

    hst = open('hst.json')
    data = json.load(hst)
    hst.close()


    response = requests.get(url).json()
    for i in range (len(response['records'])):
        if (data[str(response['records'][i]['fields']['dep'])]['color'] != response['records'][i]['fields']['couleur']) or data[str(response['records'][i]['fields']['dep'])]['date'] != response['records'][i]['fields']['dateinsert']:  
            if response['records'][i]['fields']['couleur'] != 'Vert':
                if data[str(response['records'][i]['fields']['dep'])]['reasons'] != response['records'][i]['fields']['risque_valeur0'] :
                    if response['records'][i]['fields']['couleur'] == 'Jaune':  
                        message = "🟡 #Vigilance Jaune en cours 🟡\n"
                        print('[bold bright_yellow]'+str(datetime.date.today())+' Alerte Jaune - '+response['records'][i]['fields']['nom_dept']+'[/bold bright_yellow]')
                        data[str(response['records'][i]['fields']['dep'])]['color'] = "Jaune"
                    elif response['records'][i]['fields']['couleur'] == 'Orange':
                        message = "🟠 #Vigilance Orange en cours 🟠\n"
                        print('[bold bright_orange]'+str(datetime.date.today())+' Alerte Orange - '+response['records'][i]['fields']['nom_dept']+'[/bold bright_orange]')
                        data[str(response['records'][i]['fields']['dep'])]['color'] = "Orange"
                    else :
                        message = "🔴 #Vigilance Rouge en cours 🔴\n"
                        print('[bold bright_red]'+str(datetime.date.today())+' Alerte Rouge - '+response['records'][i]['fields']['nom_dept']+'[/bold bright_red]')
                        data[str(response['records'][i]['fields']['dep'])]['color'] = "Rouge"
                    data[str(response['records'][i]['fields']['dep'])]['reasons'] = response['records'][i]['fields']['risque_valeur0']
                    message += 'Département : '+response['records'][i]['fields']['nom_dept']+'('+response['records'][i]['fields']['dep']+")\n"
                    message += 'Motif.s : '+response['records'][i]['fields']['risque_valeur0']+'\n'
                    message += 'Emise le '+response['records'][i]['fields']['dateinsert'][8:10]+'/'+response['records'][i]['fields']['dateinsert'][5:7]+'/'+response['records'][i]['fields']['dateinsert'][0:4]+' à '+response['records'][i]['fields']['dateinsert'][11:16]+'\n'
                    message += "Valable jusqu'au "+response['records'][i]['fields']['dateprevue'][8:10]+'/'+response['records'][i]['fields']['dateprevue'][5:7]+'/'+response['records'][i]['fields']['dateprevue'][0:4]+' à '+response['records'][i]['fields']['dateprevue'][11:16]+'\n'

            else :
                message = "🟢 Fin de #vigilance 🟢\n"
                print('[bold bright_green]'+str(datetime.date.today())+' Alerte Verte - '+response['records'][i]['fields']['nom_dept']+'[/bold bright_green]')
                data[str(response['records'][i]['fields']['dep'])]['color'] = "Vert"
                message +='Département : '+response['records'][i]['fields']['nom_dept']+'('+response['records'][i]['fields']['dep']+")\n"
                message +='Emise le '+response['records'][i]['fields']['dateinsert'][8:10]+'/'+response['records'][i]['fields']['dateinsert'][5:7]+'/'+response['records'][i]['fields']['dateinsert'][0:4]+' à '+response['records'][i]['fields']['dateinsert'][11:16]+'\n'
            
            api.update_status(message)
            time.sleep(900)
        data[str(response['records'][i]['fields']['dep'])]['date'] = response['records'][i]['fields']['dateinsert']
    
    hst = open("hst.json", "r+")
    json.dump(data, hst, indent = 6)
    hst.close()

    time.sleep(1800)
        #print('Vigilance '+response['records'][i]['fields']['couleur']+' pour '+response['records'][i]['fields']['risque_valeur0']+' DEPT : '+response['records'][i]['fields']['nom_dept']+'('+response['records'][i]['fields']['dep']+") Valable jusqu'au "+response['records'][i]['fields']['dateprevue'][8:10]+'/'+response['records'][i]['fields']['dateprevue'][5:7]+'/'+response['records'][i]['fields']['dateprevue'][0:4]+' à '+response['records'][i]['fields']['dateprevue'][11:16])
