
from tkinter import Tk
from controller.main_controller import MainController

if __name__ == "__main__":
    root = Tk()
    app = MainController(root)
    root.mainloop()
