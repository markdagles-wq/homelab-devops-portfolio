#!/usr/bin/env python3
import subprocess
import sys
import re
from datetime import datetime

# Seznam cca 10+ vzorů pro detekci citlivých dat a parametrů
SENSITIVE_PATTERNS = [
    r"BEGIN\s+PRIVATE\s+KEY",                  # 1. SSH / TLS Privátní klíče
    r"api[_-]?key\s*=\s*['\"].+['\"]",             # 2. API klíče
    r"password\s*=\s*['\"].+['\"]",               # 3. Natvrdo napsaná hesla
    r"secret[_-]?key\s*=\s*['\"].+['\"]",         # 4. Tajné klíče
    r"passwd\s*=\s*['\"].+['\"]",                 # 5. Alternativa pro heslo
    r"authorization\s*:\s*bearer\s+[a-zA-Z0-9]",  # 6. Autorizační tokeny (Bearer)
    r"mongodb(?:\+srv)?://[^\s]+",                # 7. Databázové připojení MongoDB
    r"postgres(?:ql)?://[^\s]+",                  # 8. Databázové připojení PostgreSQL
    r"mysql://[^\s]+",                            # 9. Databázové připojení MySQL
    r"jwt[_-]?token\s*=\s*['\"].+['\"]",          # 10. JWT Tokeny
    r"aws_[a-z_]+_key\s*=\s*['\"].+['\"]",        # 11. AWS klíče
]

def run_cmd(cmd):
    """Pomocná funkce pro spuštění příkazu v terminálu."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def check_security():
    """Bezpečnostní kontrola neuložených změn před commitem."""
    print("[*] Procházím bezpečnostní kontrolou (Security Check)...")
    
    code, diff, _ = run_cmd("git diff")
    code_stat, untracked, _ = run_cmd("git ls-files --others --exclude-standard")
    
    untracked_content = ""
    if untracked:
        for f in untracked.splitlines():
            # Nechceme kontrolovat samotný deploy.py nebo skryté git soubory
            if f == "deploy.py" or f.startswith(".git"):
                continue
            try:
                with open(f, "r", encoding="utf-8", errors="ignore") as file:
                    untracked_content += file.read() + "\n"
            except Exception:
                pass

    total_check_text = diff + "\n" + untracked_content

    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, total_check_text, re.IGNORECASE):
            print("\n" + "🚨" * 20)
            print(f"[BEZPEČNOSTNÍ CHYBA] Zjištěn únik citlivých dat! (Odpovídající vzor: {pattern})")
            print("Deploy byl z bezpečnostních důvodů ZASTAVEN.")
            print("🚨" * 20 + "\n")
            return False
            
    print("[OK] Bezpečnostní kontrola prošla. Žádné zjevné klíče/hesla nenalezeny.")
    return True

def main():
    print("=" * 60)
    print("🚀 AUTOMATICKÝ DEPLOY NA GITHUB")
    print("=" * 60)

    # Zjištění, zda uživatel chce vypnout bezpečnostní kontrolu
    skip_check = "--no-check" in sys.argv or "--skip-security" in sys.argv
    if skip_check:
        print("[⚠️ VAROVÁNÍ] Bezpečnostní kontrola je pro tento běh VYPNUTA (--no-check).")
        print("-" * 60)

    # 1. Kontrola stavu depozitáře
    code, out, _ = run_cmd("git status --porcelain")
    if not out:
        print("[INFO] Žádné změny k odeslání. Vše je aktuální.")
        return

    print("[*] Detekovány změny v projektu:")
    print(out)
    print("-" * 60)

    # 2. Bezpečnostní kontrola (pokud není vypnutá)
    if not skip_check:
        if not check_security():
            print("\n[TIP] Pokud chceš kontrolu jednorázově přeskočit, spuštění proveď příkazem:")
            print("      python3 deploy.py --no-check\n")
            sys.exit(1)

    # 3. Přidání souborů
    print("[*] Přidávám změny (git add .)...")
    code, _, err = run_cmd("git add .")
    if code != 0:
        print(f"[CHYBA] git add selhal: {err}")
        sys.exit(1)

    # 4. Vytvoření commitu s časovým razítkem
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Update documentation/portfolio ({now})"
    print(f"[*] Vytvářím commit: '{commit_msg}'...")
    
    code, _, err = run_cmd(f'git commit -m "{commit_msg}"')
    if code != 0:
        print(f"[CHYBA] git commit selhal: {err}")
        sys.exit(1)

    # 5. Push na GitHub
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
