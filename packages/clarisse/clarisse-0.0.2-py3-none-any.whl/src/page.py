"""
Clarisse

page module.
Define class Page, the canvas of type in types_supported.py.

by 1MLightyears@gmail.com

on 20201211
"""

from PySide2.QtWidgets import QPushButton,QScrollArea,QLineEdit,QLabel,QWidget,QFormLayout
from PySide2.QtCore import QThread, Signal, QSize, Qt

from output_dialog import show_output

import log
import sys
import io

__all__=["Page","PageCanvas"]

class RedirectIO():
    def __init__(self, s: str = ""):
        self.content = s
    def write(self, s):
        self.content+=str(s)
    def read(self):
        return self.content.strip(" \n")

class RunThread(QThread):
    """
    The real function-executor.
    """
    def __init__(self,func,func_args:tuple=(),func_kwargs:dict={},parent=None, *args, **kwargs):
        super().__init__(parent=None, *args, **kwargs)
        self.func = func
        self.args = func_args
        self.kwargs = func_kwargs
        self.ret=None

    def run(self):
        log.info("run func with args={0},kwargs={1}".format(self.args,self.kwargs))
        self.ret = self.func(*self.args, **self.kwargs)
        return self.ret

class PageCanvas(QWidget):
    OnResize = Signal(QSize)
    def resizeEvent(self, event):
        self.OnResize.emit(self.size())

class Page(QWidget):
    def __init__(self,
            func=None,
            func_args=[],
            func_kwargs={},
            margin=30,
            vert_spacing=10,
            Current_Layout="TopBottomLayout",
            description="",
            *args, **kwargs
        ):
        super().__init__()

        # static definitions
        self.func = func
        self.args = func_args
        self.kwargs = func_kwargs
        self.widget_list = []
        self.margin = margin
        self.vert_spacing =vert_spacing
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.Current_Layout=getattr(self,Current_Layout,self.TopBottomLayout)

        # Initiallize: create widgets
        # main_window -> central_widget -> page ->  widget_scroll -> canvas
        self.canvas = PageCanvas()

        # create a scroll bar
        self.widget_scroll = QScrollArea(self)
        self.widget_scroll.setWidget(self.canvas)

        # use a QFormLayout to place widgets
        self.form_layout = QFormLayout()
        self.form_layout.setMargin(self.margin)
        self.form_layout.setSpacing(self.vert_spacing)
        self.form_layout.setRowWrapPolicy(self.form_layout.WrapLongRows)
        self.canvas.setLayout(self.form_layout)

        # default description is func.__doc__
        description = self.func.__doc__ if description=="" else description
        self.description = QLabel(description) # doesn't need to scroll
        self.description.setParent(self)
        self.description.setTextFormat(Qt.MarkdownText)
        self.description.setOpenExternalLinks(True)
        log.info("description geometry={0}".format(self.description.geometry()))

        # create a Run button to excute the function
        self.run_button = QPushButton("&Run", self)
        self.run_button.clicked.connect(self.Run)
        self.run_button.adjustSize()

        self.Current_Layout(self.size())

        log.info("button geometry={geometry}".format(geometry=self.run_button.geometry()))

        # allow the user to run the func multiple times to test output
        # but only the last return is delivered (as a confirmed run)
        self.run_thread = RunThread(self.func, self.args, self.kwargs)
        self.run_thread.finished.connect(self.Done)

    def setArgs(self, *args, **kwargs):
        """
        Set and update arguments for running self.func.
        """
        self.args = args + self.args[len(args):]
        self.kwargs.update(kwargs)

    ### Layouts
    def TopBottomLayout(self, page_size):
        """
        set an up-down layout for self.page.
        """
        self.resize(page_size)

        # description should be placed on the top
        self.description.move(self.x()+self.margin,self.y()+self.margin)
        self.description.adjustSize()

        # run_button should be placed below description
        self.run_button.setGeometry(
            self.margin,
            self.description.y()+self.description.height()+self.margin,
            page_size.width() - 2*self.margin,
            self.run_button.height()
        )

        # canvas should be placed below run_button
        self.canvas.setGeometry(
            self.x(),
            self.run_button.y()+self.run_button.height(),
            page_size.width()-self.margin, # scroll has width
            self.canvas.height()
        )

        # widget_scroll should be placed between the end of page and run_button
        self.widget_scroll.setGeometry(
            self.x(),
            self.run_button.y()+self.run_button.height(),
            page_size.width(),
            page_size.height()-self.run_button.y()-self.run_button.height())

    ### slot functions
    def Run(self):
        """
        Run self.func in another thread.
        """
        for i in self.widget_list:
            self.kwargs.update({i.objectName(): i.getValue()})

        # redirect standard output
        self.redirect_IO = RedirectIO()
        sys.stdout = self.redirect_IO
        sys.stderr = self.redirect_IO

        # avoid multiple clicks
        self.run_button.setText("Running...")
        self.run_button.setEnabled(False)
        self.run_thread.start()

    def Done(self):
        """
        Restore run_button.
        """
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        show_output(self.redirect_IO.read(),self.func.__name__,self.run_thread.ret)
        self.run_button.setText("Run")
        self.run_button.setEnabled(True)