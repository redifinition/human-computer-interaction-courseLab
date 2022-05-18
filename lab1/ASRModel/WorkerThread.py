from PyQt5.QtCore import QThread, pyqtSignal

from ASRModel.CommandExecutor import CommandExecutorSingleton


class InputWorker(QThread):
    sig = pyqtSignal(str)

    def __init__(self):
        super(InputWorker,self).__init__()
        # 单例模式，指令处理器
        self.command_executor = CommandExecutorSingleton()

    def run(self):
        result = self.command_executor.getCommand()
        print(result)
        self.sig.emit(result)
