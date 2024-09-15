# MIDAS BOT
# Author    : @fakinsit
# Date      : 09/09/24

import os, time, sys, re, json, cloudscraper, logging
from urllib.parse import unquote
from datetime import datetime
from pyfiglet import Figlet
from colorama import Fore, Style, init
init(autoreset=True)

logging.basicConfig(filename='re.log', level=logging.ERROR, format='[%(asctime)s] - %(levelname)s - [%(message)s]')

def get_formatted_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class MidasBot:
    def __init__(self):
        self.tix = 0
        self.token_file = 'account_token.json'
        self.query_file = 'quentod.txt'
        self.api_url_base = "https://api-tg-app.midas.app/api"
        self.header_base = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
            'Accept': 'application/json, text/plain, */*',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'Origin': 'https://prod-tg-app.midas.app',
            'Referer': 'https://prod-tg-app.midas.app/',
        }
        self.scraper = cloudscraper.create_scraper()
        self.start_color = (0, 0, 255)
        self.end_color = (128, 0, 128)

    def banner(self):
        os.system("title MIDAS BOT" if os.name == "nt" else "clear")
        os.system("cls" if os.name == "nt" else "clear")
        custom_fig = Figlet(font='slant')
        self.print_gradient_text(custom_fig.renderText(' MIDAS'), self.start_color, self.end_color)
        print(Fore.RED + '[#] [C] R E G E X    ' + Fore.GREEN + '[MIDAS BOT] $$ ' + Fore.RESET)
        print(Fore.GREEN + '[#] Welcome & Enjoy !', Fore.RESET)
        print(Fore.YELLOW + '[#] Having Troubles? PM Telegram [t.me/fakinsit]', Fore.RESET)
        print('')

    def load_query_ids(self):
        timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
        try:
            with open(self.query_file, 'r') as file:
                print(f"[{timestamp}] - Loaded query IDs from {Fore.GREEN}{self.query_file}{Fore.RESET}")
                return file.read().splitlines()
        except FileNotFoundError:
            print(f"[{timestamp}] - {Fore.RED}Error: File {Fore.RED}{self.query_file}{Fore.RESET} not found.")
            return []

    def save_token(self, username, token):
        timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
        try:
            data = {}
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r') as f:
                    data = json.load(f)
            data[username] = token
            with open(self.token_file, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"[{timestamp}] - Token saved for username: {Fore.GREEN}@{username}{Fore.RESET}")
        except Exception as e:
            print(f"[{timestamp}] - {Fore.RED}Error: Failed to save token for @{username}: {e}{Fore.RESET}")

    def load_token(self, username):
        timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r') as f:
                    data = json.load(f)
                return data.get(username)
            return None
        except Exception as e:
            print(f"[{timestamp}] - {Fore.RED}Error: Failed to load token for @{username}: {e}{Fore.RESET}")
            return None

    def validate_token(self, token):
        headers = self.header_base.copy()
        headers['Authorization'] = f'Bearer {token}'
        url = f"{self.api_url_base}/referral/referred-users"
        timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
        try:
            response = self.scraper.get(url, headers=headers)
            if response.status_code == 200:
                print(f"[{timestamp}] - {Fore.GREEN}Token validation successful{Fore.RESET}")
                return True
            else:
                logging.error(f"[validate_token] HTTP {response.status_code}")
                print(f"[{timestamp}] - {Fore.RED}Error: Token validation failed. HTTP {response.status_code}{Fore.RESET}")
                print(f"[{timestamp}] - {Fore.RED}Tips: Try to restart the internet / wifi{Fore.RESET}")
                return False
        except Exception as e:
            logging.error(f"[validate_token] Error: {e}")
            print(f"[{timestamp}] - {Fore.RED}Error: Token validation failed due to {e}{Fore.RESET}")
            print(f"[{timestamp}] - {Fore.RED}Tips: Try to restart the internet / wifi{Fore.RESET}")
            return False

    def get_token(self, query_id):
        headers = self.header_base.copy()
        url = f"{self.api_url_base}/auth/register"
        data = {"initData": query_id}
        timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
        try:
            response = self.scraper.post(url, headers=headers, json=data)
            if response.status_code == 201:
                print(f"[{timestamp}] - {Fore.GREEN}Login successful{Fore.RESET}")
                return response.text
            else:
                logging.error(f"[get_token] HTTP {response.status_code}")
                print(f"[{timestamp}] - {Fore.RED}Error: Failed to get token. HTTP {response.status_code}{Fore.RESET}")
                print(f"[{timestamp}] - {Fore.RED}Tips: Try to restart the internet / wifi{Fore.RESET}")
                return None
        except Exception as e:
            logging.error(f"[get_token] Error: {e}")
            print(f"[{timestamp}] - {Fore.RED}Error: Failed to get token due to {e}{Fore.RESET}")
            print(f"[{timestamp}] - {Fore.RED}Tips: Try to restart the internet / wifi{Fore.RESET}")
            return None

    def process_accounts(self):
        query_ids = self.load_query_ids()
        timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
        for query_id in query_ids:
            username = self.get_username(query_id)
            self.turudek(30)
            if username:
                token = self.load_token(username)
                if not token or not self.validate_token(token):
                    print(f"[{timestamp}] - {Fore.YELLOW}Token for {Fore.WHITE}@{username}{Fore.YELLOW} is expired or missing. Generating a new token...{Fore.RESET}")
                    token = self.get_token(query_id)
                    if token:
                        self.save_token(username, token)
                if token:
                    self.perform_tasks(token)
        print(f"[{timestamp}] - {Fore.GREEN}All accounts processed. Waiting for 1 hours...{Fore.RESET}")
        self.turudek(1 * 60 * 60)

    def perform_tasks(self, token):
        self.check_in(token)
        self.get_user_info(token)
        self.play_game_if_needed(token)
        self.claim_tasks(token)
        self.check_referrals(token)
        print(f"{Fore.WHITE}-==========[github.com/raihante/midas]==========-{Fore.RESET}")

    def get_username(self, query_id):
        timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
        try:
            found = re.search('user=([^&]*)', query_id).group(1)
            decoded_user_part = unquote(found)
            user_obj = json.loads(decoded_user_part)
            username = user_obj['username']
            print(f"[{timestamp}] - Username: {Fore.GREEN}@{username}{Fore.RESET}")
            return username
        except Exception as e:
            print(f"[{timestamp}] - {Fore.RED}Error: Failed to extract username: {e}{Fore.RESET}")
            return None

    def check_in(self, token):
        headers = self.header_base.copy()
        headers['Authorization'] = f'Bearer {token}'
        url = f"{self.api_url_base}/streak"
        timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
        try:
            response = self.scraper.get(url, headers=headers)
            if response.status_code == 200:
                if response.json().get('claimable'):
                    self.scraper.post(url, headers=headers)
                    print(f"[{timestamp}] - {Fore.GREEN}Check-in successful{Fore.RESET}")
                else:
                    print(f"[{timestamp}] - {Fore.YELLOW}already check-in{Fore.RESET}")
            else:
                logging.error(f"[check_in] HTTP {response.status_code}")
                print(f"[{timestamp}] - {Fore.RED}Error: Check-in failed. HTTP {response.status_code}{Fore.RESET}")
        except Exception as e:
            logging.error(f"[check_in] Error: {e}")
            print(f"[{timestamp}] - {Fore.RED}Error: Check-in failed due to {e}{Fore.RESET}")

    def get_user_info(self, token):
        headers = self.header_base.copy()
        headers['Authorization'] = f'Bearer {token}'
        url = f"{self.api_url_base}/user"
        timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
        try:
            response = self.scraper.get(url, headers=headers)
            if response.status_code == 200:
                user_info = response.json()
                self.tix = user_info.get('tickets', 0)
                print(f"[{timestamp}] - BALANCE : {Fore.GREEN}{user_info['points']}{Fore.RESET} GM")
                print(f"[{timestamp}] - CHECK-IN : {Fore.GREEN}{user_info['streakDaysCount']}{Fore.RESET} DAYS")
                print(f"[{timestamp}] - TICKETS : {Fore.GREEN}{self.tix}{Fore.RESET}")
            else:
                logging.error(f"[get_user_info] HTTP {response.status_code}")
                print(f"[{timestamp}] - {Fore.RED}Error: Failed to retrieve user info. HTTP {response.status_code}{Fore.RESET}")
        except Exception as e:
            logging.error(f"[get_user_info] Error: {e}")
            print(f"[{timestamp}] - {Fore.RED}Error: Failed to retrieve user info due to {e}{Fore.RESET}")

    def play_game_if_needed(self, token):
        headers = self.header_base.copy()
        headers['Authorization'] = f'Bearer {token}'
        url = f"{self.api_url_base}/game/play"
        timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
        if self.tix > 0:
            print(f"[{timestamp}] - {Fore.GREEN}Playing games with {self.tix} tickets...{Fore.RESET}")
            for _ in range(self.tix):
                try:
                    response = self.scraper.post(url, headers=headers)
                    if response.status_code == 201:
                        reward = response.json().get('points', 0)
                        print(f"[{timestamp}] - Game played, reward: {Fore.GREEN}{reward} points{Fore.RESET}")
                    else:
                        logging.error(f"[play_game_if_needed] HTTP {response.status_code}")
                        print(f"[{timestamp}] - {Fore.RED}Error: Failed to play game. HTTP {response.status_code}{Fore.RESET}")
                    self.turudek(15)
                except Exception as e:
                    logging.error(f"[play_game_if_needed] Error: {e}")
                    print(f"[{timestamp}] - {Fore.RED}Error: Failed to play game due to {e}{Fore.RESET}")

    def claim_tasks(self, token):
        headers = self.header_base.copy()
        headers['Authorization'] = f'Bearer {token}'
        url = f"{self.api_url_base}/tasks/available"
        timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
        try:
            response = self.scraper.get(url, headers=headers)
            if response.status_code == 200:
                tasks = response.json()
                for task in tasks:
                    task_id = task['id']
                    if task['state'] == 'CLAIMABLE':
                        print(f"[{timestamp}] - {Fore.GREEN}task : {task['name']}{Fore.RESET}")
                        claim_url = f"{self.api_url_base}/tasks/claim/{task_id}"
                        self.scraper.post(claim_url, headers=headers)
                        print(f"[{timestamp}] - Task {Fore.GREEN}'{task['name']}'{Fore.RESET} claimed with {Fore.GREEN}{task['points']} points{Fore.RESET}")
                    elif task['state'] == 'WAITING':
                        start_url = f"{self.api_url_base}/tasks/start/{task_id}"
                        self.scraper.post(start_url, headers=headers)
            else:
                logging.error(f"[claim_tasks] HTTP {response.status_code}")
                print(f"[{timestamp}] - {Fore.RED}Error: Failed to claim tasks. HTTP {response.status_code}{Fore.RESET}")
        except Exception as e:
            logging.error(f"[claim_tasks] Error: {e}")
            print(f"[{timestamp}] - {Fore.RED}Error: Failed to claim tasks due to {e}{Fore.RESET}")

    def check_referrals(self, token):
        headers = self.header_base.copy()
        headers['Authorization'] = f'Bearer {token}'
        status_url = f"{self.api_url_base}/referral/status"
        claim_url = f"{self.api_url_base}/referral/claim"
        timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
        try:
            response = self.scraper.get(status_url, headers=headers)
            if response.status_code == 200:
                referral_info = response.json()
                if referral_info.get('canClaim') == True:
                    self.scraper.post(claim_url, headers=headers)
                    print(f"[{timestamp}] - {Fore.GREEN}Referral rewards claimed{Fore.RESET}")
                else:
                    print(f"[{timestamp}] - can claim ref : {Fore.RED}False{Fore.RESET}")
            else:
                logging.error(f"[check_referrals] HTTP {response.status_code}")
                print(f"[{timestamp}] - {Fore.RED}Error: Failed to check referrals. HTTP {response.status_code}{Fore.RESET}")
        except Exception as e:
            logging.error(f"[check_referrals] Error: {e}")
            print(f"[{timestamp}] - {Fore.RED}Error: Failed to check referrals due to {e}{Fore.RESET}")

    def rgb_to_ansi(self, r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    def interpolate_color(self, start_color, end_color, factor: float):
        return (
            int(start_color[0] + (end_color[0] - start_color[0]) * factor),
            int(start_color[1] + (end_color[1] - start_color[1]) * factor),
            int(start_color[2] + (end_color[2] - start_color[2]) * factor),
        )

    def print_gradient_text(self, text, start_color, end_color):
        colored_text = ""
        for i, char in enumerate(text):
            factor = i / (len(text) - 1) if len(text) > 1 else 1
            r, g, b = self.interpolate_color(start_color, end_color, factor)
            colored_text += self.rgb_to_ansi(r, g, b) + char
        print(colored_text + "\033[0m")

    def turudek(self, total_seconds):
        bar_length = 25
        start_time = time.time()
        end_time = start_time + total_seconds
        while True:
            current_time = time.time()
            remaining_time = end_time - current_time
            if remaining_time <= 0:
                print(f"[{Fore.MAGENTA}{get_formatted_time()}{Fore.RESET}] - {Fore.GREEN}Time's up!, waiting..{Fore.RESET}", end='\r')
                break
            elapsed_time = total_seconds - remaining_time
            blocks_filled = int(bar_length * (elapsed_time / total_seconds))
            progress_bar = ""
            for i in range(blocks_filled):
                factor = i / (blocks_filled - 1) if blocks_filled > 1 else 1
                r, g, b = self.interpolate_color(self.start_color, self.end_color, factor)
                progress_bar += self.rgb_to_ansi(r, g, b) + "#"
            empty_space = "-" * (bar_length - blocks_filled)
            hours = int(remaining_time // 3600)
            minutes = int((remaining_time % 3600) // 60)
            seconds = int(remaining_time % 60)
            time_remaining = f"{hours:02}:{minutes:02}:{seconds:02}"
            print(f"[{Fore.MAGENTA}{Fore.YELLOW}WAIT TIME: {time_remaining}{Fore.RESET}] - [{progress_bar}{Fore.YELLOW}{empty_space}{Fore.RESET}]", end='\r')
            time.sleep(0.1)

    def run(self):
        try:
            self.banner()
            while True:
                self.process_accounts()
        except KeyboardInterrupt:
            timestamp = Fore.MAGENTA + get_formatted_time() + Fore.RESET
            print(f"[{timestamp}] - {Fore.RED}Exiting MIDAS BOT...{Fore.RESET}")
            sys.exit()

if __name__ == "__main__":
    bot = MidasBot()
    bot.run()
