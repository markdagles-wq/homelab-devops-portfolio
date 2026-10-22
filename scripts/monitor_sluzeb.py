#!/usr/bin/env python3
import subprocess

ZELENA = "\033[92m"
ZLUTA = "\033[93m"
CERVENA = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


def get_running_processes():
    cmd = ["ps", "-eo", "rss,comm", "--sort=-rss"]
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    processes = {}
    for line in result.stdout.strip().split("\n")[1:]:
        parts = line.strip().split(None, 1)
        if len(parts) == 2:
            try:
                rss_kb = int(parts[0])
                comm = parts[1]
                ram_mb = rss_kb / 1024
                processes[comm] = processes.get(comm, 0) + ram_mb
            except ValueError:
                continue
    return processes


def main():
    print(
        f"\n{BOLD}🔍 Analýza systému, RAM a procesů na ThinkPadu...{RESET}\n"
    )
    print(f"{'NÁZEV PROCESU':<30} | {'CELKOVÁ RAM':<15} | STAV")
    print("-" * 65)

    processes = get_running_processes()
    sumnive_kandidati = []
    celkova_ram_mb = 0

    for proc, ram_mb in processes.items():
        celkova_ram_mb += ram_mb  # Přičteme do celkového součtu

        if ram_mb < 3.0:
            continue

        if ram_mb > 500:
            barva, stav = CERVENA, "⚠️ VYSOKÁ"
        elif ram_mb > 150:
            barva, stav = ZLUTA, "⚡ STŘEDNÍ"
        else:
            barva, stav = ZELENA, "✅ OK"

        print(
            f"{proc:<30} | {barva}{ram_mb:>6.1f} MB{RESET}        | {barva}{stav}{RESET}"
        )

        if proc in ["tumblerd", "tracker-miner-fs", "baloo_file"]:
            sumnive_kandidati.append(proc)

    print("-" * 65)

    # Vyhodnocení celkové spotřeby v uživatelském prostoru
    if celkova_ram_mb > 2000:
        sum_barva = CERVENA
        sum_stav = "⚠️ NAD 2 GB (Pozor na limit!)"
    elif celkova_ram_mb > 1200:
        sum_barva = ZLUTA
        sum_stav = "⚡ STŘEDNÍ ZÁTĚŽ"
    else:
        sum_barva = ZELENA
        sum_stav = "✅ BEZPEČNÁ ZÓNA (Pod 2 GB)"

    print(
        f"\n{BOLD}📊 Celková alokovaná RAM procesů: {sum_barva}{celkova_ram_mb:.1f} MB{RESET} ({sum_stav})"
    )

    if sumnive_kandidati:
        print(
            f"\n{ZLUTA}💡 Nalezeny potenciální zbytečné procesy na pozadí:{RESET}"
        )
        for k in sumnive_kandidati:
            print(f" - {k}")
        volba = (
            input(
                "\nChceš tyto zbytečné procesy dočasně sestřelit? (y/n): "
            )
            .strip()
            .lower()
        )
        if volba == "y":
            for k in sumnive_kandidati:
                subprocess.run(["pkill", "-f", k])
            print(f"{ZELENA}✅ Hotovo, procesy byly ukončeny.{RESET}")


if __name__ == "__main__":
    main()