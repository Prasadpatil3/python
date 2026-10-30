"""Main entry point for the Student Record Management System."""

import sys
import tkinter as tk
from gui import StudentManagementApp


def setup_windows_dpi():
    """Enable crisp font rendering on high-DPI Windows screens."""
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass


def main():
    setup_windows_dpi()
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
