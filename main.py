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
print('[bold bright_pink]'+str(datetime.date.today())+' Alert API Starting [/bold bright_pink]')
while True:
    print('[bold bright_blue]'+str(datetime.date.today())+' Alert Analyse Starting [/bold bright_blue]')

    hst = open('hst.json')
    data = json.load(hst)
    hst.close()

    meteo_reasons = []
    meteo_colors = ["Rouge","Orange","Jaune","Vert"]
    meteo_emote = ["🔴","🟠","🟡","🟢"]
    dept_alerted = []
                
    response = requests.get(url).json()
    for dept in range (len(response['records'])):
        if (data[str(response['records'][dept] ['fields']['dep'])]['color'] != response['records'][dept] ['fields']['couleur']) or (data[str(response['records'][dept] ['fields']['dep'])]['date'] != response['records'][dept] ['fields']['dateinsert'] and response['records'][dept] ['fields']['couleur'] != 'Vert'):  
            if response['records'][dept] ['fields']['couleur'] != 'Vert':
                if data[str(response['records'][dept] ['fields']['dep'])]['reasons'] != response['records'][dept] ['fields']['risque_valeur0'] :
                    data[str(response['records'][dept] ['fields']['dep'])]['color'] = response['records'][dept] ['fields']['couleur']
                    if response['records'][dept] ['fields']['risque_valeur0'] not in meteo_reasons:
                        meteo_reasons.append(response['records'][dept] ['fields']['risque_valeur0'])
                    data[str(response['records'][dept] ['fields']['dep'])]['reasons'] = response['records'][dept] ['fields']['risque_valeur0']
            else :
                data[str(response['records'][dept] ['fields']['dep'])]['color'] = "Vert"
                data[str(response['records'][dept] ['fields']['dep'])]['end_alert'] = True

        data[str(response['records'][dept] ['fields']['dep'])]['date'] = response['records'][dept] ['fields']['dateinsert']
    
    
    for color_level in meteo_colors:
        if color_level == "Vert":
            message = meteo_emote[3]+" Fin de #Vigilance "+meteo_emote[3]
            for dept in data:
                if color_level == "Vert" and data[dept]['end_alert'] == True:
                    data[dept]['color']
                    dept_alerted.append(dept)
            message += '\nDépartment : '
            for dept_id in dept_alerted:
                message += dept_id
                if dept_alerted.index(dept_id) != len(dept_alerted) -1 :
                    message+=', '
            if len(dept_alerted) != 0 :
                    print (message)
                    #api.update_status(message)
                    time.sleep(900)
        else :   
            for reason in meteo_reasons:
                message = meteo_emote[meteo_colors.index(color_level)]+" Début de #Vigilance "+meteo_emote[meteo_colors.index(color_level)]
                dept_alerted = []
                for dept in data:    
                    if data[dept]['color'] == color_level:
                        if data[dept]['reasons'] == reason:
                            dept_alerted.append(dept)
                message += '\nDépartment : '
                for dept_id in dept_alerted:
                    message += dept_id
                    if dept_alerted.index(dept_id) != len(dept_alerted) -1 :
                        message+=', '
                message+='\nMotif.s : '+reason
                message += "\nValable jusqu'au "+data[dept]['date'][8:10]+'/'+data[dept]['date'][5:7]+'/'+data[dept]['date'][0:4]+' à '+data[dept]['date'][11:16]+'\n'

                if len(dept_alerted) != 0 :
                    print (message)
                    #api.update_status(message)
                    time.sleep(900)

    hst = open("hst.json", "r+")
    json.dump(data, hst, indent = 6)
    hst.close()
    print('[bold bright_blue]'+str(datetime.date.today())+' Alert Analyse end [/bold bright_blue]')
    time.sleep(1800)