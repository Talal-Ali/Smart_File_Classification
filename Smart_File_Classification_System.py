import os
import sys
import shutil
import sqlite3 as sq
from tkinter import messagebox
import tkinter as tk

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH    = os.path.join(SCRIPT_DIR, "datatypes.db")


def get_types():
    if not os.path.exists(DB_PATH):
        show_popup("Error", f"Database not found:\n{DB_PATH}")
        sys.exit(1)
    con = sq.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        SELECT dt.Type, c.Category
        FROM DataTypes dt
        JOIN Categories c ON dt.Category_ID = c.Category_ID
    """)
    types_dict = {row[0]: row[1] for row in cur.fetchall()}
    con.close()
    return types_dict


def show_popup(title, message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, message)
    root.destroy()


def organize(folder):
    types_dict = get_types()
    moved      = []
    skipped    = []

    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        if os.path.isdir(fpath) or fname.startswith('.'):
            continue
        _, ext   = os.path.splitext(fname)
        ext      = ext.lower()
        category = types_dict.get(ext, "Other")
        dest_dir = os.path.join(folder, category)
        try:
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(fpath, os.path.join(dest_dir, fname))
            moved.append((fname, category))
        except Exception as e:
            print(f"Could not move {fname}: {e}")
            skipped.append(fname)

    return moved, skipped


def build_summary(folder, moved, skipped):
    if not moved and not skipped:
        return f"Nothing to organize in:\n{folder}"

    by_category = {}
    for fname, category in moved:
        by_category.setdefault(category, []).append(fname)

    lines = [f"Organized {len(moved)} file(s) in:\n{folder}\n"]
    for category, files in sorted(by_category.items()):
        lines.append(f"  {category} ({len(files)})")

    if skipped:
        lines.append(f"\nCould not move {len(skipped)} file(s):")
        for fname in skipped:
            lines.append(f"  {fname}")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_popup("Smart Classifier", "Usage:\nRight-click a folder to organize it.")
        sys.exit(0)

    folder = sys.argv[1]

    if not os.path.isdir(folder):
        show_popup("Error", f"Folder not found:\n{folder}")
        sys.exit(1)

    moved, skipped = organize(folder)
    summary        = build_summary(folder, moved, skipped)
    show_popup("Smart Classifier — Done", summary)