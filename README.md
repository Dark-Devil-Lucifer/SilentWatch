# SilentWatch

🛡️ SilentWatch — Real-time Keylogger Detection (Python + PyQt5)

SilentWatch is a lightweight GUI application built with Python and PyQt5 that scans running processes in real time to detect potential keylogger activity and suspicious programs. It is intended as an investigative and monitoring tool — not a replacement for full endpoint security solutions.

Key features
- Real-time process scanning
- Suspicious keyword matching for process names/paths
- Exportable scan logs (CSV / plain text)
- Clean dark-mode GUI built with PyQt5
- System information display (CPU, memory, processes)

Quick requirements
- Python 3.8+ (or the Python 3.x series available on your platform)
- PyQt5
- psutil

Installation
1. Clone the repository:

```bash
git clone https://github.com/Dark-Devil-Lucifer/SilentWatch.git
cd SilentWatch
```

2. (Recommended) Create and activate a virtual environment:

```bash
python -m venv venv
# On macOS / Linux
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

3. Install the dependencies:

```bash
pip install PyQt5 psutil
# Or if you include a requirements.txt in the future:
# pip install -r requirements.txt
```

Usage

From the project root run:

```bash
python silentwatch.py
```

Notes:
- On Windows, you may need to run the application with elevated privileges (Run as Administrator) to allow process inspection.
- On some platforms, process metadata and access may be restricted by the OS — SilentWatch reports what it can observe with the current permissions.

Exporting logs

Use the UI controls to export scan logs. Logs are exported in a simple CSV/plain-text format to a location you choose.

Security & Privacy

SilentWatch inspects running processes and may capture process names, paths, and basic system information. It does not transmit data anywhere by default — exported logs are stored locally. Treat exported logs as sensitive information.

Limitations
- SilentWatch is a detection/monitoring tool and is not a complete antivirus or endpoint protection product.
- False positives are possible (benign programs may look suspicious based on name/path patterns). Use discretion when acting on detections.

Troubleshooting
- If the UI fails to start, ensure PyQt5 is installed and compatible with your Python version.
- If process scanning returns limited results, try running the app with elevated privileges.

Contributing
Contributions, bug reports, and feature requests are welcome. Please open issues or pull requests in the repository. A good starting workflow:

1. Fork the repo
2. Create a feature branch
3. Make changes and include tests where relevant
4. Open a pull request describing your changes

License
If you plan to share or accept contributions, consider adding a LICENSE file (for example, MIT, Apache-2.0) to make the project's terms clear.

Acknowledgements
- Built with PyQt5 for the GUI
- Uses psutil for process and system information

Contact
For questions or help, open an issue on GitHub: https://github.com/Dark-Devil-Lucifer/SilentWatch

