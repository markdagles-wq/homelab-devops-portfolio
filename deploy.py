#!/usr/bin/env python3
import subprocess
import sys
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path

# Seznam cca 10+ vzorů pro detekci citlivých dat a parametrů
SENSITIVE_PATTERNS = [
    r"BEGIN\s+PRIVATE\s+KEY",                     # 1. SSH / TLS Privátní klíče
    r"api[_-]?key\s*=\s*['\"].+['\"]",             # 2. API klíče
    r"password\s*=\s*['\"].+['\"]",                # 3. Natvrdo napsaná hesla
    r"secret[_-]?key\s*=\s*['\"].+['\"]",          # 4. Tajné klíče
    r"passwd\s*=\s*['\"].+['\"]",                  # 5. Alternativa pro heslo
    r"authorization\s*:\s*bearer\s+[a-zA-Z0-9]",   # 6. Autorizační tokeny (Bearer)
    r"mongodb(?:\+srv)?://[^\s]+",                 # 7. Databázové připojení MongoDB
    r"postgres(?:ql)?://[^\s]+",                   # 8. Databázové připojení PostgreSQL
    r"mysql://[^\s]+",                             # 9. Databázové připojení MySQL
    r"jwt[_-]?token\s*=\s*['\"].+['\"]",           # 10. JWT Tokeny
    r"aws_[a-z_]+_key\s*=\s*['\"].+['\"]",         # 11. AWS klíče
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
            # Nechceme kontrolovat konfigurační a správcovské soubory
            if f in ["deploy.py", "verify.py", "videos.json", "manifest.sha256"] or f.startswith(".git"):
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

def update_readme_videos():
    """Automaticky přečte videos.json, seskupí je podle kategorií a přepíše sekci v README.md."""
    print("[*] Aktualizuji sekci videí v README.md podle kategorií z videos.json...")
    json_path = Path("videos.json")
    readme_path = Path("README.md")

    if not json_path.exists() or not readme_path.exists():
        print("[INFO] Soubor videos.json nebo README.md nenalezen, přeskakuji auto-generování videí.")
        return

    try:
        videos = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[CHYBA] Nelze parsovat videos.json: {e}")
        return

    # Seskupení videí podle kategorií se zachováním pořadí
    categories = {}
    for v in videos:
        cat = v.get("category", "Ostatní")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(v)

    # Sestavení přehledného HTML bloku pro README
    html_lines = []
    for cat, cat_videos in categories.items():
        html_lines.append(f"<details>")
        html_lines.append(f"<summary><b>📂 {cat} ({len(cat_videos)} ukázek) - Klikni pro rozbalení</b></summary>\n")
        
        for v in cat_videos:
            vid_id = v.get("id")
            title = v.get("title", "Video ukázka")
            html_lines.append(f"* **{title}**")
            html_lines.append(f"  * [![Miniatura](https://img.youtube.com/vi/{vid_id}/mqdefault.jpg)](https://youtu.be/{vid_id})")
            html_lines.append(f"  * *[▶️ Sledovat video na YouTube](https://youtu.be/{vid_id})*\n")
            
        html_lines.append(f"</details>\n")

    generated_content = "\n".join(html_lines)

    # Vložení do README.md mezi značky
    readme_content = readme_path.read_text(encoding="utf-8")
    start_tag = "<!-- VIDEOS_START -->"
    end_tag = "<!-- VIDEOS_END -->"

    if start_tag in readme_content and end_tag in readme_content:
        parts = readme_content.split(start_tag)
        after_start = parts[1].split(end_tag)[1]
        new_readme = parts[0] + start_tag + "\n\n" + generated_content + "\n" + end_tag + after_start
        readme_path.write_text(new_readme, encoding="utf-8")
        print("[OK] README.md bylo úspěšně aktualizováno o nejnovější roztříděná videa.")
    else:
        print("[VAROVÁNÍ] Značky pro videa v README.md nebyly nalezeny.")

def generate_hash_manifest():
    """Automaticky vygeneruje/aktualizuje SHA-256 manifest všech souborů před deployem."""
    print("[*] Generuji aktuální SHA-256 manifest projektových souborů...")
    root_dir = Path(".")
    manifest_file = Path("manifest.sha256")
    
    ignore_dirs = {".git", "__pycache__", ".venv"}
    ignore_files = {manifest_file.name, "deploy.py", "verify.py", "videos.json"}

    manifest_lines = []
    
    for path in sorted(root_dir.glob("**/*")):
        # Přeskočíme ignorované adresáře
        if any(part in ignore_dirs for part in path.parts):
            continue
        # Zpracujeme jen soubory
        if path.is_file() and path.name not in ignore_files:
            try:
                sha256_hash = hashlib.sha256()
                with open(path, "rb") as f:
                    for byte_block in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(byte_block)
                rel_path = path.relative_to(root_dir)
                manifest_lines.append(f"{sha256_hash.hexdigest()}  {rel_path}")
            except Exception as e:
                print(f"[VAROVÁNÍ] Nelze zahašovat {path}: {e}")

    # Zápis do manifestu
    manifest_file.write_text("\n".join(manifest_lines) + "\n")
    print(f"[OK] Manifest úspěšně aktualizován: {manifest_file.resolve()}")

def main():
    print("=" * 60)
    print("🚀 AUTOMATICKÝ DEPLOY, VIDEO SYNC & INTEGRITY MGR")
    print("=" * 60)

    # Zjištění, zda uživatel chce vypnout bezpečnostní kontrolu
    skip_check = "--no-check" in sys.argv or "--skip-security" in sys.argv
    if skip_check:
        print("[⚠️ VAROVÁNÍ] Bezpečnostní kontrola je pro tento běh VYPNUTA (--no-check).")
        print("-" * 60)

    # 1. Bezpečnostní kontrola (pokud není vypnutá)
    if not skip_check:
        if not check_security():
            print("\n[TIP] Pokud chceš kontrolu jednorázově přeskočit, spuštění proveď příkazem:")
            print("      python3 deploy.py --no-check\n")
            sys.exit(1)

    # 2. Automatická aktualizace sekce videí v README.md z videos.json
    update_readme_videos()
    print("-" * 60)

    # 3. Automatické generování SHA-256 hash manifestu (zahrnuje i změněné README)
    generate_hash_manifest()
    print("-" * 60)

    # 4. Kontrola stavu depozitáře
    code, out, _ = run_cmd("git status --porcelain")
    if not out:
        print("[INFO] Žádné nové změny k odeslání. Vše je aktuální.")
        return

    print("[*] Detekovány změny v projektu:")
    print(out)
    print("-" * 60)

    # 5. Přidání souborů (včetně videos.json, README.md a nového manifestu)
    print("[*] Přidávám změny (git add .)...")
    code, _, err = run_cmd("git add .")
    if code != 0:
        print(f"[CHYBA] git add selhal: {err}")
        sys.exit(1)

    # 6. Vytvoření commitu s časovým razítkem
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Auto-deploy: Update portfolio, videos & integrity manifest ({now})"
    print(f"[*] Vytvářím commit: '{commit_msg}'...")
    
    code, _, err = run_cmd(f'git commit -m "{commit_msg}"')
    if code != 0 and "nothing to commit" not in err:
        print(f"[CHYBA] git commit selhal: {err}")
        sys.exit(1)

    # 7. Push na GitHub
    print("[*] Odesílám na GitHub (git push)...")
    code, out, err = run_cmd("git push origin main")
    
    if code == 0:
        print("=" * 60)
        print("✅ ÚSPĚŠNĚ ULOŽENO, ZAHASOVÁNO A PUBLIKOVÁNO NA GITHUB!")
        print("=" * 60)
    else:
        print(f"[CHYBA] Push selhal: {err}")
        print("[TIP] Pokud to chce heslo/token, pusť skript ručně nebo nastav 'git config --global credential.helper store'")

if __name__ == "__main__":
    main()
