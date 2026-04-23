import requests, urllib3, time, os, subprocess, sys, random
from datetime import datetime

# SSL Warnings ပိတ်ခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- [ CONFIGURATION ] ---
RAW_KEY_URL = "https://raw.githubusercontent.com/kokoarkar446-cloud/Bypass-code/main/keys.txt"
LICENSE_FILE = "license.txt"

# --- [ SYSTEM COLORS ] ---
def col(c):
    codes = {
        "Y": "\033[93m", "G": "\033[92m", "R": "\033[91m", 
        "C": "\033[96m", "P": "\033[95m", "W": "\033[97m", "OFF": "\033[0m"
    }
    return codes.get(c, "\033[0m")

def get_hwid():
    # ID ကို Whoami ဖြင့် ရယူခြင်း
    return f"ID-{subprocess.check_output(['whoami']).decode().strip()}"

def banner():
    os.system('clear')
    print(col("Y") + " ="*35 + col("OFF"))
    print(col("C") + """
      ██████╗ ██╗   ██╗██╗     ██╗██╗███████╗
      ██╔══██╗██║   ██║██║     ██║██║██╔════╝
      ██████╔╝██║   ██║██║     ██║██║█████╗  
      ██╔══██╗██║   ██║██║██   ██║██║██╔══╝  
      ██║  ██║╚██████╔╝██║╚█████╔╝██║███████╗
      ╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚════╝ ╚═╝╚══════╝""" + col("OFF"))
    print(f"        {col('R')}✨ Ruijie Bypass - PREMIUM EDITION ✨{col('OFF')}")
    print(col("Y") + " ="*35 + col("OFF") + "\n")

def verify():
    hwid = get_hwid()
    banner()
    now = datetime.now()

    # ၁။ Offline Auto Login (File ရှိရင် ရက်စွဲပါ တိုက်စစ်မယ်)
    if os.path.exists(LICENSE_FILE):
        with open(LICENSE_FILE, "r") as f:
            saved_data = f.read().strip().split(":")
        
        # Saved Format -> key:expiry_date
        saved_date = datetime.strptime(saved_data[1], '%Y-%m-%d')
        
        # သက်တမ်းကျန်သေးလား စစ်မယ်
        if (saved_date - now).days >= 0:
            print(f"{col('G')}[✓] Status: Premium Active (Exp: {saved_data[1]}){col('OFF')}")
            time.sleep(1)
            return True
        else:
            print(f"{col('R')}[!] Your Key has Expired!{col('OFF')}")
            os.remove(LICENSE_FILE) # သက်တမ်းကုန်ဖိုင်ကို ဖျက်မယ်
            sys.exit()

    # ၂။ Online Activation (ပထမဆုံးအကြိမ်အတွက်)
    print(f"{col('W')}[*] Connecting to License Server...{col('OFF')}")
    resp = requests.get(f"{RAW_KEY_URL}?t={random.random()}", timeout=15).text
    
    print(f"{col('W')}[+] YOUR DEVICE ID: {col('Y')}{hwid}{col('OFF')}")
    print(col("C") + " -----------------------------------" + col("OFF"))
    key = input(f"{col('Y')}[?] ENTER LICENSE KEY: {col('OFF')}").strip()

    # GitHub ထဲမှာ Key:ID:Date ပုံစံရှိမရှိ စစ်မယ်
    for line in resp.splitlines():
        if f"{key}:{hwid}" in line:
            parts = line.split(":")
            exp_date_str = parts[2] # ဥပမာ - 2026-12-30
            exp_date = datetime.strptime(exp_date_str, '%Y-%m-%d')
            
            # ရက်စွဲကို ထပ်စစ်မယ်
            if (exp_date - now).days >= 0:
                with open(LICENSE_FILE, "w") as f:
                    f.write(f"{key}:{exp_date_str}")
                print(f"{col('G')}[✓] Access Granted! Exp: {exp_date_str}{col('OFF')}")
                time.sleep(2)
                return True
            else:
                print(f"{col('R')}[!] Key is Expired on {exp_date_str}{col('OFF')}")
                sys.exit()

    print(f"{col('R')}[!] Invalid Key or Unauthorized ID.{col('OFF')}")
    sys.exit()

def main_dashboard():
    banner()
    print(f"{col('Y')}--- [ RUIJIE BYPASS DASHBOARD ] ---{col('OFF')}")
    print(f"{col('G')}[1] Start Bypass Protocol")
    print(f"{col('G')}[2] Check Status")
    print(f"{col('R')}[0] Exit Program{col('OFF')}")
    
    choice = input(f"\n{col('C')}Select Option >> {col('OFF')}")
    
    if choice == "1":
        print(f"\n{col('P')}[+] System Running...{col('OFF')}")
        # သင့်ရဲ့ Bypass လုပ်မယ့် Function တွေကို ဒီမှာထည့်ပါ
    elif choice == "0":
        sys.exit()
    else:
        main_dashboard()

if __name__ == "__main__":
    if verify():
        main_dashboard()
