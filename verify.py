#!/usr/bin/env python3
import hashlib
import subprocess
import sys
from pathlib import Path

# Nastavení
MANIFEST_FILE = Path("manifest.sha256")
IGNORE_DIRS = {".git", "__pycache__", ".venv"}
IGNORE_FILES = {MANIFEST_FILE.name, "deploy.py", "verify.py"}

def run_cmd(cmd):
    """Pomocná funkce pro spuštění příkazu v terminálu."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def calculate_sha256(file_path):
    """Spočítá SHA-256 hash konkrétního souboru."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"[CHYBA] Nelze přečíst {file_path}: {e}")
        return None

def main():
    print("=" * 60)
    print("🔍 KONTROLA INTEGRITY & RECOVERY (Verify & Sync)")
    print("=" * 60)

    # 1. Volitelná obnova z GitHubu, pokud uživatel zadal --restore nebo --pull
    if "--restore" in sys.argv or "--pull" in sys.argv:
        print("[*] Vynucuji tvrdou obnovu ze vzdáleného GitHubu (Hard Reset)...")
        # Nejprve stáhneme aktuální data a pak natvrdo resetujeme lokální pracovní kopii
        run_cmd("git fetch origin main")
        code, out, err = run_cmd("git reset --hard origin/main")
        if code == 0:
            print("[OK] Lokální adresář byl natvrdo synchronizován a obnoven z GitHubu.")
            print("-" * 60)
        else:
            print(f"[CHYBA] Obnova selhala: {err}")
            sys.exit(1)

    # 2. Kontrola existence manifestu
    if not MANIFEST_FILE.exists():
        print(f"[CHYBA] Soubor {MANIFEST_FILE} nebyl v adresáři nalezen!")
        print("[TIP] Spusť nejprve 'python3 deploy.py' pro vygenerování manifestu.")
        sys.exit(1)

    # Načtení očekávaných hashů z manifestu
    expected_manifest = {}
    for line in MANIFEST_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            file_hash, file_path = parts
            expected_manifest[file_path.strip()] = file_hash.strip()

    root_dir = Path(".")
    errors = 0
    checked = 0

    print("[*] Porovnávám lokální soubory s manifestem...\n")

    current_files = set()
    for path in sorted(root_dir.glob("**/*")):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.is_file() and path.name not in IGNORE_FILES:
            rel_path = str(path.relative_to(root_dir))
            current_files.add(rel_path)
            checked += 1

            if rel_path in expected_manifest:
                current_hash = calculate_sha256(path)
                if current_hash == expected_manifest[rel_path]:
                    print(f"  [OK] {rel_path}")
                else:
                    print(f"  ❌ [ZMĚNA] {rel_path} (Hash nesouhlasí!)")
                    errors += 1
            else:
                print(f"  ⚠️ [NAVÍC] {rel_path} (Není v manifestu)")

    # Kontrola chybějících souborů
    missing_files = set(expected_manifest.keys()) - current_files
    for mf in missing_files:
        print(f"  🚨 [CHYBÍ] {mf} (Soubor v adresáři chybí!)")
        errors += 1

    print("=" * 60)
    if errors == 0:
        print(f"✅ INTEGRITA JE V POŘÁDKU! Zkontrolováno {checked} souborů, vše sedí.")
    else:
        print(f"❌ NALEZENY PROBLÉMY: Počet nesrovnalostí: {errors}")
        print("\n[TIP] Pokud chceš poškozené či smazané soubory automaticky obnovit z GitHubu, spuštěj:")
        print("      python3 verify.py --restore")
    print("=" * 60)

if __name__ == "__main__":
    main()
