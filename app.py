import sys
import hashlib
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel
from PyQt5.QtCore import Qt

class FileIntegrityChecker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Integrity Checker")
        self.setGeometry(300, 300, 400, 250)

        # Layout
        self.layout = QVBoxLayout()

        # Create Widgets
        self.label = QLabel("Enter the original checksum:", self)
        self.label.setAlignment(Qt.AlignLeft)
        
        # Input field for original checksum
        self.checksum_input = QLineEdit(self)
        self.checksum_input.setPlaceholderText("Enter the original checksum here...")
        
        # Browse button
        self.browse_button = QPushButton("Browse File", self)
        self.browse_button.clicked.connect(self.browse_file)

        # Result label
        self.result_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignCenter)

        # Add widgets to layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.checksum_input)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)

    def browse_file(self):
        # Open file dialog to select a file
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*.*)")
        if file_path:
            self.check_file_integrity(file_path)

    def calculate_checksum(self, file_path, hash_algorithm="sha256"):
        """
        Calculate checksum for a file using a specified hash algorithm (default is SHA-256).
        
        :param file_path: Path to the file for which checksum needs to be calculated.
        :param hash_algorithm: The hash algorithm to use ('sha256', 'sha1', 'md5', etc.).
        :return: The checksum as a string.
        """
        # Choose the hash algorithm
        hash_func = getattr(hashlib, hash_algorithm)()

        try:
            # Open the file in binary read mode
            with open(file_path, "rb") as f:
                # Read the file in chunks and update the hash
                for byte_block in iter(lambda: f.read(4096), b""):
                    hash_func.update(byte_block)

            # Return the final checksum
            return hash_func.hexdigest()

        except Exception as e:
            return f"Error calculating checksum: {e}"

    def check_file_integrity(self, file_path):
        # Get the original checksum from the input field
        original_checksum = self.checksum_input.text().strip()

        # If no checksum is provided, show an error
        if not original_checksum:
            self.result_label.setText("Please enter the original checksum.")
            return

        # Calculate the checksum of the selected file
        local_checksum = self.calculate_checksum(file_path, hash_algorithm="sha256")
        if "Error" in local_checksum:
            self.result_label.setText(local_checksum)
            return

        # Compare the local checksum with the original checksum
        if local_checksum == original_checksum:
            self.result_label.setText("File integrity check passed!")
        else:
            self.result_label.setText("File integrity check failed!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileIntegrityChecker()
    window.show()
    sys.exit(app.exec_())
