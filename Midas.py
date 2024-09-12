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
    print(custom_fig.renderText(' MIDAS'))
    print(Fore.RED + '[#] [C] R E G E X    ' + Fore.GREEN + '[MIDAS BOT] $$ ' + Fore.RESET)
    print(Fore.GREEN + '[#] Welcome & Enjoy !', Fore.RESET)
    print(Fore.YELLOW + '[#] Having Troubles? PM Telegram [t.me/fakinsit]', Fore.RESET)
    print('')

def runforeva():
    with open('quentod.txt', 'r') as file:
        queryh = file.read().splitlines()
        
    try:
        value = True
        while value:
            for index, query_id in enumerate(queryh, start=1):
                username = getname(query_id)
                
                # Check if username already has a token
                if has_token(username):
                    # Get the existing token
                    token = get_existing_token(username)
                    
                    # Check if the token is valid
                    if not is_token_valid(token):
                        Log.warn(f'Token for @{username} is expired. Generating a new token...')
                        token = gettoken(query_id)
                        if token:
                            save_token(username, token)
                else:
                    # If no token exists, generate a new one
                    token = gettoken(query_id)
                    if token:
                        save_token(username, token)
                
                postrequest(token)
            
            Log.success('All accounts processed. Waiting for 6 hours...')
            sleep(6 * 60 * 60)  # Wait for 6 hours (in seconds)

    except Exception as e:
        sleep(10)
        Log.error(f'[MAIN] error, restarting: {e}')
        runforeva()


def is_token_valid(token):
    """ Check if the provided token is valid. """
    bear = 'Bearer ' + token
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Host': 'api-tg-app.midas.app',
        'Origin': 'https://prod-tg-app.midas.app',
        'Pragma': 'no-cache',
        'Referer': 'https://prod-tg-app.midas.app/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Content-Type': 'application/json',
        'Authorization': bear
    }
    try:
        url = "https://api-tg-app.midas.app/api/referral/referred-users"
        req = urllib.request.Request(url, None, header, method='GET')
        response = urllib.request.urlopen(req)
        time.sleep(5)
        if response.getcode() == 200:
            return True
        else:
            return False
    except Exception as e:
        Log.error(f'[is_token_valid] Failed to check token validity: {e}')
        sleep(300)
        return False


def has_token(username):
    """ Check if the username already has a token saved. """
    if os.path.exists('account_token.json'):
        with open('account_token.json', 'r') as f:
            data = json.load(f)
        return username in data
    return False

def get_existing_token(username):
    """ Retrieve the existing token for the given username. """
    if os.path.exists('account_token.json'):
        with open('account_token.json', 'r') as f:
            data = json.load(f)
        return data.get(username, None)
    return None

def gettoken(querybro):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Host': 'api-tg-app.midas.app',
        'Origin': 'https://prod-tg-app.midas.app',
        'Pragma': 'no-cache',
        'Referer': 'https://prod-tg-app.midas.app/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Content-Type': 'application/json'
    }
    try:
        url = "https://api-tg-app.midas.app/api/auth/register"
        redrop = json.dumps({"initData": querybro}).encode('utf-8')
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
    except Exception as e:
        Log.error(f'[gettoken] Failed to get token : {e}')
        Log.error(f'[gettoken] Use 1.1.1.1 or another VPN to login first!')

def getuser(querybro):
    bear = 'Bearer ' + querybro
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Host': 'api-tg-app.midas.app',
        'Origin': 'https://prod-tg-app.midas.app',
        'Pragma': 'no-cache',
        'Referer': 'https://prod-tg-app.midas.app/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Content-Type': 'application/json',
        'Authorization': bear
    }
    
    global tix

    try:
        url = "https://api-tg-app.midas.app/api/user"
        urlvisit = "https://api-tg-app.midas.app/api/user/visited"
        req = urllib.request.Request(url, None, header, method='GET')
        response = urllib.request.urlopen(req).read()
        time.sleep(3)
        result = json.loads(response.decode('utf-8'))
        jsonpoints = result['points']
        jsonsd = result['streakDaysCount']
        jsontix = result['tickets']
        Log.warn('GM points : ' + str(jsonpoints))
        Log.warn('check-in Day : ' + str(jsonsd))
        Log.warn('tickets : ' + str(jsontix))
        tix = jsontix
        try:
            reqv = urllib.request.Request(urlvisit, None, header, method='PATCH')
            urllib.request.urlopen(reqv)
        except:
            pass
    except Exception as e:
        Log.error(f'[getuser] Failed to get user : {e}')

def getcheckin(querybro):
    bear = 'Bearer ' + querybro
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Host': 'api-tg-app.midas.app',
        'Origin': 'https://prod-tg-app.midas.app',
        'Pragma': 'no-cache',
        'Referer': 'https://prod-tg-app.midas.app/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Content-Type': 'application/json',
        'Authorization': bear
    }
    
    url = "https://api-tg-app.midas.app/api/streak"
    
    try:
        req = urllib.request.Request(url, None, header, method='GET')
        response = urllib.request.urlopen(req).read()
        result = json.loads(response.decode('utf-8'))
        jsonclaimable = result['claimable']
        if jsonclaimable == True:
            try:
                req = urllib.request.Request(url, None, header, method='POST')
                urllib.request.urlopen(req)
                Log.s('check-in success!')
            except:
                pass
    except Exception as e:
        Log.error(f'[checkin] Failed to check-in : {e}')

def getname(querybro):
    try:
        found = re.search('user=([^&]*)', querybro).group(1)
        decodedUserPart = unquote(found)
        userObj = json.loads(decodedUserPart)
        username = userObj['username']
        Log.success('username : @' + username)
        return username
    except Exception as e:
        Log.error(f'[getname] Failed to decode username : {e}')

def save_token(username, token):
    try:
        data = {}
        if os.path.exists('account_token.json'):
            with open('account_token.json', 'r') as f:
                data = json.load(f)
        data[username] = token
        with open('account_token.json', 'w') as f:
            json.dump(data, f, indent=4)
        Log.success(f'Token saved for username: @{username}')
    except Exception as e:
        Log.error(f'[save_token] Failed to save token: {e}')

def playgame(tomket):
    bear = 'Bearer ' + tomket
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Host': 'api-tg-app.midas.app',
        'Origin': 'https://prod-tg-app.midas.app',
        'Pragma': 'no-cache',
        'Referer': 'https://prod-tg-app.midas.app/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Content-Type': 'application/json',
        'Authorization': bear
    }

    n = tix

    for _ in range(n):
        try:
            url = "https://api-tg-app.midas.app/api/game/play"
            req = urllib.request.Request(url, None, header, method='POST')
            response = urllib.request.urlopen(req).read()
            result = json.loads(response.decode('utf-8'))
            jsonreward = result.get('points', 0)
            Log.success('success play game, reward : ' + str(jsonreward))
            sleep(15)
        except Exception as e:
            Log.error(f'[play_game] Failed to starting game : {e}')

def gettask(tomket):
    bear = 'Bearer '+tomket
    header =   {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Host': 'api-tg-app.midas.app',
            'Origin': 'https://prod-tg-app.midas.app',
            'Pragma': 'no-cache',
            'Referer': 'https://prod-tg-app.midas.app/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
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
                    urllib.request.urlopen(req2)
                except:
                    pass
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
                    pass

    except:
        pass

def getreff(tomket):
    bear = 'Bearer ' + tomket
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Host': 'api-tg-app.midas.app',
        'Origin': 'https://prod-tg-app.midas.app',
        'Pragma': 'no-cache',
        'Referer': 'https://prod-tg-app.midas.app/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Content-Type': 'application/json',
        'Authorization': bear
    }

    try:
        urlreff = "https://api-tg-app.midas.app/api/referral/status"
        urlclaimref = "https://api-tg-app.midas.app/api/referral/claim"
        req = urllib.request.Request(urlreff, None, header, method='GET')
        response = urllib.request.urlopen(req).read()
        result = json.loads(response.decode('utf-8'))
        if result['totalPoints'] > 0:
            jsoncanClaim = result['canClaim']
            jsontotalPoints = result['totalPoints']
            jsontotalTickets = result['totalTickets']
            Log.success('referral Points : ' + Fore.RESET + str(jsontotalPoints))
            Log.success('referral Tickets : ' + Fore.RESET + str(jsontotalTickets))
            if jsoncanClaim:
                Log.warn('can claim ref : ' + Fore.GREEN + str(jsoncanClaim))
                Log.warn('claiming..')
                req = urllib.request.Request(urlclaimref, None, header, method='POST')
                responseclaim = urllib.request.urlopen(req)
                if responseclaim.getcode() == 201:
                    Log.success('Referral rewards claimed successfully')
            else:
                Log.warn('can claim ref : ' + Fore.RED + str(jsoncanClaim))
        else:
            Log.warn('can claim ref : ' + Fore.RED + str(result['canClaim']))
    except Exception as e:
        Log.error(f'[get_reff] Failed to getting refferal : {e}')

def sleep(total_seconds):
    """Pause execution for `total_seconds` while printing remaining time in minutes, hours, seconds, and milliseconds."""
    
    start_time = time.time()
    end_time = start_time + total_seconds

    while True:
        current_time = time.time()
        remaining_time = end_time - current_time

        if remaining_time <= 0:
            print("Time's up!                      ", end='\r') 
            break
        

        hours = int(remaining_time // 3600)
        minutes = int((remaining_time % 3600) // 60)
        seconds = int(remaining_time % 60)

        # Print the formatted time remaining
        time_remaining = f"{hours:02}:{minutes:02}:{seconds:02}"
        print(f"[WAIT TIME: {time_remaining}]", end='\r')
        
        time.sleep(0.1)

def postrequest(bearer):
    try:
        getcheckin(bearer)
        getuser(bearer)
        if tix > 0:
            Log.warn('have a game tickets!')
            Log.warn('start playing..')
            playgame(bearer)
        getreff(bearer)
        gettask(bearer)
    except:
        sleep(10)
        runforeva()

    print('-==========[github.com/raihante/midas]==========-')
    sleep(300)

if __name__ == "__main__":
    try:
        banner()
        runforeva()
    except KeyboardInterrupt:
        sys.exit()
