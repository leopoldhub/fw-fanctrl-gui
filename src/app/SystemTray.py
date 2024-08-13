from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QSystemTrayIcon, QMenu

from src.GCBypass import GCBYPASS


class SystemTray(QSystemTrayIcon):
    def __init__(self, icon, app, mainWindow, fanctrlService):
        self.app = app
        self.mainWindow = mainWindow
        self.fanctrlService = fanctrlService
        super().__init__()
        self.setToolTip("fw fan control GUI")
        self.setIcon(icon)

        self.mainMenu = QMenu()

        self.reloadAction = QAction("Reload")
        self.reloadAction.triggered.connect(self.onClickReload)
        self.mainMenu.addAction(self.reloadAction)

        self.mainMenu.addSeparator()

        self.currentStrategyAction = QAction("current: STRATEGY")
        self.currentStrategyAction.setDisabled(True)
        self.mainMenu.addAction(self.currentStrategyAction)

        self.mainMenu.addSeparator()

        self.strategyListMenu = QMenu()
        self.strategyListMenu.setTitle("Choose strategy")
        self.mainMenu.addAction(self.strategyListMenu.menuAction())

        self.mainMenu.addSeparator()

        self.resetAction = QAction("Reset")
        self.resetAction.triggered.connect(self.onClickReset)
        self.mainMenu.addAction(self.resetAction)

        self.mainMenu.addSeparator()

        self.pauseAction = QAction("Pause")
        self.pauseAction.triggered.connect(self.onClickPause)
        self.mainMenu.addAction(self.pauseAction)

        self.resumeAction = QAction("Resume")
        self.resumeAction.triggered.connect(self.onClickResume)
        self.mainMenu.addAction(self.resumeAction)

        self.mainMenu.addSeparator()

        self.openAction = QAction("Open")
        self.openAction.triggered.connect(self.onClickShow)
        self.mainMenu.addAction(self.openAction)

        self.quitAction = QAction("Quit")
        self.quitAction.triggered.connect(self.onClickQuit)
        self.mainMenu.addAction(self.quitAction)

        self.activated.connect(self.onClickShow)

        self.setContextMenu(self.mainMenu)
        self.setVisible(True)

        QTimer.singleShot(500, self.onClickReload)

        GCBYPASS["tray"] = {}

    def onClickShow(self):
        self.mainWindow.ui.show()
        self.mainWindow.ui.raise_()
        self.mainWindow.ui.activateWindow()

    def onClickQuit(self):
        self.app.quit()

    def onClickReload(self):
        self.mainWindow.updateStrategies()

    def onClickReset(self):
        self.mainWindow.resetStrategy()

    def onClickPause(self):
        self.mainWindow.pauseService()

    def onClickResume(self):
        self.mainWindow.resumeService()

    def onStrategyChooseClick(self, strategy):
        self.mainWindow.useStrategy(strategy)

    def refresh(self, currentStrategy, strategies):
        self.currentStrategyAction.setText(f"current: {currentStrategy}")
        self.strategyListMenu.clear()
        for strategy in strategies:
            self.addToStrategyListMenu(strategy)

    def addToStrategyListMenu(self, strategy):
        action = QAction(strategy)
        action.triggered.connect(lambda: self.onStrategyChooseClick(strategy))
        GCBYPASS["tray"][f"{strategy}"] = action
        self.strategyListMenu.addAction(action)


def main(icon, app, mainWindow, fanctrlService):
    return SystemTray(icon, app, mainWindow, fanctrlService)


if __name__ == "__main__":
    main()
