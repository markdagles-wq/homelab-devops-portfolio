#!/usr/bin/env python3
import os
import subprocess

IMAGE_NAME = "finance_ai_hub_img"
CONTAINER_NAME = "finance_ai_hub_container"
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_cmd(cmd):
    print(f"[CMD] {cmd}")
    return subprocess.run(cmd, shell=True)

def cleanup():
    print("\n[*] Uklízím kontejner...")
    subprocess.run(f"podman rm -f {CONTAINER_NAME}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    print("=" * 60)
    print("    FINANČNÍ AUTOPILOT & AI HUB (PODMAN)      ")
    print("=" * 60)
    
    os.chdir(PROJECT_DIR)
    
    try:
        # 0. Automatický úklid před buildem
        print("[*] Provádím úklid staré build cache a kontejnerů...")
        run_cmd(f"podman rm -f {CONTAINER_NAME} >/dev/null 2>&1")
        run_cmd("podman builder prune -f >/dev/null 2>&1")

        # 1. Sestavení kontejneru
        print("[*] Sestavuji Podman obraz...")
        build_res = run_cmd(f"podman build --tag {IMAGE_NAME} .")
        if build_res.returncode != 0:
            print("[!] Chyba při sestavování kontejneru.")
            return

        # 2. Kontrola Excelu na hostiteli
        excel_path = os.path.join(PROJECT_DIR, "finance.xlsx")
        if os.path.exists(excel_path):
            print(f"[*] Detekován Excel na hostiteli: {excel_path}")
        else:
            print("[!] VAROVÁNÍ: finance.xlsx nebyl v kořenu projektu nalezen!")

        # 3. Spuštění kontejneru s celou složkou (Excel živě + AI servery stabilní v /opt)
        print("[*] Spouštím kontejner...")
        print("[*] Webové rozhraní (PHP UI):    http://localhost:8000")
        print("[*] Hlavní AI Server (Qwen):    http://localhost:8080")
        print("[*] Bezpečnostní Guard (Phi-4): http://localhost:8081")
        print("[*] Pro ukončení stiskni Ctrl+C\n")
        
        run_cmd(
            f"podman run --rm --name {CONTAINER_NAME} "
            f"-p 8000:8000 -p 8080:8080 -p 8081:8081 "
            f"-v {PROJECT_DIR}:/app:z "
            f"{IMAGE_NAME}"
        )
        
    except KeyboardInterrupt:
        cleanup()
    finally:
        cleanup()

if __name__ == "__main__":
    main()
