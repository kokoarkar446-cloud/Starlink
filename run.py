import requests, re, urllib3, time, threading, os, random, subprocess, sys, base64
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- ENCODED CONFIG ---
# GitHub Raw Link
_0x446 = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2tva29hcmthcjQ0Ni1jbG91ZC9TdGFybGluay9tYWluL2tleS50eHQ="
_0x112 = "LnN5c3RlbV9jb25maWdfZGF0YV9sb2c="

def get_link(): return base64.b64decode(_0x446).decode()
def get_file(): return base64.b64decode(_0x112).decode()

# --- COLORS ---
Y, G, R, W, C, M, OFF = "\033[1;33m", "\033[1;32m", "\033[1;31m", "\033[1;37m", "\033[1;36m", "\033[1;35m", "\033[0m"

def get_uid():
    try: return subprocess.check_output(['whoami']).decode('utf-8').strip()
    except: return "u0_a128"

def check_access():
    uid = get_uid()
    now = datetime.now()
    v_url = get_link()
    v_file = get_file()

    # 1. Offline Check
    if os.path.exists(v_file):
        try:
            with open(v_file, "r") as f:
                d = f.read().split('|')
                if d[0] == uid:
                    expire_time = datetime.strptime(d[2].strip(), "%Y-%m-%d %H:%M")
                    if now < expire_time:
                        return True, d[1], d[2]
        except: pass

    # 2. Access Denied & Key Input UI
    os.system('clear')
    print(f" {R}╔══════════════════════════════════════════╗")
    print(f" ║          AUTHENTICATION REQUIRED         ║")
    print(f" ╚══════════════════════════════════════════╝{OFF}")
    print(f"\n {G}⚡ YOUR ID : {W}{uid}{OFF}")
    print(f" {Y}[!] Send your ID to Admin to buy a Key.{OFF}")
    print(f" {W}------------------------------------------{OFF}")
    
    # ဒီနေရာမှာ Key ကို တောင်းမှာပါ
    user_key = input(f" {C}[+] ENTER YOUR KEY : {W}").strip()
    
    if not user_key:
        print(f" {R}[!] Key cannot be empty!{OFF}")
        sys.exit()

    try:
        print(f" {Y}[*] Verifying Key with server...{OFF}")
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(f"{v_url}?t={random.random()}", headers=headers, timeout=15)
        
        if res.status_code == 200:
            for line in res.text.splitlines():
                # GitHub ထဲက Key နဲ့ User ရိုက်တဲ့ Key တူ၊ မတူ စစ်မယ်
                if user_key in line and uid in line:
                    with open(v_file, "w") as f: f.write(line)
                    p = line.split('|')
                    print(f" {G}[✓] KEY ACTIVATED SUCCESSFULLY!{OFF}")
                    time.sleep(2)
                    return True, p[1].strip(), p[2].strip()
            
            print(f" {R}[!] INVALID KEY OR UNREGISTERED ID!{OFF}")
            sys.exit()
    except:
        print(f" {R}[!] CONNECTION ERROR: Internet required for Activation.{OFF}")
        sys.exit()

def turbo_pulse(link):
    while True:
        try:
            requests.get(link, timeout=5, verify=False)
            print(f" {Y}[{G}✓{R}] {W}TURBO ACTIVE >>> {C}[{random.randint(10,60)}ms] {OFF}", end="\r")
        except: time.sleep(0.5)

def start_speed_logic():
    # Bypass Logic... (အရင်အတိုင်း)
    print(f"\n {G}[✓] BYPASS SEQUENCE STARTED...{OFF}")
    # (ဒီနေရာမှာ သင့်ရဲ့ bypass ကုဒ်တွေ ဆက်ထည့်ပါ)
    # ဥပမာ- turbo_pulse စတာတွေ...

if __name__ == "__main__":
    status, name, exp = check_access()
    if status:
        os.system('clear')
        print(f" {G}[✓] LOGIN SUCCESS: Welcome {name}{OFF}")
        print(f" {C}[#] Expiry Date: {exp}{OFF}\n")
        start_speed_logic()
