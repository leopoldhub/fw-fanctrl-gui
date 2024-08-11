import sys

from PySide6 import QtWidgets, QtUiTools, QtGui
from PySide6.QtCore import QFile, QTextStream, QIODevice, Slot
from PySide6.QtGui import QIcon

from src.exception.ServiceException import ServiceException
from src.app.SystemTray import main as systemTrayMain
from src.GCBypass import GCBYPASS

class MainWindow:
    def __init__(self, icon, fanctrlService):
        self.fanctrlService = fanctrlService

        # Load the UI file
        self.ui = QtUiTools.QUiLoader().load("resources/ui/main/main.ui")
        self.ui.setWindowIcon(icon)

        # Set the style
        qss_file = QFile("resources/ui/main/main.qss")
        if qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
            qss_stream = QTextStream(qss_file)
            self.ui.setStyleSheet(qss_stream.readAll())
            qss_file.close()

        reloadStrategyButton = self.ui.findChild(
            QtWidgets.QPushButton, "Button_ReloadStrategy"
        )
        reloadStrategyButton.clicked.connect(self.onReloadButtonClick)

        changeStrategyButton = self.ui.findChild(
            QtWidgets.QPushButton, "Button_ChangeStrategy"
        )
        changeStrategyButton.clicked.connect(self.onChangeStrategyButtonClick)

        resetStrategyButton = self.ui.findChild(
            QtWidgets.QPushButton, "Button_Reset"
        )
        resetStrategyButton.clicked.connect(self.onResetStrategyButtonClick)

        pauseButton = self.ui.findChild(
            QtWidgets.QPushButton, "Button_Pause"
        )
        pauseButton.clicked.connect(self.onPauseButtonClick)

        resumeButton = self.ui.findChild(
            QtWidgets.QPushButton, "Button_Resume"
        )
        resumeButton.clicked.connect(self.onResumeButtonClick)

        self.updateStrategies()

    @Slot()
    def onReloadButtonClick(self):
        self.updateStrategies()

    @Slot()
    def onChangeStrategyButtonClick(self):
        self.useSelectedStrategy()

    @Slot()
    def onResetStrategyButtonClick(self):
        self.resetStrategy()

    @Slot()
    def onPauseButtonClick(self):
        self.pauseService()

    @Slot()
    def onResumeButtonClick(self):
        self.resumeService()

    def getErrorLabel(self):
        return self.ui.findChild(QtWidgets.QPlainTextEdit, "TextArea_Error")

    def printError(self, error):
        self.getErrorLabel().show()
        print(error, file=sys.stderr)
        self.getErrorLabel().setPlainText(error)

    def hideErrorLabel(self):
        self.getErrorLabel().hide()

    def updateStrategies(self):
        self.hideErrorLabel()
        try:
            self.fanctrlService.reload()
            strategyList = self.fanctrlService.getStrategies()
            comboBox = self.ui.findChild(
                QtWidgets.QComboBox, "ComboBox_Strategy"
            )
            comboBox.clear()
            comboBox.addItems(strategyList)
            currentStrategy = self.fanctrlService.getCurrentStrategy()
            comboBox.setCurrentText(currentStrategy)
            if hasattr(self, "tray") and self.tray is not None:
                self.tray.refresh(currentStrategy, strategyList)
        except ServiceException as e:
            self.printError(e.args[0])
        except Exception as e:
            self.printError(e)

    def useStrategy(self, strategy):
        self.hideErrorLabel()
        try:
            self.fanctrlService.use(strategy)
        except ServiceException as e:
            self.printError(e.args[0])
        except Exception as e:
            self.printError(e)
        self.updateStrategies()

    def resetStrategy(self):
        self.hideErrorLabel()
        try:
            self.fanctrlService.reset()
        except ServiceException as e:
            self.printError(e.args[0])
        except Exception as e:
            self.printError(e)
        self.updateStrategies()

    def pauseService(self):
        self.hideErrorLabel()
        try:
            self.fanctrlService.pause()
        except ServiceException as e:
            self.printError(e.args[0])
        except Exception as e:
            self.printError(e)

    def resumeService(self):
        self.hideErrorLabel()
        try:
            self.fanctrlService.resume()
        except ServiceException as e:
            self.printError(e.args[0])
        except Exception as e:
            self.printError(e)

    def useSelectedStrategy(self):
        comboBox = self.ui.findChild(
            QtWidgets.QComboBox, "ComboBox_Strategy"
        )
        self.useStrategy(comboBox.currentText())


def main(args, app, fanctrlService):
    app.setQuitOnLastWindowClosed(False)

    icon = QIcon()
    GCBYPASS[icon] = icon
    icon.addFile("resources/icons/icon-256.ico")
    icon.addFile("resources/icons/icon-128.ico")
    icon.addFile("resources/icons/icon-64.ico")
    icon.addFile("resources/icons/icon-32.ico")
    icon.addFile("resources/icons/icon-16.ico")
    app.setWindowIcon(icon)

    QtGui.QFontDatabase.addApplicationFont(
        "resources/font/Font Awesome 6 Brands-Regular-400.otf"
    )
    QtGui.QFontDatabase.addApplicationFont(
        "resources/font/Font Awesome 6 Free-Regular-400.otf"
    )
    QtGui.QFontDatabase.addApplicationFont(
        "resources/font/Font Awesome 6 Free-Solid-900.otf"
    )

    window = MainWindow(icon, fanctrlService)
    if not args.background:
        window.ui.show()

    window.tray = systemTrayMain(icon, app, window, fanctrlService)

    return window


if __name__ == "__main__":
    main()
