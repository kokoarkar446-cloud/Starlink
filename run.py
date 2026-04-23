import requests, urllib3, time, os, subprocess, sys, random

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

    # ၁။ Offline Login (File ရှိနေရင် အင်တာနက်မစစ်ဘဲ Dashboard တန်းပြမယ်)
    if os.path.exists(LICENSE_FILE):
        print(f"{col('G')}[✓] Status: Active (Offline Auto Login Success){col('OFF')}")
        time.sleep(1)
        return True

    # ၂။ Online Activation (File မရှိမှ တစ်ခါပဲ အင်တာနက်စစ်မယ်)
    print(f"{col('W')}[*] First Time Activation. Connecting to Server...{col('OFF')}")
    resp = requests.get(f"{RAW_KEY_URL}?t={random.random()}", timeout=15).text
    
    print(f"{col('W')}[+] YOUR DEVICE ID: {col('Y')}{hwid}{col('OFF')}")
    print(col("C") + " -----------------------------------" + col("OFF"))
    key = input(f"{col('Y')}[?] ENTER LICENSE KEY: {col('OFF')}").strip()

    # Key:ID format ကို GitHub က စာသားထဲမှာ ရှာမယ်
    if f"{key}:{hwid}" in resp:
        with open(LICENSE_FILE, "w") as f:
            f.write(key)
        print(f"{col('G')}[✓] Access Granted! License Saved for Offline Use.{col('OFF')}")
        time.sleep(2)
        return True
    else:
        print(f"{col('R')}[!] Invalid Key or Unauthorized ID.{col('OFF')}")
        sys.exit()

def main_dashboard():
    banner()
    print(f"{col('Y')}--- [ RUIJIE BYPASS DASHBOARD ] ---{col('OFF')}")
    print(f"{col('G')}[1] Start Bypass Protocol")
    print(f"{col('G')}[2] Device Info")
    print(f"{col('G')}[3] Settings")
    print(f"{col('R')}[0] Exit Program{col('OFF')}")
    
    choice = input(f"\n{col('C')}Select Option >> {col('OFF')}")
    
    if choice == "1":
        print(f"\n{col('P')}[+] Bypass System is Online...{col('OFF')}")
        # ဒီနေရာမှာ သင်လုပ်စေချင်တဲ့ Bypass Script တွေကို ထည့်ပါ
    elif choice == "0":
        sys.exit()
    else:
        main_dashboard()

if __name__ == "__main__":
    # Program စတင်ခြင်း
    if verify():
        main_dashboard()
