#!/usr/bin/env python3
import subprocess
import shutil
import sys
import os

# Barvy pro terminál
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def print_header(text):
    print(f"\n{CYAN}{BOLD}{'=' * 65}{RESET}")
    print(f"{CYAN}{BOLD}  {text}{RESET}")
    print(f"{CYAN}{BOLD}{'=' * 65}{RESET}")

def run_cmd(cmd):
    try:
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print(f"{RED}[CHYBA]: {e}{RESET}")

def check_os_info():
    print_header("1. SYSTEM & KERNEL OVERVIEW")
    run_cmd("uname -or && cat /etc/os-release | grep PRETTY_NAME")

def check_disk_usage():
    print_header("2. DISK SPACE HEALTH")
    # Zobrazí využití disku v lidsky čitelné formě
    run_cmd("df -h --output=source,size,used,avail,pcent,target -x tmpfs -x devtmpfs")

def check_memory_load():
    print_header("3. MEMORY & CPU LOAD")
    run_cmd("free -h && uptime")

def check_active_users():
    print_header("4. LOGGED IN USERS & SECURITY CHECK")
    run_cmd("who && w")

def main():
    try:
        while True:
            print(f"{BOLD}{CYAN}")
            print("============================================================")
            print("      ARK SYS HEALTH - UNIVERSAL SERVER PULSE CHECK         ")
            print(f"============================================================{RESET}")
            
            print("  [1] 🖥️  Zobrazit verzi OS a jádra (System & Kernel)")
            print("  [2] 💾  Kontrola zaplnění diskového prostoru (Disk Health)")
            print("  [3] 📊  Stav paměti RAM a vytížení CPU (Memory & Load)")
            print("  [4] 👤  Přehled přihlášených uživatelů (Active Sessions)")
            print("  [0] 🚪  Ukončit nástroj")
            
            try:
                choice = input(f"\n{CYAN}Zvol kontrolní akci (0-4): {RESET}").strip()
            except KeyboardInterrupt:
                print(f"\n\nUkončuji Ark Sys Health. Měj se skvěle!")
                sys.exit(0)
            
            if choice == '1':
                check_os_info()
            elif choice == '2':
                check_disk_usage()
            elif choice == '3':
                check_memory_load()
            elif choice == '4':
                check_active_users()
            elif choice == '0':
                print("\nUkončuji Ark Sys Health. Server pod kontrolou!")
                sys.exit(0)
            else:
                print(f"{RED}[!] Neplatná volba, zadej číslo 0 až 4.{RESET}")
            
            input(f"\n{YELLOW}Stiskni Enter pro návrat do menu...{RESET}")

    except KeyboardInterrupt:
        print(f"\n\nUkončuji Ark Sys Health. Bezpečné odpojení.")
        sys.exit(0)

if __name__ == "__main__":
    main()
