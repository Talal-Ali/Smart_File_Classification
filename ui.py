
import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3 as sq
import os


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datatypes.db")


BG_MAIN     = "#494949"   # main window background (light grey)
BG_HEADER   = "#2C3E50"   # header bar (dark navy)
BG_ROW_ODD  = "#505050"   # odd row background
BG_ROW_EVEN = "#212121"   # even row background (subtle stripe)
FG_MAIN     = "#FFFFFF"   # primary text colour
FG_LIGHT    = "#FFFFFF"   # text on dark backgrounds
BTN_ADD     = "#27AE60"   # green — add action
BTN_EDIT    = "#2980B9"   # blue  — edit action
BTN_DELETE  = "#E74C3C"   # red   — delete action
BTN_CLOSE   = "#95A5A6"   # grey  — close/cancel

FONT_TITLE  = ("Segoe UI", 14, "bold")
FONT_HEAD   = ("Segoe UI", 10, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_BTN    = ("Segoe UI", 9, "bold")


# ─────────────────────────────────────────────
# DATABASE HELPERS
# All DB logic lives here, separate from the UI.
# Each function opens its own connection so the
# UI never holds a long-lived DB handle.
# ─────────────────────────────────────────────

def db_connect():
    """
    Open and return a connection to the database.
    Raises SystemExit with a message if the file is not found.
    """
    if not os.path.exists(DB_PATH):
        messagebox.showerror("Database Not Found", f"Could not find {DB_PATH}")
        raise SystemExit
    return sq.connect(DB_PATH)


def db_get_categories():
    """
    Fetch all categories from the Categories table.

    Returns
    -------
    list of tuples : [(Category_ID, Category), ...]
        e.g. [(1, 'Documents'), (2, 'Developer'), ...]
    """
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT Category_ID, Category FROM Categories ORDER BY Category")
    rows = cur.fetchall()
    con.close()
    return rows


def db_category_exists(name):
    """
    Check whether a category name already exists (case-insensitive).

    Parameters
    ----------
    name : str  The category name to check.

    Returns
    -------
    bool : True if the category exists, False otherwise.
    """
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT 1 FROM Categories WHERE LOWER(Category) = LOWER(?)", (name,))
    exists = cur.fetchone() is not None
    con.close()
    return exists


def db_add_category(name):
    """
    Insert a new category into the Categories table.

    Parameters
    ----------
    name : str  The category name to insert.
    """
    con = db_connect()
    cur = con.cursor()
    cur.execute("INSERT INTO Categories (Category) VALUES (?)", (name,))
    con.commit()
    con.close()


def db_edit_category(category_id, new_name):
    """
    Update the name of an existing category.

    Parameters
    ----------
    category_id : int  The ID of the category to update.
    new_name    : str  The new name for the category.
    """
    con = db_connect()
    cur = con.cursor()
    cur.execute("UPDATE Categories SET Category = ? WHERE Category_ID = ?", (new_name, category_id))
    con.commit()
    con.close()


def db_delete_category(category_id):
    """
    Delete a category and all its associated file types.

    Parameters
    ----------
    category_id : int  The ID of the category to delete.

    Note: DataTypes rows are deleted first to avoid foreign key violations.
    """
    con = db_connect()
    cur = con.cursor()
    cur.execute("DELETE FROM DataTypes WHERE Category_ID = ?", (category_id,))
    cur.execute("DELETE FROM Categories WHERE Category_ID = ?", (category_id,))
    con.commit()
    con.close()


def db_get_types(category_id):
    """
    Fetch all file extensions belonging to a category.

    Parameters
    ----------
    category_id : int  The ID of the category.

    Returns
    -------
    list of str : ['.pdf', '.docx', ...]
    """
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT Type FROM DataTypes WHERE Category_ID = ? ORDER BY Type", (category_id,))
    rows = [r[0] for r in cur.fetchall()]
    con.close()
    return rows


def db_type_exists(ext):
    """
    Check if a file extension already exists in any category.

    Parameters
    ----------
    ext : str  The extension to check (e.g. '.pdf').

    Returns
    -------
    str or None : The category name it belongs to, or None if not found.
    """
    con = db_connect()
    cur = con.cursor()
    cur.execute("""
        SELECT c.Category FROM DataTypes dt
        JOIN Categories c ON dt.Category_ID = c.Category_ID
        WHERE LOWER(dt.Type) = LOWER(?)
    """, (ext,))
    row = cur.fetchone()
    con.close()
    return row[0] if row else None


def db_add_type(ext, category_id):
    """
    Insert a new file extension into the DataTypes table.

    Parameters
    ----------
    ext         : str  The file extension (e.g. '.pdf').
    category_id : int  The ID of the category it belongs to.
    """
    con = db_connect()
    cur = con.cursor()
    cur.execute("INSERT INTO DataTypes (Type, Category_ID) VALUES (?, ?)", (ext, category_id))
    con.commit()
    con.close()


def db_edit_type(old_ext, new_ext):
    """
    Rename a file extension in the DataTypes table.

    Parameters
    ----------
    old_ext : str  The current extension name.
    new_ext : str  The new extension name.
    """
    con = db_connect()
    cur = con.cursor()
    cur.execute("UPDATE DataTypes SET Type = ? WHERE Type = ?", (new_ext, old_ext))
    con.commit()
    con.close()


def db_delete_type(ext):
    """
    Delete a file extension from the DataTypes table.

    Parameters
    ----------
    ext : str  The extension to delete.
    """
    con = db_connect()
    cur = con.cursor()
    cur.execute("DELETE FROM DataTypes WHERE Type = ?", (ext,))
    con.commit()
    con.close()


# ─────────────────────────────────────────────
# HELPER — parse semicolon-separated input
# ─────────────────────────────────────────────

def parse_input(raw):
    """
    Split a semicolon-separated string into a cleaned list of values.
    Strips whitespace and ignores empty entries.

    Parameters
    ----------
    raw : str  User input e.g. "Documents;Databases;3D-Models"

    Returns
    -------
    list of str : ['Documents', 'Databases', '3D-Models']
    """
    return [v.strip() for v in raw.split(";") if v.strip()]


def normalise_ext(ext):
    """
    Ensure an extension starts with a dot and is lowercased.
    e.g. 'PDF' → '.pdf',  '.Py' → '.py',  '.pdf' → '.pdf'

    Parameters
    ----------
    ext : str

    Returns
    -------
    str
    """
    ext = ext.strip().lower()
    if not ext.startswith("."):
        ext = "." + ext
    return ext


# ─────────────────────────────────────────────
# TYPES WINDOW
# Opens as a popup when the user clicks ▽ on a
# category row. Shows all extensions for that
# category with Add / Edit / Delete controls.
# ─────────────────────────────────────────────

class TypesWindow(tk.Toplevel):
    """
    Popup window that displays and manages file extensions
    for a single category.

    Parameters
    ----------
    parent      : tk.Widget  The parent window (App).
    category_id : int        The DB ID of the category.
    category    : str        The display name of the category.
    """

    def __init__(self, parent, category_id, category):
        super().__init__(parent)
        self.category_id = category_id
        self.category    = category

        self.title(f"{category} — File Types")
        self.resizable(False, False)
        self.configure(bg=BG_MAIN)
        self.grab_set()  # make this window modal (blocks the parent)

        self._build_ui()
        self._load_types()

        # centre the popup over the parent window
        self.update_idletasks()
        px = parent.winfo_x() + (parent.winfo_width()  // 2) - (self.winfo_width()  // 2)
        py = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{px}+{py}")

    def _build_ui(self):
        """Build all widgets for the types window."""

        # ── Header ──────────────────────────────
        header = tk.Frame(self, bg=BG_HEADER, pady=10)
        header.pack(fill="x")
        tk.Label(header, text=f"📄 {self.category}",
                 bg=BG_HEADER, fg=FG_LIGHT, font=FONT_TITLE).pack(padx=16)
        tk.Label(header, text="Manage file extensions for this category",
                 bg=BG_HEADER, fg="#95A5A6", font=FONT_BODY).pack()

        # ── List frame ───────────────────────────
        list_frame = tk.Frame(self, bg=BG_MAIN, padx=16, pady=12)
        list_frame.pack(fill="both", expand=True)

        # scrollable listbox
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            list_frame,
            fg="#D9D9D9",
            bg="#494949",
            yscrollcommand=scrollbar.set,
            font=FONT_BODY,
            width=28,
            height=10,
            selectbackground="#2980B9",
            selectforeground=FG_LIGHT,
            borderwidth=0,
            highlightthickness=1,
            highlightcolor="#BDC3C7",
            relief="flat"
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)

        # ── Buttons ──────────────────────────────
        btn_frame = tk.Frame(self, bg=BG_MAIN, pady=10)
        btn_frame.pack()

        self._btn(btn_frame, "＋ Add",    BTN_ADD,    self._add).pack(side="left",  padx=6)
        self._btn(btn_frame, "✏ Edit",   BTN_EDIT,   self._edit).pack(side="left", padx=6)
        self._btn(btn_frame, "🗑 Delete", BTN_DELETE, self._delete).pack(side="left", padx=6)
        self._btn(btn_frame, "✕ Close",  BTN_CLOSE,  self.destroy).pack(side="left", padx=6)

    def _btn(self, parent, text, color, command):
        """Helper to create a consistently styled button."""
        return tk.Button(
            parent, text=text, command=command,
            bg=color, fg=FG_LIGHT, font=FONT_BTN,
            relief="flat", padx=12, pady=6, cursor="hand2",
            activebackground=color, activeforeground=FG_LIGHT
        )

    def _load_types(self):
        """
        Reload the listbox from the database.
        Called on init and after every add/edit/delete.
        """
        self.listbox.delete(0, "end")
        types = db_get_types(self.category_id)
        for i, ext in enumerate(types):
            self.listbox.insert("end", f"  {ext}")
            self.listbox.itemconfig(i, bg=BG_ROW_ODD if i % 2 == 0 else BG_ROW_EVEN)

    def _selected(self):
        """
        Return the currently selected extension, stripped of whitespace.
        Shows a warning and returns None if nothing is selected.
        """
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Nothing selected", "Please select a file type first.", parent=self)
            return None
        return self.listbox.get(sel[0]).strip()

    def _add(self):
        """
        Prompt the user for one or more extensions (semicolon-separated),
        validate each one, then insert into the DB.

        Guard rails:
        - Skips blank entries
        - Normalises to lowercase with a leading dot
        - Blocks duplicates that already exist in any category
        """
        raw = simpledialog.askstring(
            "Add File Types",
            "Enter extension(s) separated by semicolons:\ne.g.  .png ; .jpg ; .webp",
            parent=self
        )
        if not raw:
            return

        added, skipped = [], []

        for entry in parse_input(raw):
            ext = normalise_ext(entry)
            existing_cat = db_type_exists(ext)
            if existing_cat:
                # guard rail: extension already assigned somewhere
                skipped.append(f"{ext} (already in '{existing_cat}')")
            else:
                db_add_type(ext, self.category_id)
                added.append(ext)

        self._load_types()

        msg = ""
        if added:
            msg += f"Added: {', '.join(added)}\n"
        if skipped:
            msg += f"\nSkipped (already exist):\n" + "\n".join(skipped)
        if msg:
            messagebox.showinfo("Result", msg.strip(), parent=self)

    def _edit(self):
        """
        Rename the selected extension.

        Guard rails:
        - Blocks renaming to an extension that already exists elsewhere
        - Skips if the user enters the same value
        """
        old = self._selected()
        if not old:
            return

        new_raw = simpledialog.askstring(
            "Edit File Type",
            f"Rename  {old}  to:",
            initialvalue=old,
            parent=self
        )
        if not new_raw:
            return

        new = normalise_ext(new_raw)

        if new == old:
            return  # nothing changed

        existing_cat = db_type_exists(new)
        if existing_cat:
            messagebox.showerror(
                "Already Exists",
                f"'{new}' already exists in category '{existing_cat}'.",
                parent=self
            )
            return

        db_edit_type(old, new)
        self._load_types()

    def _delete(self):
        """
        Delete the selected extension after confirmation.
        """
        ext = self._selected()
        if not ext:
            return

        if messagebox.askyesno("Confirm Delete",
                               f"Delete '{ext}' from {self.category}?", parent=self):
            db_delete_type(ext)
            self._load_types()


# ─────────────────────────────────────────────
# MAIN APP WINDOW
# Shows the full list of categories. Each row
# has the category name and a ▽ button to open
# its TypesWindow. Add / Edit / Delete buttons
# manage categories themselves.
# ─────────────────────────────────────────────

class App(tk.Tk):
    """
    The main application window.
    Manages the category list and provides
    Add / Edit / Delete controls for categories.
    """

    def __init__(self):
        super().__init__()
        self.title("Smart Classifier")
        self.resizable(False, False)
        self.configure(bg=BG_MAIN)

        self._build_ui()
        self._load_categories()

        # centre on screen
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w  = self.winfo_width()
        h  = self.winfo_height()
        self.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")

    def _build_ui(self):
        """Build all widgets for the main window."""

        # ── Header ──────────────────────────────
        header = tk.Frame(self, bg=BG_HEADER, pady=14)
        header.pack(fill="x")
        tk.Label(header, text="🗂  Smart Classifier",
                 bg=BG_HEADER, fg=FG_LIGHT, font=FONT_TITLE).pack(padx=20)
        tk.Label(header, text="Manage categories and file types",
                 bg=BG_HEADER, fg="#3F3F3F", font=FONT_BODY).pack()

        # ── Column headings ──────────────────────
        col_frame = tk.Frame(self, bg="#494949", pady=6)
        col_frame.pack(fill="x", padx=16, pady=(12, 0))
        tk.Label(col_frame, text="Category",
                 bg="#494949", fg=FG_MAIN, font=FONT_HEAD, width=24, anchor="w").pack(side="left", padx=10)
        tk.Label(col_frame, text="Types",
                 bg="#494949", fg=FG_MAIN, font=FONT_HEAD).pack(side="left")

        # ── Scrollable category list ─────────────
        canvas_frame = tk.Frame(self, bg=BG_MAIN)
        canvas_frame.pack(fill="both", expand=True, padx=16, pady=4)

        self.canvas    = tk.Canvas(canvas_frame, bg=BG_MAIN, highlightthickness=0, height=300)
        scrollbar      = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.row_frame = tk.Frame(self.canvas, bg=BG_MAIN)

        self.canvas.create_window((0, 0), window=self.row_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left",  fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.row_frame.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # ── Bottom buttons ───────────────────────
        btn_frame = tk.Frame(self, bg=BG_MAIN, pady=12)
        btn_frame.pack()

        self._btn(btn_frame, "＋ Add Category",    BTN_ADD,    self._add).pack(side="left",  padx=8)
        self._btn(btn_frame, "✏ Edit Category",   BTN_EDIT,   self._edit).pack(side="left", padx=8)
        self._btn(btn_frame, "🗑 Delete Category", BTN_DELETE, self._delete).pack(side="left", padx=8)

        # track which category row is selected
        self._selected_id   = None
        self._selected_name = None
        self._row_widgets   = []   # keep refs to avoid garbage collection

    def _btn(self, parent, text, color, command):
        """Helper to create a consistently styled button."""
        return tk.Button(
            parent, text=text, command=command,
            bg=color, fg=FG_LIGHT, font=FONT_BTN,
            relief="flat", padx=14, pady=7, cursor="hand2",
            activebackground=color, activeforeground=FG_LIGHT
        )

    # ── Category rows ────────────────────────────

    def _load_categories(self):
        """
        Clear and rebuild the category list from the database.
        Called on startup and after every add/edit/delete.
        Resets the current selection.
        """
        # destroy existing rows
        for w in self._row_widgets:
            w.destroy()
        self._row_widgets.clear()
        self._selected_id   = None
        self._selected_name = None

        categories = db_get_categories()

        for i, (cat_id, cat_name) in enumerate(categories):
            bg = BG_ROW_ODD if i % 2 == 0 else BG_ROW_EVEN
            row = tk.Frame(self.row_frame, bg=bg, pady=4)
            row.pack(fill="x")
            self._row_widgets.append(row)

            # category name label — clickable to select the row
            lbl = tk.Label(row, text=cat_name, bg=bg, fg=FG_MAIN,
                           font=FONT_BODY, width=24, anchor="w", cursor="hand2")
            lbl.pack(side="left", padx=10)

            # ▽ button — opens the TypesWindow for this category
            arrow = tk.Button(
                row, text="▽", bg=bg, fg="#2980B9",
                font=FONT_BTN, relief="flat", cursor="hand2",
                command=lambda cid=cat_id, cname=cat_name: self._open_types(cid, cname)
            )
            arrow.pack(side="left", padx=4)

            # clicking either the label or the row selects it
            for widget in (row, lbl, arrow):
                widget.bind("<Button-1>",
                    lambda e, cid=cat_id, cname=cat_name, r=row, b=bg:
                        self._select_row(cid, cname, r, b))

    def _select_row(self, cat_id, cat_name, row_frame, original_bg):
        """
        Highlight the clicked row and store the selected category.

        Parameters
        ----------
        cat_id       : int       DB ID of the selected category.
        cat_name     : str       Name of the selected category.
        row_frame    : tk.Frame  The row widget to highlight.
        original_bg  : str       The row's original background colour.
        """
        # reset all rows to their original colour
        for i, w in enumerate(self._row_widgets):
            w.configure(bg=BG_ROW_ODD if i % 2 == 0 else BG_ROW_EVEN)
            for child in w.winfo_children():
                try:
                    child.configure(bg=BG_ROW_ODD if i % 2 == 0 else BG_ROW_EVEN)
                except Exception:
                    pass

        # highlight selected row
        row_frame.configure(bg="#4CB1FF")
        for child in row_frame.winfo_children():
            try:
                child.configure(bg="#4CB1FF")
            except Exception:
                pass

        self._selected_id   = cat_id
        self._selected_name = cat_name

    def _open_types(self, category_id, category_name):
        """
        Open the TypesWindow popup for the given category.

        Parameters
        ----------
        category_id   : int  DB ID of the category.
        category_name : str  Display name of the category.
        """
        TypesWindow(self, category_id, category_name)

    # ── Category CRUD ────────────────────────────

    def _add(self):
        """
        Prompt for one or more category names (semicolon-separated),
        validate, then insert into the DB.

        Guard rails:
        - Skips blank entries
        - Blocks names that already exist (case-insensitive)
        """
        raw = simpledialog.askstring(
            "Add Categories",
            "Enter category name(s) separated by semicolons:\ne.g.  3D-Models ; Databases",
            parent=self
        )
        if not raw:
            return

        added, skipped = [], []

        for name in parse_input(raw):
            if db_category_exists(name):
                skipped.append(name)
            else:
                db_add_category(name)
                added.append(name)

        self._load_categories()

        msg = ""
        if added:
            msg += f"Added: {', '.join(added)}\n"
        if skipped:
            msg += f"\nSkipped (already exist):\n" + "\n".join(skipped)
        if msg:
            messagebox.showinfo("Result", msg.strip(), parent=self)

    def _edit(self):
        """
        Rename the selected category.

        Guard rails:
        - Warns if no category is selected
        - Blocks renaming to a name that already exists
        """
        if not self._selected_id:
            messagebox.showwarning("Nothing selected",
                                   "Please select a category first.", parent=self)
            return

        new_name = simpledialog.askstring(
            "Edit Category",
            f"Rename  '{self._selected_name}'  to:",
            initialvalue=self._selected_name,
            parent=self
        )
        if not new_name or new_name.strip() == self._selected_name:
            return

        new_name = new_name.strip()

        if db_category_exists(new_name):
            messagebox.showerror("Already Exists",
                                 f"A category named '{new_name}' already exists.", parent=self)
            return

        db_edit_category(self._selected_id, new_name)
        self._load_categories()

    def _delete(self):
        """
        Delete the selected category and ALL its associated file types,
        after a confirmation prompt.
        """
        if not self._selected_id:
            messagebox.showwarning("Nothing selected",
                                   "Please select a category first.", parent=self)
            return

        types = db_get_types(self._selected_id)
        extra = f"\n\nThis will also delete {len(types)} file type(s)." if types else ""

        if messagebox.askyesno(
            "Confirm Delete",
            f"Delete category '{self._selected_name}'?{extra}",
            parent=self
        ):
            db_delete_category(self._selected_id)
            self._load_categories()


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()
