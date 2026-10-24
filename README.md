# 🛠️ HomeLab, System Administration & Infrastructure Portfolio

**Jméno a Příjmení**  Václav Novotný
📍 **Kontakt:** rewol@post.cz | +420 737 906 400  
🔗 **GitHub:** https://github.com/markdagles-wq/homelab-devops-portfolio

---

### 🎥 Ukázky z terminálu (Silent Engineering Demos)

> *Všechna videa jsou koncipována jako tiché vizuální demonstrace funkčnosti kódu s úvodními titulky.*

#### 1. Architektura & AI Hub Sandbox
[![Project Echo Demo](https://img.youtube.com/vi/ID_VIDEA_1/maxresdefault.jpg)](https://youtu.be/ID_VIDEA_1)
*▶️ Kliknutím přehrajete ukázku spuštění AI Hubu a orchestrace*

---

#### 2. CLI Analýza & Správa procesů: `scripts/monitor_sluzeb.py`
[![Monitor služeb Demo](https://img.youtube.com/vi/ID_VIDEA_2/maxresdefault.jpg)](https://youtu.be/ID_VIDEA_2)
*▶️ Kliknutím přehrajete demonstraci analýzy RAM a interaktivního úklidu*

---

#### 3. Systémová diagnostika: `scripts/ark_sys_health.py`
[![Sys Health Demo](https://img.youtube.com/vi/ID_VIDEA_3/maxresdefault.jpg)](https://youtu.be/ID_VIDEA_3)
*▶️ Kliknutím přehrajete reálnou diagnostiku a health-check systému*

---

### 🔒 Poznámka k repozitáři a soukromí
Zde zveřejněné skripty a struktury slouží jako ukázka  
mého stylu programování, kontejnerizace a automatizace.

Kompletní produkční Ansible role (včetně pokročilého  
LUKS/TPM šifrování disků), systémové konfigurační  
soubory a citlivé bezpečnostní vazby jsou z autorských  
důvodů neveřejné. 

**Rád vám je detailně předvedu a vysvětlím při osobním pohovoru.**

---

### 📂 Struktura tohoto repozitáře a tiché video-ukázky

```text
homelab-devops-portfolio/
├── README.md                          <-- Hlavní dokumentace a portfolio
├── ai_hub/                            <-- AI Sandbox & Podman orchestrace
│   ├── run.py                         <-- Hlavní Python orchestrátor (cleanup, build, porty)
│   └── core/
│       └── engines/
│           ├── __init__.py
│           └── finance_engine.py      <-- Pandas Excel parser a generátor metrik
├── ansible/                           <-- Infrastructure as Code (Ansible)
│   ├── site.yml                       <-- Hlavní orchestrace a přiřazení rolí
│   └── role/
│       └── roles_podman/
│           ├── role_client_containers/
│           │   ├── tasks/
│           │   │   └── main.yml       <-- Úlohy pro klientské kontejnery
│           │   └── templates/
│           │       ├── docker-compose-db.yml.j2
│           │       ├── docker-compose-lemp.yml.j2
│           │       ├── docker-compose-node.yml.j2
│           │       └── docker-compose-python.yml.j2
│           ├── role_control_plane/
│           │   ├── files/
│           │   │   └── control_plane.py <-- Flask dashboard a správa klientů
│           │   └── tasks/
│           │       └── main.yml       <-- Instalace a systemd služba pro control plane
│           └── role_traefik_gateway/
│               └── tasks/
│                   └── main.yml       <-- Nasazení Traefik proxy a sítí
└── scripts/                           <-- Vlastní systémové utility
    ├── monitor_sluzeb.py              <-- CLI analýza RAM, procesů a interaktivní úklid
    └── ark_sys_health.py              <-- Pokročilý systémový health-check & diagnostika
    
🎯 O mně & Moje IT filozofie

Nepocházím z akademického IT prostředí ani nemám roky korporátní praxe.

Vše, co umím, jsem si sám postavil, odlaďoval a vydřel v HomeLabu.

Žádné bezhlavé klikání:

Chci do hloubky rozumět fungování OS,

efektivní alokaci HW zdrojů,

zabezpečení dat na úrovni disků

a kompletní automatizaci.

Architektura nad syntaxí:

AI využívám jako efektivní nástroj pro psaní kódu (rychlé ruce),

ale celkovou architekturu, síťový design

a logiku systému navrhuji a řídím sám.

Minimalismus & Nízká režie:

Preferuji čistý Debian CLI.

Aplikace izoluji do venv a bezrootových kontejnerů.

I na 32 GB RAM šetřím zdroje (Podman místo Dockeru,

podtaktování CPU pro úsporu energie, žádný balast).

Bezpečnost na prvním místě:

Šifrování disků vázané na TPM2 čip,

hardening SSH, izolace sítí a aplikací.

🖥️ 1. Hardware Tuning, Kernel & Bezpečnost

(Debian / HP EliteDesk G4 / ThinkPad)

Hardware & BIOS:

Fyzická údržba (přepastování CPU),

zamykání BIOSu heslem, správná alokace zdrojů.

LUKS + TPM2 Šifrování (Clevis):

Automatické bezpečné odemykání NVMe disků

vázané na TPM2 čip (PCR 7) s konfigurací crypttab

a obnovou initramfs. (Kód předvedu na pohovoru)

Power Management & Limity:

Vlastní systemd služba pro zamykání Intel RAPL Power Limitů,

governor schedutil a zastropování CPU na max 80 % pro úsporu wattů.

RAM & Memory Management:

   Odstranění diskového LVM swapu a přechod na zRAM (zstd 25 %).

   Využití /tmp jako tmpfs přímo v RAM.

   Optimalizace kernelu pro AI zátěž přes 2MB Hugepages

   a tuning vfs_cache_pressure.

I/O Schedulery:

Cílené nastavení schedulerů (deadline pro NVMe, none pro SSD).

🤖 2. Infrastructure as Code & Orchestrace

(Ansible & Podman)

Modularizované role (ansible/role/roles_podman/):

Dynamická distribuce konfigurace podle typu stroje (hosts / facts).

SSH Hardening:

Vypnutí heslového přihlašování, změna portů, správa SSH klíčů.

Automation & Container Management:

Automatické nasazování klientských prostředí přes podman-compose

do adresářové struktury /opt/clients/ s právy (0750 / 0640).

Traefik Gateway & Control Plane:

Automatizované nasazování reversní proxy Traefik

a správa klientských subdomén.

Self-Healing / Log Monitoring:

Vyhodnocování stavu kontejnerů (čtení logů přes tail -n 20)

s automatickým restartem v případě selhání.

🚀 3. Projekt: Finance AI Hub & Podman Sandbox

Prototyp kontejnerizovaného finančního autopilota:

Runtime & Izolace (ai_hub/run.py):

Běží v Podmanu s orchestrací

(cleanup, build, volume mounty).

Data Engine (ai_hub/core/engines/finance_engine.py):

Parsování a čištění dat z Excel výkazů (finance.xlsx)

pomocí pandas, generování JSON metrik a kontextu pro AI.

AI Engine & Guard Architecture:

   Hlavní AI model (Qwen) na portu 8080 pro finanční analýzu.

   Bezpečnostní Guard model (Phi-4) na portu 8081 pro validaci výstupů.

   PHP API Bridge pro komunikaci rozhraní s backendem.

🌐 4. Síťová architektura, Auditing & Zálohy

Síť & Cloud Evolution:

Přechod od Nginx proxy k čisté mesh síti přes Tailscale.

Plánovaný přechod řízení webové prezentace do cloudu přes Terraform.

Emergency Alerting (SMS Bridge):

Python skript pro kritické notifikace.

Propojení Debian serveru s Android/Termux zařízením

přes SSH tunel v Tailscale / ADB fallback pro 100% doručení SMS.

System & Code Audit (ark_audit.py):

Vlastní Python skener pro hloubkovou kontrolu adresářů

a generování manifestů závislostí (pip, apt, systémové binárky).

RAM & Process Monitor (scripts/monitor_sluzeb.py):

CLI nástroj v Pythonu s barevným rozlišením spotřeby RAM podle procesů

a detekcí zbytečných služeb (tumblerd, tracker-miner) s možností ukončení.

🔒 5. Integrita kódu & Supply Chain Security

    Kryptografická verifikace: Pro zajištění maximální transparentnosti a 
    
    integrity kódu využívám vestavěný skript pro generování SHA-256 manifestů. 
    
    Zabraňuje neautorizované modifikaci struktury repozitáře.

        Generování manifestu: python3 hash_generator.py

        Ověření integrity: sha256sum -c manifest.sha256

🔒 Poznámka k soukromí & Kontakt

Zde zveřejněné skripty a struktury slouží jako demonstrace mého stylu programování,

      kontejnerizace a automatizace. Kompletní produkční Ansible role 
 
 a citlivé konfigurace jsou z autorských důvodů neveřejné.

Rád vám kompletní architekturu předvedu a detailně vysvětlím při osobním pohovoru.

✉️ Email: rewol@post.cz

📞 Telefon: +420 737 906 400

🌐 GitHub Profile: markdagles-wq
