from PySide2.QtWidgets import QDialog, QTextEdit
from PySide2.QtCore import Qt

__all__ = ["show_output"]

class ModifiedQDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(ModifiedQDialog,self).__init__(*args,**kwargs)
        self.output = QTextEdit(self)
        self.output.setGeometry(0, 0, self.width(), self.height())
        self.output.setReadOnly(True)

    def resizeEvent(self, event):
        super(ModifiedQDialog, self).resizeEvent(event)
        self.output.resize(self.size())

def show_output(s="",func_name="",ret=None):
    dialog = ModifiedQDialog()
    dialog.resize(400,300)
    dialog.output.setText(s)
    dialog.setWindowTitle("Output of {0} - returns {1}".format(func_name,ret))
    dialog.setWindowModality(Qt.NonModal)
    dialog.exec_()
    dialog.deleteLater()