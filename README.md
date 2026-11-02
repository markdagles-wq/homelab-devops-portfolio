# 🛠️ HomeLab, System Administration & Infrastructure Portfolio

**Václav Novotný** | ✉️ rewol@post.cz | 📞 +420 737 906 400 | 🔗 [GitHub Profile](https://github.com/markdagles-wq)

---

### 🚀 Očekávané novinky & Stav vývoje
> *Tento repozitář je živý organismus. Pravidelně sem doplňuji nové moduly, skripty a ukázky z reálného provozu mých Debian serverů.*

- **Aktuální verze:** Stabilní jádro kontejnerové orchestrace a bezpečnostních bran.
- **Připravuji v nejbližších dnech:** Rozšíření Ansible rolí o automatický backup management a integraci s novým monitoring dashboardem. *(Sledujte commity!)*

---

### 📂 Architektura v kostce (Struktura projektu)

<details>
<summary><b>🗂️ Zobrazit stromovou strukturu repozitáře (Klikni pro rozbalení)</b></summary>

```text
homelab-devops-portfolio/
├── README.md              <-- Dokumentace a portfolio
├── deploy.py              <-- Auto-deploy s bezpečnostní bránou a generátorem hashů
├── verify.py              <-- Nástroj pro ověření integrity a tvrdou obnovu (--restore)
├── manifest.sha256        <-- Automatický kryptografický manifest integrity
├── videos.json            <-- Živá databáze videoukázek pro auto-generování
├── ai_hub/                <-- Podman orchestrace & AI Sandbox (Qwen + Phi-4 Guard)
├── ansible/               <-- IaC: Site.yml a modulární role (Podman, Traefik, Control Plane)
└── scripts/               <-- Systemd/CLI utility (monitor_sluzeb.py, ark_sys_health.py)

---

### 🎥 Živé video-ukázky z terminálu (Auto-updated Portfolio)

<!-- VIDEOS_START -->

<details>
<summary><b>📂 Python Skripty (2 ukázek) - Klikni pro rozbalení</b></summary>

* **CLI Analýza RAM (scripts/monitor_sluzeb.py)**
  * [![Miniatura](https://img.youtube.com/vi/V-Lv1OOfGRc/mqdefault.jpg)](https://youtu.be/V-Lv1OOfGRc)
  * *[▶️ Sledovat video na YouTube](https://youtu.be/V-Lv1OOfGRc)*

* **Systémová diagnostika (scripts/ark_sys_health.py)**
  * [![Miniatura](https://img.youtube.com/vi/_V8-E2RFi0w/mqdefault.jpg)](https://youtu.be/_V8-E2RFi0w)
  * *[▶️ Sledovat video na YouTube](https://youtu.be/_V8-E2RFi0w)*

</details>

<details>
<summary><b>📂 Ansible Role (1 ukázek) - Klikni pro rozbalení</b></summary>

* **Modularizované Ansible role pro Podman kontejnerizaci**
  * [![Miniatura](https://img.youtube.com/vi/SEM_DAL_ID_ANSIBLE/mqdefault.jpg)](https://youtu.be/SEM_DAL_ID_ANSIBLE)
  * *[▶️ Sledovat video na YouTube](https://youtu.be/SEM_DAL_ID_ANSIBLE)*

</details>

<details>
<summary><b>📂 PHP Kód (3 ukázek) - Klikni pro rozbalení</b></summary>

* **Control Plane Dashboard & Správa klientů**
  * [![Miniatura](https://img.youtube.com/vi/SEM_DAL_ID_PHP_1/mqdefault.jpg)](https://youtu.be/SEM_DAL_ID_PHP_1)
  * *[▶️ Sledovat video na YouTube](https://youtu.be/SEM_DAL_ID_PHP_1)*

* **API Bridge pro komunikaci backendu a lokálního AI**
  * [![Miniatura](https://img.youtube.com/vi/SEM_DAL_ID_PHP_2/mqdefault.jpg)](https://youtu.be/SEM_DAL_ID_PHP_2)
  * *[▶️ Sledovat video na YouTube](https://youtu.be/SEM_DAL_ID_PHP_2)*

* **Bezpečnostní notifikace a monitoring rozhraní**
  * [![Miniatura](https://img.youtube.com/vi/SEM_DAL_ID_PHP_3/mqdefault.jpg)](https://youtu.be/SEM_DAL_ID_PHP_3)
  * *[▶️ Sledovat video na YouTube](https://youtu.be/SEM_DAL_ID_PHP_3)*

</details>

<!-- VIDEOS_END -->

---

💡 Inženýrský přístup & Klíčové pilíře

    🔒 Security & Supply Chain: Vlastní deploy.py (sken citlivých dat před pushem) + automatický 
    
    manifest.sha256 pro ověření integrity.

    ⚡ Performance & Kernel Tuning: zRAM (zstd 25 %), RAM optimization a TPM2 + LUKS odemykání 
    
    disků na Debian CLI.

    📦 IaC & Orchestrace: Modularizované Ansible role, bezrootový Podman (/opt/clients/) a 
    
    reverzní proxy Traefik.

Hardware, Kernel & Bezpečnost

    Hardware Tuning: Běží na HP EliteDesk G4 / ThinkPad, fyzický tuning a BIOS hardening.

    LUKS + TPM2 (Clevis): Automatické bezpečné odemykání NVMe disků vázané na TPM2 (PCR 7).

    Power Management: Systemd služba pro řízení Intel RAPL Power Limitů a úsporu wattů.

    RAM Optimization: Přechod z diskového swapu na zRAM (zstd 25 %), využití tmpfs pro /tmp.

Infrastructure as Code & Orchestrace

    Ansible Role: Modularizovaná struktura pro bezpečný deployment (site.yml).

    SSH Hardening: Vypnutí hesel, změna portů, správa SSH klíčů.

    Podman Compose: Izolované klientské kontejnery v /opt/clients/ s právy (0750).

    Traefik Gateway: Automatizovaná reverzní proxy a správa klientských subdomén.

Integrity & Deploy Automation

    deploy.py: Python utilita pro skenování diffu a zamezení úniku klíčů/hesel.

    Integrity Manifest: SHA-256 hashovací brána garantující neporušenost souborů při přenosu.

🔒 Poznámka & Kontakt

    Zveřejněné skripty slouží jako demonstrace mého stylu práce, kontejnerizace a automatizace.
    
    Kompletní produkční role a citlivé konfigurace jsou z bezpečnostních důvodů neveřejné. 
    
    Rád vám celou architekturu detailně představím a vysvětlím při osobním pohovoru.

    ✉️ Email: rewol@post.cz

    📞 Telefon: +420 737 906 400

    🔗 GitHub: markdagles-wq
