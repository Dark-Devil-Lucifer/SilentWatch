import sys
import psutil
import datetime
import platform
import socket
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTextEdit, QListWidget, QStackedWidget, QMessageBox,
    QFileDialog
)
from PyQt5.QtGui import QFont, QPixmap, QIcon

class ScannerThread(QThread):
    update_output = pyqtSignal(str)
    scan_complete = pyqtSignal()

    def __init__(self, whitelist):
        super().__init__()
        self._running = True
        self.whitelist = whitelist

    def run(self):
        self.update_output.emit("\n🔍 Starting scan...\n")
        suspicious_found = False

        for proc in psutil.process_iter(['pid', 'name']):
            if not self._running:
                self.update_output.emit("⏹ Scan stopped by user.\n")
                break

            try:
                name = proc.info['name']
                pid = proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

            if name.lower() in self.whitelist:
                self.update_output.emit(f"✓ Whitelisted: {name} (PID {pid})\n")
                continue

            suspicious_keywords = ['keylogger', 'logger', 'hook', 'capture', 'keyboard']
            if any(k in name.lower() for k in suspicious_keywords):
                self.update_output.emit(f"⚠️ Suspicious: {name} (PID {pid})\n")
                suspicious_found = True
            else:
                self.update_output.emit(f"✓ Safe: {name} (PID {pid})\n")

        if not suspicious_found and self._running:
            self.update_output.emit("✅ No suspicious processes found.\n")

        self.scan_complete.emit()

    def stop(self):
        self._running = False

class SilentWatchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LUCIFER's Gadgets - SilentWatch")
        self.setGeometry(100, 100, 900, 600)

        self.whitelist = set(["gsd-keyboard", "systemd", "bash", "python", "python3"])
        self.log_history = []

        self.init_ui()

    def init_ui(self):
        # Background image
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("images.jpeg"))
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, 900, 600)

        # Translucent panel
        self.panel = QWidget(self)
        self.panel.setGeometry(30, 30, 840, 540)
        self.panel.setStyleSheet("""
            background-color: rgba(0, 0, 0, 150);
            border: 2px solid #00FF00;
            border-radius: 15px;
        """)

        self.stacked_widget = QStackedWidget(self.panel)
        self.stacked_widget.setGeometry(10, 10, 820, 520)

        self.home_screen = QWidget()
        self.main_screen = QWidget()
        self.contact_screen = QWidget()

        self.init_home_screen()
        self.init_main_screen()
        self.init_contact_screen()

        self.stacked_widget.addWidget(self.home_screen)
        self.stacked_widget.addWidget(self.main_screen)
        self.stacked_widget.addWidget(self.contact_screen)
        self.stacked_widget.setCurrentWidget(self.home_screen)

    def init_home_screen(self):
        layout = QVBoxLayout()

        welcome = QLabel("Welcome to SilentWatch")
        welcome.setFont(QFont("Consolas", 26, QFont.Bold))
        welcome.setStyleSheet("color: #00FF00;")
        welcome.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome)

        description = QLabel(
            "<b>SilentWatch</b> is your personal security companion.<br><br>"
            "It features <b>real-time system monitoring</b>, <b>automatic detection of suspicious activity</b>,<br>"
            "detailed system insights, and a clean user interface built for professionals.<br><br>"
            "🔐 <b>Features</b>:<br>"
            "✔️ <b>Real-Time Process Scanner</b><br>"
            "✔️ <b>Smart Threat Classifier</b><br>"
            "✔️ <b>One-click Process Details</b><br>"
            "✔️ <b>Exportable Scan Reports</b><br>"
            "✔️ <b>Dark Mode Dashboard</b><br>"
            "✔️ <b>Lightweight, Fast, and Accurate</b><br>"
            "✔️ <b>Designed for Security Analysts & Power Users</b>"
        )
        description.setFont(QFont("Consolas", 11))
        description.setStyleSheet("color: white;")
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)

        contact_button = QPushButton("Contact: Ajay Chouhan")
        contact_button.setFont(QFont("Consolas", 11, QFont.Bold))
        contact_button.setStyleSheet("""
            background-color: rgba(0, 0, 0, 180);
            color: #00FF00;
            border: 2px solid #00FF00;
            border-radius: 10px;
            padding: 8px;
        """)
        contact_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.contact_screen))
        layout.addWidget(contact_button, alignment=Qt.AlignCenter)

        start_button = QPushButton("Launch Dashboard")
        start_button.setFont(QFont("Consolas", 12))
        start_button.setStyleSheet("background-color: black; color: #00FF00; border: 2px solid #00FF00; border-radius: 10px; padding: 10px;")
        start_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_screen))
        layout.addWidget(start_button, alignment=Qt.AlignCenter)

        self.home_screen.setLayout(layout)

    def init_contact_screen(self):
        layout = QVBoxLayout()

        title = QLabel("Contact Developer")
        title.setFont(QFont("Consolas", 18, QFont.Bold))
        title.setStyleSheet("color: #00FF00;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        info = QLabel(
            "<b>Name:</b> Ajay Chouhan<br>"
            "<b>Phone:</b> 8871632529<br>"
            "<b>Email:</b> ajjudon2529@gamil.com<br><br>"
            "<b>GitHub:</b> github.com/ajaychouhan<br>"
            "<b>LinkedIn:</b> linkedin.com/in/ajaychouhan<br>"
            "<b>Location:</b> India"
        )
        info.setFont(QFont("Consolas", 12))
        info.setStyleSheet("color: white;")
        info.setAlignment(Qt.AlignCenter)
        info.setWordWrap(True)
        layout.addWidget(info)

        back_button = QPushButton("Back to Home")
        back_button.setStyleSheet("background-color: black; color: #00FF00; border: 2px solid #00FF00; border-radius: 10px; padding: 8px;")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_screen))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.contact_screen.setLayout(layout)

    def init_main_screen(self):
        layout = QVBoxLayout()

        title = QLabel("SilentWatch - System Monitor")
        title.setFont(QFont("Consolas", 16, QFont.Bold))
        title.setStyleSheet("color: #00FF00;")
        layout.addWidget(title)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { height: 30px; width: 150px; background-color: black; color: #00FF00; font-weight: bold; }")
        layout.addWidget(self.tabs)

        self.tab_system = QWidget()
        self.tab_scan = QWidget()
        self.tab_history = QWidget()

        self.tabs.addTab(self.tab_system, "System Info")
        self.tabs.addTab(self.tab_scan, "Scan")
        self.tabs.addTab(self.tab_history, "History")

        self.init_system_tab()
        self.init_scan_tab()
        self.init_history_tab()

        back_button = QPushButton("Back to Home")
        back_button.setStyleSheet("background-color: black; color: #00FF00; border: 2px solid #00FF00; border-radius: 10px; padding: 8px;")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_screen))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.main_screen.setLayout(layout)

    def init_system_tab(self):
        layout = QVBoxLayout()
        self.sysinfo_text = QTextEdit()
        self.sysinfo_text.setReadOnly(True)
        self.sysinfo_text.setStyleSheet("background-color: black; color: #00FF00;")
        layout.addWidget(self.sysinfo_text)

        btn_refresh = QPushButton("Refresh System Info")
        btn_refresh.setStyleSheet("background-color: black; color: #00FF00; border: 1px solid #00FF00;")
        btn_refresh.clicked.connect(self.update_system_info)
        layout.addWidget(btn_refresh)

        self.tab_system.setLayout(layout)
        self.update_system_info()

    def update_system_info(self):
        info = [
            f"System: {platform.system()} {platform.release()}",
            f"Node Name: {platform.node()}",
            f"Machine: {platform.machine()}",
            f"Processor: {platform.processor()}",
            f"Python Version: {platform.python_version()}"
        ]

        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            info.append(f"Hostname: {hostname}")
            info.append(f"IP Address: {ip_address}")
        except:
            info.append("IP Address: Unknown")



        self.sysinfo_text.setText("\n".join(info))

    def init_scan_tab(self):
        layout = QVBoxLayout()
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setStyleSheet("background-color: black; color: #00FF00;")
        layout.addWidget(self.output_box)

        btn_layout = QHBoxLayout()

        self.btn_start_scan = QPushButton("Start Scan")
        self.btn_start_scan.setStyleSheet("background-color: black; color: #00FF00; border: 1px solid #00FF00;")
        self.btn_start_scan.clicked.connect(self.start_scan)
        btn_layout.addWidget(self.btn_start_scan)

        self.btn_stop_scan = QPushButton("Stop Scan")
        self.btn_stop_scan.setStyleSheet("background-color: black; color: #00FF00; border: 1px solid #00FF00;")
        self.btn_stop_scan.clicked.connect(self.stop_scan)
        self.btn_stop_scan.setEnabled(False)
        btn_layout.addWidget(self.btn_stop_scan)

        self.btn_export = QPushButton("Export Log")
        self.btn_export.setStyleSheet("background-color: black; color: #00FF00; border: 1px solid #00FF00;")
        self.btn_export.clicked.connect(self.export_log)
        btn_layout.addWidget(self.btn_export)

        layout.addLayout(btn_layout)
        self.tab_scan.setLayout(layout)

    def init_history_tab(self):
        layout = QVBoxLayout()
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("background-color: black; color: #00FF00;")
        layout.addWidget(self.history_list)
        self.tab_history.setLayout(layout)

    def start_scan(self):
        self.output_box.clear()
        self.scanner_thread = ScannerThread(self.whitelist)
        self.scanner_thread.update_output.connect(self.output_box.append)
        self.scanner_thread.scan_complete.connect(self.scan_finished)
        self.scanner_thread.start()
        self.btn_start_scan.setEnabled(False)
        self.btn_stop_scan.setEnabled(True)

    def stop_scan(self):
        if self.scanner_thread:
            self.scanner_thread.stop()
            self.btn_start_scan.setEnabled(True)
            self.btn_stop_scan.setEnabled(False)

    def scan_finished(self):
        self.btn_start_scan.setEnabled(True)
        self.btn_stop_scan.setEnabled(False)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f"--- Scan @ {now} ---\n{self.output_box.toPlainText()}\n"
        self.log_history.append(log)
        self.history_list.addItem(f"Scan @ {now}")
        QMessageBox.information(self, "Scan Complete", "Scan finished. Review the output and history for details.")

    def export_log(self):
        if not self.output_box.toPlainText().strip():
            QMessageBox.warning(self, "No Data", "There is no scan data to export.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Save Log", "scan_log.txt", "Text Files (*.txt)")
        if filename:
            with open(filename, 'w') as file:
                file.write(self.output_box.toPlainText())
            QMessageBox.information(self, "Exported", f"Log saved to {filename}")


def main():
    app = QApplication(sys.argv)
    window = SilentWatchApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
