# 🛠️ HomeLab, System Administration & Infrastructure Portfolio
**Jméno a Příjmení**  
📍 *Kontakt:* rewol@post.cz | +420 737 906 400 | GitHub: [https://github.com/markdagles-wq/homelab-devops-portfolio]

> 🔒 **Poznámka k repozitáři a soukromí:**  
> Zde zveřejněné skripty a struktury slouží jako ukázka mého stylu programování, kontejnerizace a automatizace. Kompletní produkční Ansible role (včetně pokročilého LUKS/TPM šifrování disků), systémové konfigurační soubory a citlivé bezpečnostní vazby jsou z autorských důvodů neveřejné. **Rád vám je detailně předvedu a vysvětlím při osobním pohovoru.**

---

## 📂 Struktura tohoto repozitáře
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
    └── monitor_sluzeb.py              <-- CLI analýza RAM, procesů a interaktivní úklid

## 🎯 O mně & Moje IT filozofie

Nepocházím z akademického IT prostředí ani nemám roky korporátní praxe – **vše, co umím, jsem si sám postavil, odlaďoval a vydřel v praxi v rámci svého HomeLabu**. 

Nechci být administrátor, který věci jen bezhlavě „kliká“ v rozhraní. Chci do hloubky rozumět tomu, jak funguje operační systém, jak efektivně nakládat s hardwarovými zdroji, jak zabezpečit data na úrovni disků a jak celou infrastrukturu automatizovat.

* **Architektura nad syntaxí:** Pro psaní kódu a skriptů efektivně využívám AI jako nástroj (rychlé ruce), ale celkovou architekturu, bezpečnostní vazby, síťový design a logiku systému navrhuji a řídím sám.
* **Minimalismus & Režie:** Preferuji čistý Debian CLI. Do základního OS instaluji jen nezbytné minimum. Aplikace izoluji do `venv` a bezrootových kontejnerů. I na 32 GB RAM strojích šetřím zdroje (Podman místo Dockeru, XFCE/CLI místo smyček náročných GUI rozhraní, podtaktování CPU pro úsporu energie).
* **Bezpečnost na prvním místě:** Šifrování disků vázané na TPM2 čip, hardening SSH, izolace sítí a aplikací.

---

## 🖥️ 1. Hardware Tuning, Kernel & Bezpečnost (Debian & HP EliteDesk G4 / ThinkPad)

Správu začínám doslova „od podlahy“ u fyzického hardwaru:

* **Hardware & BIOS:** Fyzická údržba (přepastování CPU), zamykání BIOSu heslem, správná alokace zdrojů.
* **LUKS + TPM2 Šifrování (Clevis):** Automatické bezpečné odemykání šifrovaných NVMe disků vázané na TPM2 čip (PCR 7) s automatickou konfigurací `crypttab` a obnovou `initramfs`.
* **Power Management & Limity:** Vlastní systemd služba pro trvalé zamykání **Intel RAPL Power Limitů**, dynamický governor `schedutil` a zastropování CPU (např. max 80 % pro plynulý běh a úsporu wattů).
* **RAM & Memory Management:**
  * Kompletní odstranění diskového LVM swapu a přechod na **zRAM** (zstd komprese na 25 % RAM).
  * Využití `/tmp` jako `tmpfs` přímo v paměti RAM.
  * Optimalizace kernelu pro AI zátěž pomocí **2MB Hugepages** a ladění `vfs_cache_pressure`.
* **I/O Schedulery:** Cílené nastavení schedulerů (`deadline` pro NVMe, `none` pro SSD).

---

## 🤖 2. Infrastructure as Code & Orchestrace (Ansible)

Půl roku jsem odlaďoval univerzální **Ansible Playbooky**, které deklarativně řídí mé stanice i servery bez chyb:

* **Modularizované role:** Dynamická distribuce konfigurace podle typu stroje (`hosts` / `facts`).
* **SSH Hardening:** Vypnutí heslového přihlašování, změna portů, automatická distribuce SSH klíčů.
* **Automation & Container Management:** Automatické nasazování klientských prostředí přes `podman-compose` šablony do adresářové struktury `/opt/clients/` se správně nastavenými přístupovými právy (`0750` / `0640`).
* **Self-Healing / Log Monitoring:** Vyhodnocování stavu kontejnerů (čtení `tail -n 20` logů) s automatickým restartem v případě selhání.

---

## 🚀 3. Projekt: Finance AI Hub & Podman Sandbox

Funkční prototyp kontejnerizovaného finančního autopilota, na kterém si zkouším pokročilé aplikační řetězce:

* **Runtime & Izolace:** Běží v **Podmanu** s využitím `run.py` orchestrovacího skriptu (automatický cleanup, build, uchování persistentních dat přes volume mounty).
* **Data Engine (Python / Pandas):** Automatizované parsování a čištění dat z Excel výkazů (`finance.xlsx`), generování JSON metrik a kontextu pro AI.
* **AI Engine & Guard Architecture:**
  * Hlavní AI model (Qwen) na portu `8080` pro finanční analýzu.
  * Bezpečnostní „Guard“ model (Phi-4) na portu `8081` provádějící validaci výstupů.
  * PHP API Bridge pro komunikaci mezi uživatelským rozhraním a backendem.

---

## 🌐 4. Síťová architektura, Auditing & Záložní systémy

* **Síť & Cloud Evolution:** 
  * Přechod od lokálního Nginx proxy k čisté mesh síti přes **Tailscale**.
  * Plánovaný přechod řízení webové prezentace do cloudu pomocí **Terraformu** (dosažení nízké latence, zálohy a nezávislé IP).
* **Emergency Alerting (SMS Bridge):** Skript v Pythonu pro kritické notifikace. Propojení Debian serveru s Android/Termux zařízením přes **SSH tunel v Tailscale** nebo ADB Broadcast fallback pro 100% doručení SMS.
* **System & Code Audit (`ark_audit.py`):** Vlastní Python skener pro hloubkovou kontrolu adresářů, parsování víceřádkových `apt-get` zápisů v kontejnerech a generování závislostních manifestů (`pip`, `apt`, systémové binárky).
* **Custom RAM & Process Monitor:** Vlastní CLI nástroj v Pythonu s barevným rozlišením spotřeby RAM podle procesů, detekcí zbytečných služeb (`tumblerd`, `tracker-miner`) a možností jejich okamžitého ukončení.

---

## 💡 Proč reaguji na tuto pozici?

Vaše nabídka mě zaujala pestrou kombinací technologií (Linux, Windows, MikroTik, Virtualizace, Open-source systémy). Hledám prostředí, kde mohu okamžitě pomáhat kolegovským požadavkům na IT supportu a zároveň postupně přebírat složitější úkoly v oblasti správy serverů, sítí a automatizace.

Nabízím vysoké pracovně-technické nasazení, neustálou chuť se učit a schopnost dotahovat věci do funkčního konce.
