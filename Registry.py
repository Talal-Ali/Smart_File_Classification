import winreg
import os
import sys

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
ORGANIZER    = os.path.join(SCRIPT_DIR, "Smart_File_Classification_System.py")
LABEL        = "Organize with Smart Classifier"
GUID         = "{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}"

def add_context_menu():
    try:
        # Modern Windows 11 context menu path
        base_path    = f"Software\\Classes\\directory\\shell\\SmartClassifier"
        command_path = f"Software\\Classes\\directory\\shell\\SmartClassifier\\command"
        command      = f'pythonw "{ORGANIZER}" "%1"'

        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, base_path)
        winreg.SetValueEx(key, "",            0, winreg.REG_SZ, LABEL)
        winreg.SetValueEx(key, "Icon",        0, winreg.REG_SZ, "shell32.dll,4")  # folder icon
        winreg.SetValueEx(key, "ExplorerCommandHandler", 0, winreg.REG_SZ, GUID)
        winreg.CloseKey(key)

        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_path)
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)

        print("Context menu added successfully!")
        print(f"Label:   {LABEL}")
        print(f"Runs:    {command}")

    except PermissionError:
        print("Error: Run this script as Administrator.")
        sys.exit(1)


def remove_context_menu():
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\directory\\shell\\SmartClassifier\\command")
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"Software\\Classes\\directory\\shell\\SmartClassifier")
        print("Context menu removed successfully!")
    except FileNotFoundError:
        print("Context menu entry not found.")
    except PermissionError:
        print("Error: Run this script as Administrator.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "remove":
        remove_context_menu()
    else:
        add_context_menu()