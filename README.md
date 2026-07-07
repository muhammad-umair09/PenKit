# PenKit — Professional Ethical Hacking & Penetration Testing Toolkit

```text
==========================================================================
 ██████╗ ███████╗███╗   ██╗██╗  ██╗██╗████████╗
 ██╔══██╗██╔════╝████╗  ██║██║ ██╔╝██║╚══██╔══╝
 ██████╔╝█████╗  ██╔██╗ ██║█████╔╝ ██║   ██║   
 ██╔═══╝ ██╔══╝  ██║╚██╗██║██╔═██╗ ██║   ██║   
 ██║     ███████╗██║ ╚████║██║  ██╗██║   ██║   
 ╚═╝     ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝   ╚═╝   
      Professional Ethical Hacking & Penetration Testing Toolkit
==========================================================================

```

PenKit is a modular, high-performance, and production-ready command-line framework engineered for network discovery, reconnaissance, informational gathering, and basic structural security auditing. Built with Python 3.12+, PenKit delivers a clean, asynchronous, and robust toolset wrapped inside an interactive, beautifully formatted terminal user interface (TUI).

This project follows clean code conventions, structured error validation, strict separation of concerns, and native reporting engines, making it a professional open-source contribution and portfolio showcase.

> ⚠️ **DISCLAIMER:** This toolkit is designed and authorized exclusively for educational labs, Capture The Flag (CTF) competitions, authorized cybersecurity assessments, and defensive infrastructure auditing. Running unauthorized active network validation scanning against systems without explicit prior written consent is illegal. The author and maintainers assume no liability for misuse.

---

## 📌 Features

### 📡 Network & Target Discovery

* **Host Discovery:** Native ICMP Echo request validation engine paired with rapid TCP/80 connect-based fallback logic.
* **Asynchronous Port Scanner:** Fully multi-threaded TCP connection scanning engine equipped with adjustable worker boundaries, timeouts, and custom-defined port-range processing.
* **Banner Grabber:** Volatile protocol interaction checks designed to extract application server identity markings cleanly.

### 🌐 DNS & Infrastructure Mapping

* **Comprehensive DNS Interrogation:** Fast resolution array fetching `A`, `AAAA`, `MX`, `TXT`, `NS`, and `CNAME` records via structured query routing.
* **WHOIS Mapping:** Automated queries parsing registration entities, administrative regions, nameservers, and expiration metrics.
* **Subdomain Enumeration:** Dictionary-driven parallel enumeration mechanics matching active workspace zones with high-frequency prefix tables.

### 🔒 Web Application Security Verification

* **Header Structural Diagnostics:** Parses target responses to analyze `Server`, `X-Powered-By`, cookie behaviors, and cache structures.
* **Security Hardening Assessment:** Evaluates defensive posture components including `HSTS`, `CSP`, `X-Frame-Options`, `Referrer-Policy`, and `X-Content-Type-Options`.
* **Deployment Fingerprinting:** Automated parsing of `robots.txt` paths coupled with quick multi-threaded active directories discovery checks.

### 🧮 Utility Processing Pipelines

* **Cryptographic Digests Tool:** Computes structural math summaries generating `MD5`, `SHA1`, `SHA-256`, and `SHA-512` hashes concurrently.
* **Base64 Transformer Engine:** Standardized conversion and extraction pipelines for encoding and decoding base64 character blocks safely.

### 📊 Professional Report Engine

* Multi-format export pipeline generating human-readable and programmatically structured output documents (`TXT`, `JSON`, `CSV`, `HTML`, `PDF`).

---

## 📸 Screenshots

### Main Interface Menu

```text
┌─────────────────────────────────────────────┐
│      PENKIT OPERATIONAL COMMAND SYSTEM      │
├─────────────────────────────────────────────┤
│ 1. Host Discovery                           │
│ 2. Port Scanner                             │
│ 3. Banner Grabber                           │
...
└─────────────────────────────────────────────┘

```

*(Placeholder: Add your customized main menu and execution terminal output screenshot here)*

---

## 🎥 Demo

Watch PenKit in action executing multi-threaded port scans and compiling dynamic PDF metrics reports:

* [PenKit Walkthrough Demonstration Placeholder Link](https://www.google.com/search?q=%23)

---

## 🏗️ Architecture

PenKit implements a highly organized, decoupled architecture dividing runtime validation, module mechanics, configuration loading, reporting, and interface presentation layout logic.

```text
                      [ main.py Entrypoint ]
                                │
         ┌──────────────────────┼──────────────────────┐
         ▼                      ▼                      ▼
  [ core/config ]        [ core/interface ]     [ modules/engines ]
  • yaml loader          • box layouts          • host_discovery.py
  • input validator      • loading screens      • port_scanner.py
         │                      │               • security_headers.py
         └──────────────────────┼──────────────────────┘
                                │
                                ▼
                       [ core/report.py ]
            ┌───────────────────┼───────────────────┐
            ▼                   ▼                   ▼
       ( JSON / CSV )      ( HTML Report )     ( PDF Output )

```

---

## ⚙️ Technology Stack

* **Programming Language:** Python 3.12+
* **Dependencies & Infrastructure Libraries:**
* `PyYAML`: Schema parsing configuration handling.
* `colorama`: Cross-platform console text formatting.
* `dnspython`: Low-level network domain zone query validation.
* `python-whois`: Structured registry entry parsing.
* `requests`: Native HTTP/S response tracking and analyzer.
* `fpdf2`: Automated PDF document synthesis engine.



---

## 🚀 Installation

### Prerequisites

* Ensure Python **3.12** or higher is installed on your local environment.
* High-speed internet access for downloading pip distribution packages.

### Clone Repository

```bash
git clone https://github.com/muhammad-umair09/PenKit.git
cd PenKit

```

### Install Dependencies

#### On Linux / macOS Systems:

```bash
chmod +x install.sh
./install.sh

```

#### On Windows Systems:

```cmd
install.bat

```

### Run Project

Ensure your virtual environment is active, then initialize the application control screen:

```bash
source venv/bin/activate  # On Windows use: venv\Scripts\activate
python main.py

```

---

## 💻 Usage

PenKit uses a simplified interactive option routing system. Below is a structured scanning scenario:

### Executing a Multi-Threaded Port Audit

1. Choose Option `2` from the interface menu selection.
2. Provide the destination target parameter host identifier: `scanme.nmap.org`.
3. Choose the portfolio layout criteria: `common` for standard service groups, or `custom` to target explicit ports.
4. Watch the runtime visual progress bars register progress as open states are printed out live.
5. Provide a confirmation value `y` upon tool completion to export compilation records:

```text
PenKit >> 2
Enter target host/IP: scanme.nmap.org
Scan mode (common/custom): common
Progress: |██████████████████████████████| 100.0% Complete

[+] Found Open Port: 22 (SSH)
[+] Found Open Port: 80 (HTTP)

Export report? (y/n): y
Format (txt, json, csv, html, pdf) [json]: pdf
[+] Report cleanly compiled and dropped here: reports/port_scan_scanme.nmap.org_20260706_170000.pdf

```

---

## 📁 Project Structure

```text
PenKit/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── main.py
├── install.sh
├── install.bat
├── assets/
│   ├── banner.txt
│   └── logo.txt
├── config/
│   └── config.yaml
├── core/
│   ├── banner.py
│   ├── colors.py
│   ├── config_loader.py
│   ├── helpers.py
│   ├── logger.py
│   ├── progress.py
│   ├── report.py
│   └── validator.py
├── modules/
│   ├── base64_tool.py
│   ├── banner_grabber.py
│   ├── directory_checker.py
│   ├── dns_lookup.py
│   ├── hash_generator.py
│   ├── host_discovery.py
│   ├── http_headers.py
│   ├── port_scanner.py
│   ├── robots_parser.py
│   ├── security_headers.py
│   ├── ssl_checker.py
│   ├── subdomain_enum.py
│   └── whois_lookup.py
├── tests/
│   └── test_penkit.py
├── logs/
├── reports/
├── results/
└── docs/

```

---

## 🔧 Configuration

The global execution parameters are entirely governed via the `config/config.yaml` layout definition file:

```yaml
settings:
  timeout: 3.0                 # Floating-point values for connection limits
  threads: 10                  # Multi-threaded execution limit pool definitions
  output_folder: "reports"     # Target system directory where reports are dumped
  theme: "dark_hacker"         # System aesthetic interface selector mapping
  default_report_format: "json"# Automated export backup formatting selector

```

---

## 🔒 Security Considerations

* **Local Verification Contexts:** All actions, scanners, and scripts function out of synchronous/asynchronous connection setups (`socket.connect_ex`). No malicious payloads are included.
* **Credential Data Hardening:** The codebase contains absolute zero hardcoded access values or dynamic network bypass components.
* **Data Handling Hygiene:** Raw string configurations gathered during operations are sanitized for character set anomalies before serialization inside local directory reports.

---

## 🧪 Testing

PenKit uses native Python `unittest` code modules verifying functional status patterns across validators and conversion utilities:

Run the test suite using the following command:

```bash
python -m unittest discover -s tests -p "test_*.py"

```

---

## 🛠️ Troubleshooting

### Common Issue: Domain Resolution Dropped Error

* **Cause:** System local DNS servers can occasionally block rapid query streams or the targeted domain layout format may be malformed.
* **Resolution:** Ensure domain inputs exclude protocol prefixes like `https://` unless interacting explicitly with web configuration target menus.

### Common Issue: Missing Modules (`No module named 'fpdf2'`)

* **Cause:** Execution sequence initiated outside active local project virtual workspaces.
* **Resolution:** Re-execute package sync scripts (`install.sh` or `install.bat`) and verify environment status activation sequences (`source venv/bin/activate`).

---

## 🚀 Future Enhancements / Roadmap

* [ ] Add CIDR notation block target expansion arrays inside host discovery modules.
* [ ] Implement custom user-defined dictionary file path arguments within directory scanners.
* [ ] Build interactive visualization graphs showcasing open asset surfaces within the HTML export layout generator.

---

## 🤝 Contributing

Contributions are welcome. Please read the following steps to maintain clean code quality:

1. Fork the PenKit repository infrastructure.
2. Construct a dedicated structural feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit modification criteria changes matching documented typing rules (`git commit -m 'Add some AmazingFeature'`).
4. Push updates to your origin branch space (`git push origin feature/AmazingFeature`).
5. Open an official Pull Request for evaluation.

### Code Style Guidelines

Ensure modifications comply entirely with standard **PEP 8** coding standards, utilize explicit type hints on signatures, and feature docstrings for all exposed methods.
#   p e n k i t  
 