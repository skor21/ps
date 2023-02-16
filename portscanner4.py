import pyfiglet
import sys
import socket
from datetime import datetime
from tqdm import tqdm
from PyQt5 import QtCore, QtWidgets

class Scanner(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("PORT SCANNER")

        # Create labels and input boxes
        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("Enter a hostname:")
        self.label1.move(50, 50)

        self.host_name = QtWidgets.QLineEdit(self)
        self.host_name.setText("")
        self.host_name.move(200, 50)
        self.host_name.resize(200, 32)
        self.label2 = QtWidgets.QLabel(self)
        self.label2.setText("Number of ports to scan:")
        self.label2.move(50, 90)

        self.ports = QtWidgets.QLineEdit(self)
        self.ports.setText("")
        self.ports.move(200, 90)
        self.ports.resize(200, 32)

        # Create a label to display scan status
        self.status_label = QtWidgets.QLabel(self)
        self.status_label.move(50, 130)
        self.status_label.resize(400, 32)

        # Create a button to start the scan
        self.button = QtWidgets.QPushButton(self)
        self.button.setText("Scan!")
        self.button.move(200, 170)
        self.button.clicked.connect(self.start_scan)

    def start_scan(self):
        # Get the host name and number of ports to scan from the input boxes
        host_name = self.host_name.text()
        ports_to_scan = self.ports.text()

        if not host_name:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please enter a hostname.')
            return

        if not ports_to_scan:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please enter the number of ports to scan.')
            return

        # Convert the string to a list of integers
        if ports_to_scan.lower() == 'a':
            ports = range(1, 65536)
        else:
            try:
                ports = range(1, int(ports_to_scan)+1)
            except ValueError:
                QtWidgets.QMessageBox.warning(self, 'Error', 'Invalid input for ports.')
                return

        # Disable the input boxes and button while the scan is running
        self.host_name.setEnabled(False)
        self.ports.setEnabled(False)
        self.button.setEnabled(False)

        # Start the scan
        self.status_label.setText("Scanning...")
        self.update()
        open_ports = []
        for port in tqdm(ports):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((host_name, port))
            if result == 0:
                open_ports.append(port)
            sock.close()

        # Display the results
        if len(open_ports) > 0:
            self.status_label.setText("Open ports: " + str(open_ports))
        else:
            self.status_label.setText("No open ports found")

        # Enable the input boxes and button
        self.host_name.setEnabled(True)
        self.ports.setEnabled(True)
        self.button.setEnabled(True)
        
        # Close the window
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Scanner()
    ex.show()
    sys.exit(app.exec_())
