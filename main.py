import threading
import sys
from PyQt5 import QtWidgets

import storage
import front_end
import ipc_front_end
import back_end
import ipc_back_end
import ipc_server


def main():
    server = ipc_server.IPCServer()
    threading.Thread(target=server.run_server).start()

    business_logic = back_end.BackEndLogic(ipc_back_end.IpcBackEnd(), storage.Storage())
    threading.Thread(target=business_logic.ipc.ipc.listen).start()

    app = QtWidgets.QApplication(sys.argv)
    front_panel = front_end.GuiController(ipc_front_end.IpcFrontEnd())
    sys.exit(app.exec_())
    # front_panel.show_ui()
    # print("got to the end")



if __name__ == "__main__":
    main()