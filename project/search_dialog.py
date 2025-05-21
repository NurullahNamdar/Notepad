from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox

class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        # Set up the dialog
        self.setWindowTitle("Find and Replace")
        self.resize(400, 200)
        self.setMinimumWidth(350)
        
        # Set style
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            
            QLabel {
                color: #212529;
            }
            
            QLineEdit {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 8px;
                background-color: #ffffff;
            }
            
            QLineEdit:focus {
                border-color: #3498db;
            }
            
            QPushButton {
                background-color: #3498db;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            
            QPushButton:hover {
                background-color: #2980b9;
            }
            
            QPushButton:pressed {
                background-color: #1f6aa5;
            }
            
            QCheckBox {
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            
            QCheckBox::indicator:unchecked {
                border: 1px solid #e0e0e0;
                background-color: #ffffff;
                border-radius: 2px;
            }
            
            QCheckBox::indicator:checked {
                border: 1px solid #3498db;
                background-color: #3498db;
                border-radius: 2px;
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # Find section
        find_label = QLabel("Find:")
        self.find_text = QLineEdit()
        
        # Replace section
        replace_label = QLabel("Replace with:")
        self.replace_text = QLineEdit()
        
        # Options
        options_layout = QHBoxLayout()
        
        self.case_sensitive = QCheckBox("Match case")
        self.whole_words = QCheckBox("Whole words")
        self.search_backward = QCheckBox("Search backward")
        
        options_layout.addWidget(self.case_sensitive)
        options_layout.addWidget(self.whole_words)
        options_layout.addWidget(self.search_backward)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.find_button = QPushButton("Find Next")
        self.replace_button = QPushButton("Replace")
        self.replace_all_button = QPushButton("Replace All")
        self.close_button = QPushButton("Close")
        
        button_layout.addWidget(self.find_button)
        button_layout.addWidget(self.replace_button)
        button_layout.addWidget(self.replace_all_button)
        button_layout.addWidget(self.close_button)
        
        # Add to main layout
        layout.addWidget(find_label)
        layout.addWidget(self.find_text)
        layout.addWidget(replace_label)
        layout.addWidget(self.replace_text)
        layout.addLayout(options_layout)
        layout.addStretch(1)
        layout.addLayout(button_layout)
        
        # Connect signals
        self.find_button.clicked.connect(self.find_next)
        self.replace_button.clicked.connect(self.replace)
        self.replace_all_button.clicked.connect(self.replace_all)
        self.close_button.clicked.connect(self.close)
        
        # Set focus
        self.find_text.setFocus()
    
    def find_next(self):
        """Find the next occurrence of the text"""
        text = self.find_text.text()
        if not text:
            return
            
        found = self.parent.find_text(
            text,
            self.case_sensitive.isChecked(),
            self.whole_words.isChecked(),
            self.search_backward.isChecked()
        )
        
        if not found:
            QtWidgets.QMessageBox.information(
                self, "Find", f"Cannot find '{text}'", QtWidgets.QMessageBox.Ok
            )
    
    def replace(self):
        """Replace the current selection"""
        find_text = self.find_text.text()
        replace_text = self.replace_text.text()
        
        if not find_text:
            return
            
        replaced = self.parent.replace_text(
            find_text,
            replace_text,
            self.case_sensitive.isChecked(),
            self.whole_words.isChecked()
        )
        
        if replaced:
            self.find_next()
    
    def replace_all(self):
        """Replace all occurrences of the text"""
        find_text = self.find_text.text()
        replace_text = self.replace_text.text()
        
        if not find_text:
            return
            
        self.parent.replace_all(
            find_text,
            replace_text,
            self.case_sensitive.isChecked(),
            self.whole_words.isChecked()
        )