# https://www.youtube.com/watch?v=gFxZ3SerLoo guide for all code 
import os , sys, io
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QListWidget, \
                            QVBoxLayout, QHBoxLayout, QGridLayout, \
                            QDialog, QFileDialog, QMessageBox, QAbstractItemView 

from PyQt5.QtCore import Qt, QUrl 
from PyQt5.QtGui import QIcon
# https://www.pythonguis.com/tutorials/creating-your-first-pyqt-window/ # guide for pyqt 

from PyPDF2 import PdfFileMerger,PdfFileReader, PdfFileWriter

def resource_path(rel_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, rel_path)


class ListWidget(QListWidget):
    def __init__(self,parent=None):
        super().__init__(parent=None)
        self.setAcceptDrops(True)
        self.setStyleSheet('''font-size:25px''')
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else: 
            return super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else: 
            return super().dragMoveEvent(event)
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            pdfFiles = []

            for url in event.mimeData().urls():
                if url.isLocalFile():
                    if url.toString().endswith('.pdf'):
                        pdfFiles.append(str(url.toLocalFile()))
                self.addItems(pdfFiles)
        else:
            return super().dropEvent(event)

class output_field(QLineEdit):
    def __init__(self):
        super().__init__()
        self.height = 55 
        self.setStyleSheet('font-size: 30px;')
        self.setFixedHeight(self.height)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):    
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            if event.mimeData().urls():
                self.setText(event.mimeData().urls()[0].toLocalFile())
        else:
            event.ignore()

class button(QPushButton):
    def __init__(self,label_text):
        super().__init__()
        self.setText(label_text)
        self.setStyleSheet(''''
        font-size: 30px;
        width: 180px;
        height: 50px;
        ''')

class PDFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF File Merge")
        self.setWindowIcon(QIcon("bookicon.png"))
        self.resize(1800,800)
        self.initUI()

        self.buttonBrowseOutputFile.clicked.connect(self.populateFileName)      

    def get_dir(self):
        self.current_dir = os.getcwd()
        return self.current_dir
    
    def initUI(self):
        mainLayout = QVBoxLayout()
        outputFolderRow = QHBoxLayout()
        buttonLayout =  QHBoxLayout()

        self.outputFile = output_field()
        outputFolderRow.addWidget(self.outputFile)

        self.buttonBrowseOutputFile = button('&Save To')
        self.buttonBrowseOutputFile.setFixedHeight(self.outputFile.height)
        outputFolderRow.addWidget(self.buttonBrowseOutputFile)
        """
        Listbox widget
        """
        # listbox widget 
        self.pdfListWidget = ListWidget(self)

        """
        Button
        """
        self.buttonDeleteSelect = button('&Delete')
        self.buttonDeleteSelect.clicked.connect(self.deleteSelected)
        buttonLayout.addWidget(self.buttonDeleteSelect,1,Qt.AlignRight)

        self.buttonMerge = button('&Merge')
        self.buttonMerge.clicked.connect(self.mergerFile)
        buttonLayout.addWidget(self.buttonMerge)

        self.buttonClose = button('&Close')
        self.buttonClose.clicked.connect(QApplication.quit)
        buttonLayout.addWidget(self.buttonClose)

        self.buttonReset = button('&Reset')
        self.buttonReset.clicked.connect(self.clearQueue)
        buttonLayout.addWidget(self.buttonReset)

        mainLayout.addLayout(outputFolderRow)
        mainLayout.addWidget(self.pdfListWidget)
        mainLayout.addLayout(buttonLayout)
        
        self.setLayout(mainLayout)

    def deleteSelected(self):
        for item in self.pdfListWidget.selectedItems():
            self.pdfListWidget.takeItem(self.pdfListWidget.row(item))

    def clearQueue(self):
        self.pdfListWidget.clear()
        self.outputFile.setText('')

    def dialogMessage(self,message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle('PDF Manager')
        dlg.setIcon(QMessageBox.Information)
        dlg.setText(message)
        dlg.show()

    def _getSaveFilePath(self):
        # foo_dir = QFileDialog.getExistingDirectory()
        default_dir =  os.path.dirname(self.pdfListWidget.item(0).text()) # os.getcwd()
        file_save_path,_ = QFileDialog.getSaveFileName(self,'Save PDF File',default_dir,'PDF file (*.pdf)')
        
        return file_save_path
    
    def populateFileName(self):
        path = self._getSaveFilePath()
        if path:
            self.dialogMessage('Review saving url and click "Merge" button ')
            self.outputFile.setText(path)

    def mergerFile(self):
        if not self.outputFile.text():
            self.populateFileName()
            return 
        
        if self.pdfListWidget.count() > 0:
            pdfMerger = PdfFileMerger()

            try:
                for i in range(self.pdfListWidget.count()):
                    pdfMerger.append(self.pdfListWidget.item(i).text())
                    # self.dialogMessage('Click Merge button to get the output files')
                
                pdfMerger.write(self.outputFile.text())
                pdfMerger.close()
                

                self.pdfListWidget.clear()
                self.outputFile.clear()
                self.dialogMessage('PDF Merger Complete')
        
            except Exception as e:
                self.dialogMessage(e)
        else:
            self.dialogMessage('Queue is empty')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    pdfApp = PDFApp()
    pdfApp.show()

    sys.exit(app.exec_())
