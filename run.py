import requests, urllib3, time, os, subprocess, sys, random
from datetime import datetime

# SSL Bypass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- [ CONFIGURATION ] ---
# သင်အသုံးပြုမည့် VIP Key List Link
PRIMARY_URL = "https://raw.githubusercontent.com/painglintun895-rgb/my-keys/refs/heads/main/vips.txt"

def get_uid():
    """Device UID (Hardware ID) ကို ရယူခြင်း"""
    try:
        # Android device serial ကို အရင်စစ်မယ်
        uid = subprocess.check_output(['getprop', 'ro.serialno'], stderr=subprocess.STDOUT).decode('utf-8').strip()
        if not uid: raise Exception
        return f"ID-{uid}"
    except:
        # Serial ရှာမရပါက Username ကို ယူမယ်
        try: return f"ID-{subprocess.check_output(['whoami']).decode('utf-8').strip()}"
        except: return "ID-UNKNOWN-USER"

def banner(name="GUEST", exp="Checking...", days="--", col="\033[92m"):
    """Starlink & KoCLAY Style Combined UI Banner"""
    os.system('clear')
    print("\033[93m" + " ="*38)
    print("\033[96m" + """
     ██╗  ██╗ ██████╗  ██████╗██╗      █████╗ ██╗   ██╗
     ██║ ██╔╝██╔═══██╗██╔════╝██║     ██╔══██╗╚██╗ ██╔╝
     █████╔╝ ██║   ██║██║     ██║     ███████║ ╚████╔╝ 
     ██╔═██╗ ██║   ██║██║     ██║     ██╔══██║  ╚██╔╝  
     ██║  ██╗╚██████╔╝╚██████╗███████╗██║  ██║   ██║   
     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝   """)
    print(f"\033[95m 👑 MASTER: {name} | ID: {get_uid()}")
    print(f"\033[92m 📅 EXP: {exp} | ⏳ REMAINING: {days} Days")
    print(f"\033[93m ="*7 + f" [ {col}PREMIUM KEY SYSTEM ACTIVE\033[93m ] " + "="*8)
    print("\033[0m")

def check_access():
    """Key System Logic: UID နှင့် Expiry ကို Server တွင် တိုက်စစ်ခြင်း"""
    uid = get_uid()
    
    # ၁။ Server Time ယူခြင်း (အချိန်ခိုးပြင်တာ တားဆီးရန်)
    try:
        r_t = requests.get("http://worldtimeapi.org/api/timezone/Asia/Yangon", timeout=5)
        now = datetime.strptime(r_t.json()['datetime'][:10], '%Y-%m-%d')
    except:
        # အင်တာနက်မရလျှင် Local Time သုံးမယ်
        now = datetime.now() 

    # ၂။ GitHub VIP List ကို စစ်ဆေးခြင်း
    try:
        print("\033[94m[*] Connecting to Starlink Database...\033[0m")
        # Cache မဖြစ်အောင် random param ထည့်ထားတယ်
        res = requests.get(f"{PRIMARY_URL}?t={random.random()}", timeout=10, verify=False)
        
        if res.status_code == 200:
            for line in res.text.splitlines():
                if uid in line:
                    # Format မျှော်လင့်ချက်: UID | Name | YYYY-MM-DD
                    parts = line.split('|')
                    v_name = parts[1].strip()
                    v_exp = parts[2].strip()
                    exp_dt = datetime.strptime(v_exp, '%Y-%m-%d')
                    
                    diff = (exp_dt - now).days
                    if diff < 0:
                        banner(v_name, v_exp, "0", "\033[91m")
                        print("\033[91m[!] Subscription Expired! Please contact Admin to Renew.\033[0m")
                        sys.exit()
                    
                    banner(v_name, v_exp, str(diff + 1))
                    return True
            
            # UID ကို list ထဲမှာ ရှာမတွေ့ပါက
            banner()
            print(f"\033[91m[!] Access Denied!\033[0m")
            print(f"\033[97mYour ID: {col_y}{uid}{col_off} is not registered in our system.")
            sys.exit()
    except Exception as e:
        print(f"\033[91m[!] Server Connection Error! Please check your internet.\033[0m")
        sys.exit()

def main_dashboard():
    """Key မှန်မှ ပွင့်လာမည့် နေရာ"""
    print(f"\033[93m--- [ SELECT AN OPTION ] ---\033[0m")
    print(f"\033[92m[1] Launch Bypass Tool")
    print(f"[2] Check Speed")
    print(f"[3] Tool Settings")
    print(f"[0] Exit Program\033[0m")
    
    opt = input(f"\n\033[96mChoose >> \033[0m")
    if opt == "1":
        print("\033[95m[+] Tool is initializing...\033[0m")
        # ဒီနေရာမှာ သင်လုပ်စေချင်တဲ့ အလုပ်တွေကို ထည့်ပါ
    else:
        print("\033[93mExiting...\033[0m")
        sys.exit()

# စာသားအရောင်များ (Helper)
col_y = "\033[93m"
col_off = "\033[0m"

if __name__ == "__main__":
    try:
        # Key စစ်မယ်
        if check_access():
            # Key မှန်ရင် Dashboard ပြမယ်
            main_dashboard()
    except KeyboardInterrupt:
        print("\n\033[91m[!] Stopped by User.\033[0m")
        os._exit(0)
