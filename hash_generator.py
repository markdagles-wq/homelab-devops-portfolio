#!/usr/bin/env python3
import hashlib
from pathlib import Path

# Nastav složku, kterou chceš zahašovat (tečka = aktuální adresář)
ROOT_DIR = Path(".")
MANIFEST_FILE = Path("manifest.sha256")

# Soubory/složky, které chceš ignorovat (např. git, samotný skript, skryté soubory)
IGNORE_DIRS = {".git", "__pycache__", ".venv"}
IGNORE_FILES = {MANIFEST_FILE.name, "hash_generator.py"}

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Chyba při čtení {file_path}: {e}")
        return None

def main():
    print(f"Generuji SHA-256 manifest pro: {ROOT_DIR.resolve()}\n")
    manifest_lines = []

    # Rekurzivně projdeme složku
    for path in sorted(ROOT_DIR.glob("**/*")):
        # Přeskočíme ignorované adresáře
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        # Zpracujeme jen soubory
        if path.is_file() and path.name not in IGNORE_FILES:
            file_hash = calculate_sha256(path)
            if file_hash:
                # Relativní cesta vůči rootu
                rel_path = path.relative_to(ROOT_DIR)
                line = f"{file_hash}  {rel_path}"
                manifest_lines.append(line)
                print(f"[HASH] {rel_path} -> {file_hash[:16]}...")

# Zápis do manifestu
    MANIFEST_FILE.write_text("\n".join(manifest_lines) + "\n")
    print(f"\nHotovo! Manifest byl úspěšně uložen do: {MANIFEST_FILE.resolve()}")
    print("Ověření je možné provést příkazem: sha256sum -c manifest.sha256")

if __name__ == "__main__":
    main()
