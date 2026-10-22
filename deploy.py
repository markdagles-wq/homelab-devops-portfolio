#!/usr/bin/env python3
import subprocess
import sys
from datetime import datetime

def run_cmd(cmd):
    """Pomocná funkce pro spuštění příkazu v terminálu."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def main():
    print("=" * 60)
    print("🚀 AUTOMATICKÝ DEPLOY NA GITHUB")
    print("=" * 60)

    # 1. Kontrola stavu depozitáře
    code, out, _ = run_cmd("git status --porcelain")
    if not out:
        print("[INFO] Žádné změny k odeslání. Vše je aktuální.")
        return

    print("[*] Detekovány změny v projektu:")
    print(out)
    print("-" * 60)

    # 2. Přidání souborů
    print("[*] Přidávám změny (git add .)...")
    code, _, err = run_cmd("git add .")
    if code != 0:
        print(f"[CHYBA] git add selhal: {err}")
        sys.exit(1)

    # 3. Vytvoření commitu s časovým razítkem
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Update documentation/portfolio ({now})"
    print(f"[*] Vytvářím commit: '{commit_msg}'...")
    
    code, _, err = run_cmd(f'git commit -m "{commit_msg}"')
    if code != 0:
        print(f"[CHYBA] git commit selhal: {err}")
        sys.exit(1)

    # 4. Push na GitHub
    print("[*] Odesílám na GitHub (git push)...")
    code, out, err = run_cmd("git push origin main")
    
    if code == 0:
        print("=" * 60)
        print("✅ ÚSPĚŠNĚ ULOŽENO A PUBLIKOVÁNO NA GITHUB!")
        print("=" * 60)
    else:
        print(f"[CHYBA] Push selhal: {err}")
        print("[TIP] Pokud to chce heslo/token, pusť skript ručně nebo nastav 'git config --global credential.helper store'")

if __name__ == "__main__":
    main()
