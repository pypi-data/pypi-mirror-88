"""
Clarisse

Window drawing module.
analyze the interface of a function/class.

by 1MLightyears@gmail.com

on 20201211
"""
from analyze import AnalyzeFunc
from page import Page

import sys
import log

from PySide2.QtWidgets import QMainWindow, QApplication, QLabel,  QTabWidget,  QWidget
from PySide2.QtCore import  Signal, QCoreApplication, QMetaObject, QSize
from PySide2.QtGui import  QColor

__all__=["ClrsGUI"]

class Ui_MainWindow(QMainWindow, object):
    OnResize=Signal(QSize)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320,480)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def resizeEvent(self,event):
        QMainWindow.resizeEvent(self, event)
        self.OnResize.emit(self.size())


class ClrsGUI():
    def __init__(self):
        """
        Create and set the Main_Window.
        """
        log.info("ClrsGUI init")
        self.app = QApplication(sys.argv)
        self.main_window = Ui_MainWindow()
        self.main_window.setupUi(self.main_window)
        log.info("main_window create size={size}".format(size=self.main_window.geometry()))

        self.central_widget = QWidget(self.main_window)
        self.main_window.setCentralWidget(self.central_widget)
        self.main_window.OnResize.connect(self.ReDrawAllPages)

    def Parse(self,
            backend,
            default_args: tuple = (),
            default_kwargs: dict = {},
            args_desc: list = [],
            args_kwdesc: dict = {},
            *args,**kwargs):
        """
        Parse the decorated.
        """
        self.pages = []
        self.tabs = None

        # if backend is a function
        if isinstance(backend, type(lambda: 0)):
            # then args and kwargs store the default of all variables
            self.pages.append(Page(backend,*args,**kwargs))
            self.pages[-1].setParent(self.central_widget)
            self.DrawFuncInPage(self.pages[0], backend,default_args,default_kwargs,args_desc,args_kwdesc)
            self.main_window.resize(
                max([i.description.width() + i.description.x() + i.margin for i in self.pages]),
                self.main_window.height()
            )  # resize main_window's width to show all the description
            self.main_window.setWindowTitle("{0} - Clarisse GUI".format(backend.__name__))
        elif isinstance(a, object):
            self.tabs = QTabWidget(self.central_widget)
            # TODO:fill the codes; support classes
            # if backend is a class, decorate its __init__, make all its callable public
            # a page and organize them with self.tabs

    def DrawFuncInPage(self,
            page,
            func,
            default_args: tuple = (),
            default_kwargs: dict = {},
            args_desc: list = [],
            args_kwdesc: dict = {}
        ):
        """
        Draw parameters of function(func) in the main_window,
        set them with appropriate initial values.
        """
        # inspect func
        page.widget_list = AnalyzeFunc(func)
        log.info("page name={0},widget_list={1}".format(page.objectName(),[i.__name__ for i in page.widget_list]))

        # add widgets to canvas
        if page.widget_list != []:
            top=0
            for i in range(len(page.widget_list)):
                row_desc = page.widget_list[i].objectName()
                if len(args_desc) > 0:
                    row_desc = args_desc[0]
                    args_desc = args_desc[1:]
                if page.widget_list[i].objectName() in args_kwdesc:
                    row_desc = args_kwdesc[page.widget_list[i].objectName()]
                page.form_layout.addRow(QLabel(row_desc), page.widget_list[i])

                # apply arguments given to the original func as default args
                if len(default_args)>0:
                    page.widget_list[i].setDefault(default_args[0])
                    default_args = default_args[1:]
                if page.widget_list[i].objectName() in default_kwargs:
                    page.widget_list[i].setDefault(default_args[page.widget_list[i].objectName()])

                log.info("add widget name={name}, geometry={geometry}, desc={desc}".format(
                    name=page.widget_list[i].objectName(),
                    geometry=page.widget_list[i].geometry(),
                    desc=row_desc))

        # canvas resize
        page.canvas.resize(
            page.width(),
            page.canvas.y()+page.widget_list[-1].y()+page.widget_list[-1].height()+page.margin
        )
        log.info("canvas:{0}".format(page.canvas.geometry()))
        log.info("widget_scroll geometry={0}".format(page.widget_scroll.geometry()))
        log.info("page geometry={0}".format(page.geometry()))

        # modify Z-order
        page.run_button.raise_()
        page.description.raise_()

    def ReDrawAllPages(self, new_size: QSize = QSize(640,480)):
        """
        redraw each page to fit the form's size.
        """
        # tabs should adjust size
        if self.tabs != None:
            self.tabs.resize(new_size)
        for page in self.pages:
            page.Current_Layout(new_size)

        log.info("resize all pages to {0}".format(self.central_widget.geometry()))

