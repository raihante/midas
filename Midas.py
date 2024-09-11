# MIDAS BOT
# Author    : @fakinsit
# Date      : 09/09/24

import os
import time
import sys
import re
import json
import urllib.request
import urllib.parse
from urllib.parse import unquote
from pyfiglet import Figlet
from colorama import Fore
from onlylog import Log



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
        sleep(10)
        Log.error('[MAIN] error, restarting')
        runforeva()

def gettoken(querybro):
    header =   {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
            }
    try:
        url = "https://api-tg-app.midas.app/api/auth/register"
        redrop = json.dumps({"initData":querybro}).encode('utf-8')
        req = urllib.request.Request(url, redrop, header, method='POST')
        response = urllib.request.urlopen(req)
        if response.getcode() != 201:
            Log.error('[gettoken] error, check your query_id / user_id maybe expired')
        elif response.getcode() == 500:
            Log.error('[gettoken] error, close all Midas mini-app!')
            sleep(30)
        else:
            Log.success('login success')
            cihuy = response.read().decode('utf-8')
            return cihuy
    except:
        Log.error('[gettoken] error restarting, check your query_id / user_id maybe expired')

def getuser(querybro):
    bear = 'Bearer '+querybro
    header =   {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Authorization': bear
            }
    
    global tix

    try:
        url = "https://api-tg-app.midas.app/api/user"
        urlvisit = "https://api-tg-app.midas.app/api/user/visited"
        req = urllib.request.Request(url, None, header, method='GET')
        response = urllib.request.urlopen(req).read()
        result = json.loads(response.decode('utf-8'))
        jData=result
        jsonpoints =  jData['points']
        jsonsd =  jData['streakDaysCount']
        jsontix =  jData['tickets']
        Log.warn('GM points : '+ str(jsonpoints))
        Log.warn('check-in Day : '+ str(jsonsd))
        Log.warn('tickets : '+ str(jsontix))
        tix = jsontix
        try:
            reqv = urllib.request.Request(urlvisit, None, header, method='PATCH')
            urllib.request.urlopen(reqv)
        except:
            None
    except:
        Log.error('[getuser] error restarting, check your query_id / user_id maybe expired')

def getcheckin(querybro):
    bear = 'Bearer '+querybro
    header =   {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Authorization': bear
        }
        
    url = "https://api-tg-app.midas.app/api/streak"
    
    try:

        req = urllib.request.Request(url, None, header, method='GET')
        response = urllib.request.urlopen(req).read()
        result = json.loads(response.decode('utf-8'))
        jData=result
        jsonclaimable =  jData['claimable']
        if jsonclaimable == True:
            try:
                req = urllib.request.Request(url, None, header, method='POST')
                response = urllib.request.urlopen(req)
                Log.s('check-in success!')
            except:
                None
        
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
    bear = 'Bearer '+tomket
    header =   {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Authorization': bear
    }

    n = tix

    for i in range(0, n):
        try:
            url = "https://api-tg-app.midas.app/api/game/play"
            req = urllib.request.Request(url, None, header, method='POST')
            response = urllib.request.urlopen(req).read()
            result = json.loads(response.decode('utf-8'))
            jData=result
            try:
                jsonreward =  jData['points']
                Log.success('succes play game, reward : '+ str(jsonreward))
                sleep(5)
            except:
                None
        except:
            Log.error('[playgame] failed, restarting')


def gettask(tomket):
    bear = 'Bearer '+tomket
    header =   {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': bear
        }

    try:
        urltasks = "https://api-tg-app.midas.app/api/tasks/available"
        req = urllib.request.Request(urltasks, None, header, method='GET')
        response = urllib.request.urlopen(req).read()
        result = json.loads(response.decode('utf-8'))
        jData=result
        for item in jData: 
            if item['state'] == 'WAITING':
                list_id = []
                list_name = []
                list_id.append(item['id'])
                list_name.append(item['name'])
                anjoy = list_id + list_name
                try:
                    urlstart = 'https://api-tg-app.midas.app/api/tasks/start/'+str(anjoy[0])
                    req2 = urllib.request.Request(urlstart, None, header, method='POST')
                    urllib.request.urlopen(req2).read()
                except:
                    None
            elif item['state'] == 'CLAIMABLE':
                list_id = []
                list_name = []
                list_bonus = []
                list_id.append(item['id'])
                list_name.append(item['name'])
                list_bonus.append(item['points'])
                
                anjoy = list_id + list_name + list_bonus
                try:
                    urlclaim = 'https://api-tg-app.midas.app/api/tasks/claim/'+str(anjoy[0])
                    req3 = urllib.request.Request(urlclaim, None, header, method='POST')
                    responseclaim = urllib.request.urlopen(req3)
                    if responseclaim.getcode() == 201:
                        Log.success('task ' + anjoy[1] + ' claimed!, rewarded ' + str(anjoy[2]) + ' GM Points')
                except:
                    None

    except:
        Log.error('[getTask] failed, restarting')

def getreff(tomket):
    bear = 'Bearer '+tomket
    header =   {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Authorization': bear
    }

    try:
        urlreff = "https://api-tg-app.midas.app/api/referral/status"
        urlclaimref = "https://api-tg-app.midas.app/api/referral/claim"
        req = urllib.request.Request(urlreff, None, header, method='GET')
        response = urllib.request.urlopen(req).read()
        result = json.loads(response.decode('utf-8'))
        jData=result
        if jData['totalPoints'] > 0:
            jsoncanClaim =  jData['canClaim']
            jsontotalPoints =  jData['totalPoints']
            jsontotalTickets =  jData['totalTickets']
            Log.success('refferal Points : '+ Fore.RESET + str(jsontotalPoints))
            Log.success('refferal Tickets : '+ Fore.RESET + str(jsontotalTickets))
            if jsoncanClaim == True:
                Log.warn('can claim reff : '+ Fore.GREEN + str(jsoncanClaim))
                Log.warn('claiming..')
                req = urllib.request.Request(urlclaimref, None, header, method='POST')
                responseclaim = urllib.request.urlopen(req)
                if responseclaim.getcode() == 201:
                    Log.success('Refferal rewards claimed successfully')
            else:
                Log.warn('can claim reff : '+ Fore.RED + str(jsoncanClaim))
        else:
                Log.warn('can claim reff : '+ Fore.RED + str(jData['canClaim']))
    except:
        Log.error('[getreff] failed, restarting')

def sleep(num):
    for i in range(num):
        print("wait {} seconds".format(num - i), end='\r')
        time.sleep(1)


def postrequest(bearer):

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
        Log.error('[postrequest] error restarting')
        time.sleep(5)
        runforeva()

    print('-==========[github.com/raihante/midas]==========-')
    sleep(60)


# NYALAIN SENDIRI ABANGKUHH
if __name__ == "__main__":
    try:
        banner()
        runforeva()
    except KeyboardInterrupt:
        sys.exit()
