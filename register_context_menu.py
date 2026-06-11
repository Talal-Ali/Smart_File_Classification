import winreg
import os
import sys

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
ORGANIZER    = os.path.join(SCRIPT_DIR, "Smart_File_Classification_System.py")
LABEL        = "Organize with Smart Classifier"

def add_context_menu():
    try:
        command = f'pythonw "{ORGANIZER}" "%1"'

        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\directory\shell\SmartClassifier")
        winreg.SetValueEx(key, "",     0, winreg.REG_SZ, LABEL)
        winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, "shell32.dll,4")
        winreg.CloseKey(key)

        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\directory\shell\SmartClassifier\command")
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)

        print("Context menu added successfully!")

    except PermissionError:
        print("Error: Run this script as Administrator.")
        sys.exit(1)


def remove_context_menu():
    paths = [
        (winreg.HKEY_CURRENT_USER,  r"Software\Classes\directory\shell\SmartClassifier\command"),
        (winreg.HKEY_CURRENT_USER,  r"Software\Classes\directory\shell\SmartClassifier"),
        (winreg.HKEY_CLASSES_ROOT,  r"Directory\shell\SmartClassifier\command"),
        (winreg.HKEY_CLASSES_ROOT,  r"Directory\shell\SmartClassifier"),
    ]
    for hive, path in paths:
        try:
            winreg.DeleteKey(hive, path)
            print(f"Removed: {path}")
        except FileNotFoundError:
            pass
        except PermissionError:
            print("Error: Run this script as Administrator.")
            sys.exit(1)
    print("Done.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "remove":
        remove_context_menu()
    else:
        add_context_menu()