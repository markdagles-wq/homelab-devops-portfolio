# ⚙️ HomeLab, System Administration & Infrastructure Portfolio

**Václav Novotný** | ✉️ rewol@post.cz | 📞 +420 737 906 400 | 🔗 [GitHub Profile](https://github.com/markdagles-wq)

---

### 🛰️ Očekávané novinky & Stav vývoje
> *Tento repozitář je živý organismus. Pravidelně sem doplňuji nové moduly, skripty a ukázky z reálného provozu mých Debian serverů.*

* **Aktuální verze:** Stabilní jádro kontejnerové orchestrace a bezpečnostních bran.
* **Dlouhodobě rozšiřuji:** Ansible role o automatický backup management a integraci s novým monitoring dashboardem. *(Sledujte commity!)*

---

### 🎥 Živé video-ukázky z terminálu (Silent Demos)

<details>
<summary><b> 🟢 Nejnovější přidaná ukázka: ARK Enterprise Cockpit & Hardware Orchestration (Klikni pro rozbalení)</b></summary>

[![ARK TUI Demo](https://img.youtube.com/vi/SEM_ID_ZDE_DOPLN_VY_NEBO_ZATIM_PLACEHOLDER/mqdefault.jpg)](https://youtu.be/eF7yAbskCuc)
- *Živá ukázka TUI kokpitu pro správu RAPL limitů, Lenovo ACPI baterie (80%), NVIDIA telemetrie a GreenOps úspor.*

</details>

<details>
<summary><b>🖥️ Starší / Základní video-ukázky (Klikni pro rozbalení)</b></summary>

* **CLI Analýza RAM (`scripts/monitor_sluzeb.py`):**
  [![Monitor služeb Demo](https://img.youtube.com/vi/V-Lv1OOfGRc/mqdefault.jpg)](https://youtu.be/V-Lv1OOfGRc)
* **Systémová diagnostika (`scripts/ark_sys_health.py`):**
  [![Sys Health Demo](https://img.youtube.com/vi/_V8-E2RFi0w/mqdefault.jpg)](https://youtu.be/_V8-E2RFi0w)
</details>

---

### 🧬 Architektura v kostce (Struktura projektu)

<details>
<summary><b>🗃️ Zobrazit stromovou strukturu repozitáře (Klikni pro rozbalení)</b></summary>

```text
homelab-devops-portfolio/
├── README.md              <-- Dokumentace a portfolio
├── deploy.py              <-- Auto-deploy s bezpečnostní bránou a generátorem hashů
├── verify.py              <-- Skript pro ověření kryptografické integrity podle manifestu
├── manifest.sha256        <-- Automatický kryptografický manifest integrity
├── ai_hub/                <-- Podman orchestrace & AI Sandbox (Qwen + Phi-4 Guard)
├── ansible/               <-- IaC: Site.yml a modulární role (Podman, Traefik, Control Plane)
└── scripts/               <-- Systemd/CLI utility (monitor_sluzeb.py, ark_sys_health.py)

###  📂  Inženýrský přístup & Klíčové pilíře

* 🔒 **Security & Supply Chain:** Vlastní `deploy.py` (sken citlivých dat před pushem) 
      + automatický `manifest.sha256` pro ověření integrity.

* 🔋 **Performance & Kernel Tuning:** zRAM (zstd 25 %), RAM optimization a TPM2 
      + LUKS odemykání disků na Debian CLI.

* ⚡ **IaC & Orchestrace:** Modularizované Ansible role, bezrootový Podman (`/opt/clients/`) 
      + reverzní proxy Traefik.

🛠️ Kompletní technická specifikace & detaily konfigurace

#### Hardware, Kernel & Bezpečnost
* **Hardware Tuning:** Běží na HP EliteDesk G4 / ThinkPad, fyzický tuning a BIOS hardening.
* **LUKS + TPM2 (Clevis):** Automatické bezpečné odemykání NVMe disků vázané na TPM2 (PCR 7).
* **Power Management:** Systemd služba pro řízení Intel RAPL Power Limitů a úsporu wattů.
* **RAM Optimization:** Přechod z diskového swapu na zRAM (zstd 25 %), využití tmpfs pro `/tmp`.

#### Infrastructure as Code & Orchestrace
* **Ansible Role:** Modularizovaná struktura pro bezpečný deployment (`site.yml`).
* **SSH Hardening:** Vypnutí hesel, změna portů, správa SSH klíčů.
* **Podman Compose:** Izolované klientské kontejnery v `/opt/clients/` s právy (0750).
* **Traefik Gateway:** Automatizovaná reverzní proxy a správa klientských subdomén.

#### Integrity & Deploy Automation
* **`deploy.py`:** Python utilita pro skenování diffu a zamezení úniku klíčů/hesel.
* **Integrity Manifest:** SHA-256 hashovací brána garantující neporušenost souborů při přenosu.


🚀 Budoucí směr & Enterprise Rozšíření (Vrchol ledovce)

    Tento veřejný repozitář slouží jako čistá ukázka mého přístupu, psaní udržitelného kódu a 
    důrazu na bezpečnost (IaC, Podman, LUKS/TPM2). V produkčním prostředí a širším měřítku však 
    stavím a spravuji komplexní distribuované systémy:

    ☁️ Cloud & Hybridní Architektura: Propojení lokálních serverů s cloudovým prostředím pro 
       škálovatelné webové aplikace, efektivní load balancing a pokročilou správu infrastruktury.

    🔒 Zero-Trust & Tailscale Mesh: Budování pokročilých síťových topologií pomocí Tailscale 
       tunelů pro šifrovanou, bezpečnou a izolovanou komunikaci mezi uzly bez nutnosti otevírat 
       porty do veřejného internetu.

    🚢 GitOps & CI/CD (Argo CD / GitHub): Nasazení moderních GitOps praktik – automatizované 
       synchronizace stavu infrastruktury, verzování konfigurací a zero-downtime deploymentů pomocí 
       nástrojů jako Argo CD a GitHub Actions.

    ☸️ Kubernetes / K3s Orchestrace: Přechod od kontejnerizovaných služeb k plnohodnotné 
       orchestraci clusterů pomocí K3s pro vysokou dostupnost (HA), auto-healing a škálování
       klientských aplikací.

    🗄️ Databázové Architektury & Resilientní Backup: Návrh robustních databázových vrstev, 
       automatizované replikace, šifrovaných off-site záloh a strategií pro okamžitou obnovu.

---

### 🔒 Poznámka & Kontakt

>  *Kompletní produkční role a citlivé konfigurace jsou z bezpečnostních důvodů neveřejné.*

> *Rád vám celou architekturu detailně představím a vysvětlím při osobním pohovoru.*

* ✉️ **Email:** rewol@post.cz
* 📞 **Telefon:** +420 737 906 400
* 🔗 **GitHub:** [markdagles-wq](https://github.com/markdagles-wq)
