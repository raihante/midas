# MIDAS BOT
# Author    : @fakinsit
# Date      : 09/09/24

import os
import time
import sys
import re
import json
import requests
from urllib.parse import unquote
from pyfiglet import Figlet
from colorama import Fore
from onlylog import Log


header = {
      "Accept-Language": "id,en-US;q=0.9,en;q=0.8",
      "Referer": "https://midas-tg-app.netlify.app/",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
    }
tix = 0

def banner():
    os.system("title MIDAS BOT" if os.name == "nt" else "clear")
    os.system("cls" if os.name == "nt" else "clear")
    custom_fig = Figlet(font='slant')
    print('')
    print(custom_fig.renderText(' MIDAS'));
    print(Fore.RED + '[#] [C] R E G E X    ' + Fore.GREEN + '[MIDAS BOT] $$ ' + Fore.RESET)
    print(Fore.GREEN +'[#] Welcome & Enjoy !', Fore.RESET)
    print(Fore.YELLOW +'[#] Having Troubles? PM Telegram [t.me/fakinsit] ', Fore.RESET)
    print('')

def runforeva(): 
    with open('quentod.txt', 'r') as file:
        queryh = file.read().splitlines()
    try:
            value = True
            while (value):
                for index, query_id in enumerate(queryh, start=1):
                    getname(query_id)
                    postrequest(gettoken(query_id))
    except:
        Log.error('[MAIN] error, restarting')
        runforeva()

def gettoken(querybro):
    try:
        url = "https://api-tg-app.midas.app/api/auth/register"
        s = requests.Session()
        redrop = {"initData":querybro}
        response = s.post(url, headers=header, json=redrop)
        if response.status_code != 201:
            Log.error('[gettoken] error, check your query_id / user_id maybe expired')
        elif response.status_code == 500:
            Log.error('[gettoken] error, close all Midas mini-app!')
            sleep(30)
        else:
            Log.success('login success')
            return response.text

    except:
        Log.error('[gettoken] error restarting, check your query_id / user_id maybe expired')

def getuser(querybro):
    global tix
    try:
        url = "https://api-tg-app.midas.app/api/user"
        urlvisit = "https://api-tg-app.midas.app/api/user/visited"
        s = requests.Session()
        s.headers.update({"Authorization": "Bearer "+querybro})
        response = s.get(url, headers=header)
        jData=response.json()
        jsonpoints =  jData['points']
        jsonsd =  jData['streakDaysCount']
        jsontix =  jData['tickets']
        Log.warn('GM points : '+ str(jsonpoints))
        Log.warn('check-in Day : '+ str(jsonsd))
        Log.warn('tickets : '+ str(jsontix))
        tix = jsontix

        s.patch(urlvisit, headers=header)
    except:
        print(e)
        Log.error('[getuser] error restarting, check your query_id / user_id maybe expired')

def getcheckin(querybro):
    url = "https://api-tg-app.midas.app/api/streak"
    urlvisit = "https://api-tg-app.midas.app/api/user/visited"
    
    try:

        s = requests.Session()
        s.headers.update({"Authorization": "Bearer "+querybro})
        s.patch(urlvisit, headers=header)
        response = s.get(url, headers=header)
        jData=response.json()
        jsonclaimable =  jData['claimable']
        if jsonclaimable == True:
            response = s.post(url, headers=header)
            if response.status_code == 201:
                Log.s('check-in success!')
        
    except:

        Log.error('[getcheckin] error, restarting')

def getname(querybro):
    try:
        found = re.search('user=([^&]*)', querybro).group(1)
        decodedUserPart = unquote(found)
        userObj = json.loads(decodedUserPart)
        Log.success('username : @' + userObj['username'])
    except:
        Log.error('[decodedUsername] error')


def playgame(tomket):
    n = tix

    for i in range(0, n):
        try:
            url = "https://api-tg-app.midas.app/api/game/play"
            s = requests.Session()
            s.headers.update({"Authorization": "Bearer "+tomket})
            response = s.post(url, headers=header)
            sleep(5)
            if response.status_code != 201:
                Log.error('[playgame] failed, restarting')

            elif response.status_code == 500:
                Log.error('[playgame] failed, close all Midas mini-app!')
                sleep(30)
            else:
                jData=response.json()
                jsonreward =  jData['points']
                Log.success('succes play game, reward : '+ str(jsonreward))
        except:
            Log.error('[playgame] failed, restarting')


def gettask(tomket):
    try:
        urltasks = "https://api-tg-app.midas.app/api/tasks/available"
        s = requests.Session()
        s.headers.update({"Authorization": "Bearer "+tomket})
        response = s.get(urltasks, headers=header)
        jData=response.json()

        for item in jData: 
            if item['state'] == 'WAITING':
                list_id = []
                list_name = []
                list_id.append(item['id'])
                list_name.append(item['name'])
                anjoy = list_id + list_name
                urlstart = 'https://api-tg-app.midas.app/api/tasks/start/'+str(anjoy[0])
                s.post(urlstart, headers=header)
            elif item['state'] == 'CLAIMABLE':
                list_id = []
                list_name = []
                list_bonus = []
                list_id.append(item['id'])
                list_name.append(item['name'])
                list_bonus.append(item['points'])
                
                anjoy = list_id + list_name + list_bonus
                urlclaim = 'https://api-tg-app.midas.app/api/tasks/claim/'+str(anjoy[0])
                responseclaim = s.post(urlclaim, headers=header)
                if responseclaim.status_code == 201:
                    Log.success('task ' + anjoy[1] + ' claimed!, rewarded ' + str(anjoy[2]) + ' GM Points')
            

    except:
        Log.error('[getTask] failed, restarting')

def getreff(tomket):
    try:
        urlreff = "https://api-tg-app.midas.app/api/referral/status"
        urlclaimref = "https://api-tg-app.midas.app/api/referral/claim"
        s = requests.Session()
        s.headers.update({"Authorization": "Bearer "+tomket})
        response = s.get(urlreff, headers=header)
        if response.status_code == 200:
            jData=response.json()
            jsoncanClaim =  jData['canClaim']
            jsontotalPoints =  jData['totalPoints']
            jsontotalTickets =  jData['totalTickets']
            Log.success('refferal Points : '+ Fore.RESET + str(jsontotalPoints))
            Log.success('refferal Tickets : '+ Fore.RESET + str(jsontotalTickets))
            if jsoncanClaim == True:
                Log.warn('can claim reff : '+ Fore.GREEN + str(jsoncanClaim))
                Log.warn('claiming..')
                response2 = s.post(urlclaimref, headers=header)
                if response2.status_code == 201:
                    Log.success('Refferal rewards claimed successfully')
            else:
                Log.warn('can claim reff : '+ Fore.RED + str(jsoncanClaim))

    except:
        Log.error('[getreff] failed, restarting')

def sleep(num):
    for i in range(num):
        print("wait {} seconds".format(num - i), end='\r')
        time.sleep(1)


def postrequest(bearer):

    s = requests.Session()
    s.headers.update({"Authorization": "Bearer "+bearer})


    try:
        
        getuser(bearer)
        getcheckin(bearer)

        if tix > 0:
            Log.warn('have a game tickets!')
            Log.warn('start playing..')
            playgame(bearer)

        getreff(bearer)
        gettask(bearer)

    except:

        Log.error('[playgame] error restarting')
        time.sleep(5)
        runforeva()

    print('-==========[github.com/raihante/midas]==========-')
    sleep(30)


# NYALAIN SENDIRI ABANGKUHH
if __name__ == "__main__":
    try:
        banner()
        runforeva()
    except KeyboardInterrupt:
        sys.exit()


#{"message":"Can't start farming","error":"Bad Request","statusCode":400}
#{'status': 'ok', 'data': {'status': 'ok', 'exp': 28800000}}