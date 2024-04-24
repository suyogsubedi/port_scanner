import sys
import socket
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt


class PortScannerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.report = ""

    def initUI(self):
        """Initialize the user interface."""
        self.setWindowTitle('Port Scanner')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # IP input field
        ip_layout = QHBoxLayout()
        self.ip_label = QLabel('Enter IP Address:')
        self.ip_input = QLineEdit()
        ip_layout.addWidget(self.ip_label)
        ip_layout.addWidget(self.ip_input)
        layout.addLayout(ip_layout)

        # Port input field
        port_layout = QHBoxLayout()
        self.port_label = QLabel('Enter Port Numbers (comma-separated):')
        self.port_input = QLineEdit()
        port_layout.addWidget(self.port_label)
        port_layout.addWidget(self.port_input)
        layout.addLayout(port_layout)

        # Button layout
        button_layout = QHBoxLayout()

        # Scan Ports button
        self.scan_button = QPushButton('Scan Ports')
        self.scan_button.clicked.connect(self.scan_ports)
        button_layout.addWidget(self.scan_button)

        # Save Results button
        self.save_button = QPushButton('Save Results')
        self.save_button.clicked.connect(self.save_results)
        button_layout.addWidget(self.save_button)

        # Clear Results button
        self.clear_button = QPushButton('Clear Results')
        self.clear_button.clicked.connect(self.clear_results)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)

        # Text area to display results
        self.report_text = QTextEdit()
        layout.addWidget(self.report_text)

        self.setLayout(layout)

    def scan_ports(self):
        """Scan the specified ports on the target IP address."""
        ip = self.ip_input.text()
        ports = self.port_input.text().split(',')

        new_report = f"Port scan report for {ip} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}):\n"

        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, int(port)))
                if result == 0:
                    new_report += f"Port {port}: Open\n"
                elif result == 11:
                    new_report += f"Port {port}: Filtered\n"
                else:
                    new_report += f"Port {port}: Closed\n"
                sock.close()
            except Exception as e:
                new_report += f"Error scanning port {port}: {str(e)}\n"

        self.report += new_report
        self.report_text.append(new_report)

    def save_results(self):
        """Save the scan results to a text file."""
        current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
        default_filename = f"port_scan_results_{current_datetime}.txt"

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", default_filename, "Text Files (*.txt);;All Files (*)", options=options)
        
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.report)
            QMessageBox.information(self, "Save File", "Results saved successfully!")

    def clear_results(self):
        """Clear the displayed results."""
        self.report_text.clear()
        self.report = ''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PortScannerApp()
    window.show()
    sys.exit(app.exec_())
