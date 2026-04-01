import tkinter as tk
from src.ui import NumberStringGameUI

def main():
    root = tk.Tk()
    app = NumberStringGameUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
