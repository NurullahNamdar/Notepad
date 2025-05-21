import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog, 
                            QMessageBox, QFontDialog, QTextEdit, 
                            QInputDialog, QDialog)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QTextCursor, QFont, QKeySequence, QTextDocument
from search_dialog import SearchDialog

class NotepadApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Load the UI file
        uic.loadUi('notepad.ui', self)
        
        # Set window properties
        self.setWindowTitle("Simple Notepad")
        self.setMinimumSize(600, 400)
        
        # Instance variables
        self.current_file = None
        self.modified = False
        
        # Initialize icons
        self.setup_icons()
        
        # Connect signals and slots
        self.connect_actions()
        
        # Set up the status bar
        self.setup_status_bar()
        
        # Show the window
        self.show()
    
    def setup_icons(self):
        """Set up icons for actions"""
        icon_size = QSize(16, 16)
        self.actionNew.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_FileIcon))
        self.actionOpen.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton))
        self.actionSave.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogSaveButton))
        self.actionCut.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogResetButton))
        self.actionCopy.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogYesButton))
        self.actionPaste.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogNoButton))
        self.actionUndo.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ArrowBack))
        self.actionRedo.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ArrowForward))
        self.actionFind.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_FileDialogContentsView))
        
        # Set toolbar icon size
        self.toolBar.setIconSize(icon_size)
    
    def connect_actions(self):
        """Connect menu and toolbar actions to methods"""
        # File actions
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSaveAs.triggered.connect(self.save_file_as)
        self.actionExit.triggered.connect(self.close)
        
        # Edit actions
        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionPaste.triggered.connect(self.textEdit.paste)
        self.actionSelectAll.triggered.connect(self.textEdit.selectAll)
        self.actionFind.triggered.connect(self.show_find_dialog)
        
        # Format actions
        self.actionFont.triggered.connect(self.choose_font)
        self.actionWordWrap.toggled.connect(self.toggle_word_wrap)
        
        # View actions
        self.actionStatusBar.toggled.connect(self.statusbar.setVisible)
        self.actionToolBar.toggled.connect(self.toolBar.setVisible)
        
        # TextEdit changes
        self.textEdit.textChanged.connect(self.text_changed)
    
    def setup_status_bar(self):
        """Set up the status bar with line and column display"""
        self.statusbar.showMessage("Ready", 2000)
        
        # Create labels for displaying cursor position
        self.position_label = QtWidgets.QLabel("Ln: 1, Col: 1")
        self.statusbar.addPermanentWidget(self.position_label)
        
        # Connect cursor position signal
        self.textEdit.cursorPositionChanged.connect(self.update_cursor_position)
        
        # Initial update
        self.update_cursor_position()
    
    def update_cursor_position(self):
        """Update the cursor position display in the status bar"""
        cursor = self.textEdit.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.columnNumber() + 1
        self.position_label.setText(f"Ln: {line}, Col: {column}")
    
    def update_title(self):
        """Update the window title with the current file name and modified indicator"""
        title = "Simple Notepad"
        if self.current_file:
            filename = os.path.basename(self.current_file)
            title = f"{filename}{' *' if self.modified else ''} - {title}"
        elif self.modified:
            title = f"Untitled *- {title}"
        self.setWindowTitle(title)
    
    def text_changed(self):
        """Handle text changes in the editor"""
        if not self.modified:
            self.modified = True
            self.update_title()
    
    def new_file(self):
        """Create a new file"""
        if self.modified and self.check_save():
            return
            
        self.textEdit.clear()
        self.current_file = None
        self.modified = False
        self.update_title()
        self.statusbar.showMessage("New file created", 2000)
    
    def open_file(self):
        """Open an existing file"""
        if self.modified and self.check_save():
            return
            
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt);;All Files (*)", 
            options=options
        )
        
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    self.textEdit.setPlainText(file.read())
                self.current_file = file_name
                self.modified = False
                self.update_title()
                self.statusbar.showMessage(f"Opened {os.path.basename(file_name)}", 2000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open the file: {str(e)}")
    
    def save_file(self):
        """Save the current file"""
        if self.current_file:
            return self.save_to_file(self.current_file)
        else:
            return self.save_file_as()
    
    def save_file_as(self):
        """Save the current file with a new name"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Text Files (*.txt);;All Files (*)", 
            options=options
        )
        
        if file_name:
            success = self.save_to_file(file_name)
            if success:
                self.current_file = file_name
                self.update_title()
            return success
        return False
    
    def save_to_file(self, file_name):
        """Save the text to the specified file"""
        try:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.textEdit.toPlainText())
            self.modified = False
            self.update_title()
            self.statusbar.showMessage(f"Saved {os.path.basename(file_name)}", 2000)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save the file: {str(e)}")
            return False
    
    def check_save(self):
        """Check if the document needs to be saved and prompt the user"""
        if not self.modified:
            return False
            
        reply = QMessageBox.question(
            self, "Save Changes?", 
            "The document has been modified. Do you want to save changes?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
            QMessageBox.Save
        )
        
        if reply == QMessageBox.Save:
            return not self.save_file()
        elif reply == QMessageBox.Cancel:
            return True
        return False
    
    def show_find_dialog(self):
        """Show the find dialog"""
        dialog = SearchDialog(self)
        dialog.exec_()
    
    def find_text(self, text, case_sensitive=False, whole_words=False, search_backward=False):
        """Find text in the document"""
        flags = QTextDocument.FindFlags()
        
        if case_sensitive:
            flags |= QTextDocument.FindCaseSensitively
        if whole_words:
            flags |= QTextDocument.FindWholeWords
        if search_backward:
            flags |= QTextDocument.FindBackward
            
        cursor = self.textEdit.textCursor()
        if not self.textEdit.find(text, flags):
            # If not found from current position, try from beginning
            cursor.movePosition(QTextCursor.Start if not search_backward else QTextCursor.End)
            self.textEdit.setTextCursor(cursor)
            return self.textEdit.find(text, flags)
        return True
    
    def replace_text(self, find_text, replace_text, case_sensitive=False, whole_words=False):
        """Replace the current selection with the replacement text"""
        cursor = self.textEdit.textCursor()
        if cursor.hasSelection() and cursor.selectedText() == (find_text if case_sensitive else find_text.lower()):
            cursor.insertText(replace_text)
            return True
        return False
    
    def replace_all(self, find_text, replace_text, case_sensitive=False, whole_words=False):
        """Replace all occurrences of the find text with the replacement text"""
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.textEdit.setTextCursor(cursor)
        
        count = 0
        while self.find_text(find_text, case_sensitive, whole_words):
            self.replace_text(find_text, replace_text, case_sensitive, whole_words)
            count += 1
            
        QMessageBox.information(self, "Replace All", f"Replaced {count} occurrences.")
    
    def choose_font(self):
        """Show the font dialog and set the selected font"""
        current_font = self.textEdit.font()
        font, ok = QFontDialog.getFont(current_font, self, "Select Font")
        if ok:
            self.textEdit.setFont(font)
    
    def toggle_word_wrap(self, wrap):
        """Toggle word wrap mode"""
        if wrap:
            self.textEdit.setLineWrapMode(QTextEdit.WidgetWidth)
        else:
            self.textEdit.setLineWrapMode(QTextEdit.NoWrap)
    
    def closeEvent(self, event):
        """Handle the window close event"""
        if self.modified and self.check_save():
            event.ignore()
        else:
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Set Fusion style for a modern look
    window = NotepadApp()
    sys.exit(app.exec_())