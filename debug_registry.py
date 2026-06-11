import winreg

def check_key(hive, path):
    try:
        key = winreg.OpenKey(hive, path)
        print(f"EXISTS: {path}")
        winreg.CloseKey(key)
    except FileNotFoundError:
        print(f"NOT FOUND: {path}")

print("=== Checking registry entries ===\n")

# Check old entry
check_key(winreg.HKEY_CLASSES_ROOT,   r"Directory\shell\SmartClassifier")
check_key(winreg.HKEY_CLASSES_ROOT,   r"Directory\shell\SmartClassifier\command")

# Check new entry
check_key(winreg.HKEY_CURRENT_USER,   r"Software\Classes\directory\shell\SmartClassifier")
check_key(winreg.HKEY_CURRENT_USER,   r"Software\Classes\directory\shell\SmartClassifier\command")