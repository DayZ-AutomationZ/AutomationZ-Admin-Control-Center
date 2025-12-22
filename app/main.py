#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import json
import subprocess
import pathlib
import traceback
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except Exception as e:
    raise SystemExit("Tkinter is required. Error: %s" % e)

APP_NAME = "AutomationZ Admin Control Center"
APP_VERSION = "1.0.0"

BASE_DIR = pathlib.Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "tools.json"
LOGS_DIR = BASE_DIR / "logs"
ASSETS_DIR = BASE_DIR / "assets"

# ---- theme colors ----
C_BG = "#333333"       # base background
C_PANEL = "#363636"    # panels
C_TEXT = "#e6e6e6"     # readable light text
C_MUTED = "#b8b8b8"
C_ACCENT = "#4CAF50"   # AutomationZ green
C_WARN = "#ffb74d"
C_BAD = "#ef5350"

DEFAULT_TOOLS: Dict[str, Any] = {
  "tools": [
    {
      "id": "uploader",
      "name": "AutomationZ Uploader",
      "type": "python",
      "entry": "../AutomationZ_Uploader/app/main.py",
      "cwd": "../AutomationZ_Uploader",
      "args": [],
      "description": "Upload presets / files to servers (FTP/FTPS) – standalone tool."
    },
    {
      "id": "scheduler",
      "name": "AutomationZ Scheduler",
      "type": "python",
      "entry": "../AutomationZ_Scheduler/app/main.py",
      "cwd": "../AutomationZ_Scheduler",
      "args": [],
      "description": "Legacy scheduler (v1) – runs planned tasks at set times."
    },
    {
      "id": "backup_scheduler",
      "name": "AutomationZ Server Backup Scheduler",
      "type": "python",
      "entry": "../AutomationZ_Server_Backup_Scheduler/app/main.py",
      "cwd": "../AutomationZ_Server_Backup_Scheduler",
      "args": [],
      "description": "Automated backups (FTP/local) – scheduled and manual."
    },
    {
      "id": "server_health",
      "name": "AutomationZ Server Health",
      "type": "python",
      "entry": "../AutomationZ_Server_Health/app/main.py",
      "cwd": "../AutomationZ_Server_Health",
      "args": [],
      "description": "Health checks for servers (pings, endpoints, warning alerts)."
    },
    {
      "id": "admin_orchestrator",
      "name": "AutomationZ Admin Orchestrator",
      "type": "python",
      "entry": "../AutomationZ_Admin_Orchestrator/app/main.py",
      "cwd": "../AutomationZ_Admin_Orchestrator",
      "args": [],
      "description": "Plans + mappings + profiles, push presets to targets, optional restart + verify."
    },
    {
      "id": "log_cleanup",
      "name": "AutomationZ Log Cleanup Scheduler",
      "type": "python",
      "entry": "../AutomationZ_Log_Cleanup_Scheduler/app/main.py",
      "cwd": "../AutomationZ_Log_Cleanup_Scheduler",
      "args": [],
      "description": "Delete log-folder contents on a schedule (local + FTP), with exclusion rules."
    }
  ]
}

def ensure_dirs():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

def load_tools() -> Dict[str, Any]:
    if not CONFIG_PATH.exists():
        save_tools(DEFAULT_TOOLS)
        return DEFAULT_TOOLS
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception:
        return DEFAULT_TOOLS

def save_tools(obj: Dict[str, Any]) -> None:
    CONFIG_PATH.write_text(json.dumps(obj, indent=2), encoding="utf-8")

def open_path(path: pathlib.Path) -> None:
    p = str(path)
    if sys.platform.startswith("win"):
        os.startfile(p)  # type: ignore
    elif sys.platform == "darwin":
        os.system(f'open "{p}"')
    else:
        os.system(f'xdg-open "{p}"')

def abs_path(rel_or_abs: str) -> pathlib.Path:
    p = pathlib.Path(rel_or_abs)
    if p.is_absolute():
        return p
    return (BASE_DIR / p).resolve()

@dataclass
class ToolItem:
    id: str
    name: str
    type: str        # python | exe | command
    entry: str
    cwd: str = ""
    args: List[str] = None  # type: ignore
    description: str = ""

    def __post_init__(self):
        if self.args is None:
            self.args = []

def apply_dark_theme(root: tk.Tk) -> ttk.Style:
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    root.configure(bg=C_BG)

    style.configure(".", background=C_BG, foreground=C_TEXT)
    style.configure("TFrame", background=C_BG)
    style.configure("TLabel", background=C_BG, foreground=C_TEXT)
    style.configure("TLabelFrame", background=C_BG, foreground=C_TEXT)
    style.configure("TLabelFrame.Label", background=C_BG, foreground=C_TEXT)

    style.configure("TButton", background=C_PANEL, foreground=C_TEXT, borderwidth=1, focusthickness=2, focuscolor=C_ACCENT)
    style.map("TButton",
              background=[("active", "#3a3a3a"), ("pressed", "#3f3f3f")],
              foreground=[("disabled", C_MUTED)])

    style.configure("TEntry", fieldbackground=C_PANEL, background=C_PANEL, foreground=C_TEXT, insertcolor=C_TEXT)
    style.configure("TCombobox", fieldbackground=C_PANEL, background=C_PANEL, foreground=C_TEXT, arrowcolor=C_TEXT)
    style.map("TCombobox",
              fieldbackground=[("readonly", C_PANEL)],
              background=[("readonly", C_PANEL)],
              foreground=[("readonly", C_TEXT)])

    style.configure("Treeview",
                    background=C_PANEL,
                    fieldbackground=C_PANEL,
                    foreground=C_TEXT,
                    bordercolor="#1f1f1f",
                    rowheight=24)
    style.map("Treeview",
              background=[("selected", "#1f3b2b")],
              foreground=[("selected", "#ffffff")])
    style.configure("Treeview.Heading",
                    background="#242424",
                    foreground=C_TEXT,
                    relief="flat")
    style.map("Treeview.Heading",
              background=[("active", "#2d2d2d")])

    style.configure("TSeparator", background="#1f1f1f")
    return style

def style_text_widget(txt: tk.Text) -> None:
    txt.configure(
        bg=C_PANEL,
        fg=C_TEXT,
        insertbackground=C_TEXT,
        selectbackground="#1f3b2b",
        selectforeground="#ffffff",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#1f1f1f",
        highlightcolor=C_ACCENT,
        bd=0
    )

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry("980x640")
        self.minsize(900, 560)

        ensure_dirs()
        self.style = apply_dark_theme(self)

        self._img_logo: Optional[tk.PhotoImage] = None
        self._img_bg: Optional[tk.PhotoImage] = None

        # running processes by tool id
        self._procs: Dict[str, subprocess.Popen] = {}

        self.tools_raw = load_tools()
        self.tools: List[ToolItem] = self._parse_tools(self.tools_raw)

        self._build_ui()
        self._refresh_list()

        # periodic refresh of running state indicators
        self.after(1000, self._tick_processes)

    def _parse_tools(self, obj: Dict[str, Any]) -> List[ToolItem]:
        out: List[ToolItem] = []
        for t in obj.get("tools", []):
            out.append(ToolItem(
                id=str(t.get("id", "")),
                name=str(t.get("name", "")),
                type=str(t.get("type", "python")),
                entry=str(t.get("entry", "")),
                cwd=str(t.get("cwd", "")),
                args=list(t.get("args", []) or []),
                description=str(t.get("description", "")),
            ))
        return out

    def _try_load_assets(self) -> None:
        bg_path = ASSETS_DIR / "bg.png"
        if bg_path.exists():
            try:
                self._img_bg = tk.PhotoImage(file=str(bg_path))
                self._bg_label.configure(image=self._img_bg)
            except Exception:
                self._img_bg = None

        logo_path = ASSETS_DIR / "logo.png"
        if logo_path.exists():
            try:
                self._img_logo = tk.PhotoImage(file=str(logo_path))
                self._logo_label.configure(image=self._img_logo)
            except Exception:
                self._img_logo = None

    def _build_ui(self):
        self._bg_label = tk.Label(self, bg=C_BG, bd=0, highlightthickness=0)
        self._bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        container = ttk.Frame(self)
        container.place(x=0, y=0, relwidth=1, relheight=1)

        header = ttk.Frame(container)
        header.pack(fill="x", padx=12, pady=(12, 6))

        header_bg = tk.Frame(header, bg=C_PANEL, bd=0, highlightthickness=0)
        header_bg.pack(fill="x")

        self._logo_label = tk.Label(header_bg, bg=C_PANEL)
        self._logo_label.pack(side="left", padx=(10, 8), pady=8)

        title_box = tk.Frame(header_bg, bg=C_PANEL)
        title_box.pack(side="left", fill="x", expand=True)

        tk.Label(title_box, text=APP_NAME, bg=C_PANEL, fg=C_TEXT, font=("TkDefaultFont", 14, "bold")).pack(anchor="w")
        tk.Label(title_box, text=f"v{APP_VERSION}", bg=C_PANEL, fg=C_MUTED).pack(anchor="w")

        top = ttk.Frame(container)
        top.pack(fill="x", padx=12, pady=(0, 10))

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Colored.TButton",
            foreground="white",
            background=C_ACCENT,
            padding=(10, 6),
            font=("Helvetica", 10, "bold")
        )
        style.map(
            "Colored.TButton",
            background=[
                ("active", "#66BB6A"),
                ("pressed", "#388E3C"),
                ("disabled", "#555555"),
            ],
            foreground=[
                ("disabled", "#aaaaaa"),
            ]
        )

        ttk.Label(top, text="Tools").pack(side="left")
        ttk.Button(top, text="Refresh", command=self._reload, style="Colored.TButton").pack(side="left", padx=8)
        ttk.Button(top, text="Manage Tools", command=self._manage_tools, style="Colored.TButton").pack(side="left")
        ttk.Button(top, text="Edit tools.json", command=self._open_tools_json, style="Colored.TButton").pack(side="left", padx=8)
        ttk.Button(top, text="Open Logs", command=lambda: self._open_safe(LOGS_DIR), style="Colored.TButton").pack(side="left")
        ttk.Button(top, text="INFO", command=self._about, style="Colored.TButton").pack(side="right")
        ttk.Button(top, text="Contact", command=self._contact, style="Colored.TButton").pack(side="right", padx=8)

        main = ttk.Frame(container)
        main.pack(fill="both", expand=True, padx=12, pady=(0,12))

        left = ttk.LabelFrame(main, text="List")
        left.pack(side="left", fill="both", expand=False)

        self.tree = ttk.Treeview(left, columns=("status",), show="tree headings", height=20)
        self.tree.heading("#0", text="Name")
        self.tree.heading("status", text="Status")
        self.tree.column("#0", width=340)
        self.tree.column("status", width=160, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)
        self.tree.bind("<<TreeviewSelect>>", lambda e: self._on_select())

        btns = ttk.Frame(left)
        btns.pack(fill="x", padx=8, pady=(0,8))
        ttk.Button(btns, text="Launch", command=self._launch_selected, style="Colored.TButton").pack(side="left")
        ttk.Button(btns, text="Open Tool Folder", command=self._open_selected_folder, style="Colored.TButton").pack(side="left", padx=8)

        right = ttk.LabelFrame(main, text="Details")
        right.pack(side="left", fill="both", expand=True, padx=(12,0))

        self.lbl_name = ttk.Label(right, text="", font=("TkDefaultFont", 12, "bold"))
        self.lbl_name.pack(anchor="w", padx=10, pady=(10,4))

        self.txt_desc = tk.Text(right, height=9, wrap="word")
        self.txt_desc.pack(fill="x", padx=10, pady=(0,8))
        style_text_widget(self.txt_desc)
        self.txt_desc.configure(state="disabled")

        self.lbl_path = ttk.Label(right, text="")
        self.lbl_path.pack(anchor="w", padx=10)

        self.lbl_cwd = ttk.Label(right, text="")
        self.lbl_cwd.pack(anchor="w", padx=10, pady=(2,0))

        logf = ttk.LabelFrame(right, text="Status / Output")
        logf.pack(fill="both", expand=True, padx=10, pady=10)
        self.log = tk.Text(logf, wrap="word", height=10, state="disabled")
        self.log.pack(fill="both", expand=True, padx=8, pady=8)
        style_text_widget(self.log)

        bottom = ttk.Frame(container)
        bottom.pack(fill="x", padx=12, pady=(0,10))
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(bottom, textvariable=self.status_var).pack(side="left")

        author = tk.Label(
            bottom,
            text="Created by Danny van den Brande",
            fg=C_ACCENT,
            bg=C_BG,
            cursor="hand2",
            font=("Segoe UI", 9)
        )
        author.pack(side="right")
        author.bind("<Button-1>", self._open_author)

        self._try_load_assets()

    # ---------- Polished About / Contact ----------

    def _open_url(self, url: str) -> None:
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Open link failed", str(e))

    def _copy_text(self, text: str) -> None:
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.update_idletasks()
        except Exception as e:
            messagebox.showerror("Copy failed", str(e))

    def _make_link_row(self, parent: tk.Widget, label: str, value: str, url: Optional[str] = None):
        row = tk.Frame(parent, bg=C_PANEL)
        row.pack(fill="x", pady=4)

        tk.Label(row, text=label, bg=C_PANEL, fg=C_MUTED, width=10, anchor="w").pack(side="left")
        link = tk.Label(row, text=value, bg=C_PANEL, fg=C_ACCENT, cursor="hand2", anchor="w", font=("Segoe UI", 10, "underline"))
        link.pack(side="left", fill="x", expand=True)
        if url:
            link.bind("<Button-1>", lambda e: self._open_url(url))
        else:
            link.bind("<Button-1>", lambda e: self._copy_text(value))

        btns = tk.Frame(row, bg=C_PANEL)
        btns.pack(side="right")
        if url:
            ttk.Button(btns, text="Open", command=lambda: self._open_url(url)).pack(side="left", padx=4)
        ttk.Button(btns, text="Copy", command=lambda: self._copy_text(value)).pack(side="left")

    def _about(self):
        win = tk.Toplevel(self)
        win.title("About")
        w, h = 520, 320
        win.geometry(f"{w}x{h}")
        self._center_window(win, w, h)

        win.resizable(False, False)
        win.transient(self)
        win.grab_set()
        win.configure(bg=C_BG)

        wrap = tk.Frame(win, bg=C_PANEL, padx=16, pady=16)
        wrap.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(wrap, text=f"{APP_NAME}", bg=C_PANEL, fg=C_TEXT, font=("Segoe UI", 14, "bold")).pack(anchor="w")
        tk.Label(wrap, text=f"Version {APP_VERSION}", bg=C_PANEL, fg=C_MUTED).pack(anchor="w", pady=(0, 10))

        tk.Label(
            wrap,
            text="A unified launcher for the AutomationZ toolchain.\nManage tools, launch scripts, and keep everything organized.",
            bg=C_PANEL, fg=C_TEXT, justify="left"
        ).pack(anchor="w", pady=(0, 12))

        self._make_link_row(wrap, "GitHub", "github.com/DayZ-AutomationZ", "https://github.com/DayZ-AutomationZ")
        self._make_link_row(wrap, "Ko‑fi", "ko-fi.com/dannyvandenbrande", "https://ko-fi.com/dannyvandenbrande")

        # Footer actions
        actions = tk.Frame(win, bg=C_BG)
        actions.pack(fill="x", padx=12, pady=(0, 12))
        ttk.Button(actions, text="Open GitHub", command=lambda: self._open_url("https://github.com/DayZ-AutomationZ")).pack(side="left")
        ttk.Button(actions, text="Close", command=win.destroy).pack(side="right")

    def _contact(self):
        win = tk.Toplevel(self)
        win.title("Contact")
        w, h = 520, 340
        win.geometry(f"{w}x{h}")
        self._center_window(win, w, h)

        win.resizable(False, False)
        win.transient(self)
        win.grab_set()
        win.configure(bg=C_BG)

        wrap = tk.Frame(win, bg=C_PANEL, padx=16, pady=16)
        wrap.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(wrap, text="Contact", bg=C_PANEL, fg=C_TEXT, font=("Segoe UI", 14, "bold")).pack(anchor="w")
        tk.Label(wrap, text="Get in touch or support the project:", bg=C_PANEL, fg=C_TEXT).pack(anchor="w", pady=(0, 10))

        email = "dannyautomationz@gmail.com"
        self._make_link_row(wrap, "Email", email, None)
        self._make_link_row(wrap, "GitHub", "github.com/DayZ-AutomationZ", "https://github.com/DayZ-AutomationZ")
        self._make_link_row(wrap, "Ko‑fi", "ko-fi.com/dannyvandenbrande", "https://ko-fi.com/dannyvandenbrande")

        actions = tk.Frame(win, bg=C_BG)
        actions.pack(fill="x", padx=12, pady=(0, 12))
        ttk.Button(actions, text="Copy email", command=lambda: self._copy_text(email)).pack(side="left")
        ttk.Button(actions, text="Open GitHub", command=lambda: self._open_url("https://github.com/DayZ-AutomationZ")).pack(side="left", padx=8)
        ttk.Button(actions, text="Close", command=win.destroy).pack(side="right")

    def _center_window(self, win: tk.Toplevel, w: int, h: int):
        # centers 'win' on the main app window (self)
        self.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (w // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (h // 2)
        win.geometry(f"{w}x{h}+{x}+{y}")

    # ---------- existing features ----------

    def _open_author(self, event=None):
        self._open_url("https://github.com/DayZ-AutomationZ")

    def _manage_tools(self):
        """Built-in editor for tools.json (no external dependencies)."""
        win = tk.Toplevel(self)
        win.title("Manage Tools")
        win.geometry("1245x725")
        win.minsize(820, 480)
        win.configure(bg=C_BG)
        win.transient(self)
        win.grab_set()

        data = {"tools": [t for t in (self.tools_raw.get("tools", []) or [])]}

        root = ttk.Frame(win)
        root.pack(fill="both", expand=True, padx=12, pady=12)

        left = ttk.LabelFrame(root, text="Tools")
        left.pack(side="left", fill="both", expand=False)

        cols = ("type", "entry")
        tree = ttk.Treeview(left, columns=cols, show="headings", height=18)
        tree.heading("type", text="Type")
        tree.heading("entry", text="Entry")
        tree.column("type", width=90, anchor="center")
        tree.column("entry", width=360)
        tree.pack(fill="both", expand=True, padx=8, pady=8)

        btns = ttk.Frame(left)
        btns.pack(fill="x", padx=8, pady=(0, 8))

        right = ttk.LabelFrame(root, text="Edit selected")
        right.pack(side="left", fill="both", expand=True, padx=(12, 0))

        form = ttk.Frame(right)
        form.pack(fill="both", expand=True, padx=10, pady=10)

        v_id = tk.StringVar()
        v_name = tk.StringVar()
        v_type = tk.StringVar(value="python")
        v_entry = tk.StringVar()
        v_cwd = tk.StringVar()
        v_args = tk.StringVar()

        def row(label, var, r, w=56):
            ttk.Label(form, text=label).grid(row=r, column=0, sticky="w", pady=3)
            e = ttk.Entry(form, textvariable=var, width=w)
            e.grid(row=r, column=1, sticky="w", pady=3)
            return e

        r = 0
        row("id", v_id, r); r += 1
        row("name", v_name, r); r += 1

        ttk.Label(form, text="type").grid(row=r, column=0, sticky="w", pady=3)
        ttk.Combobox(form, textvariable=v_type, state="readonly", values=["python","exe","command"], width=18).grid(row=r, column=1, sticky="w", pady=3)
        r += 1

        row("entry", v_entry, r); r += 1
        row("cwd (optional)", v_cwd, r); r += 1
        row("args (comma-separated)", v_args, r); r += 1

        ttk.Label(form, text="description").grid(row=r, column=0, sticky="nw", pady=3)
        txt_desc = tk.Text(form, height=6, width=56, wrap="word")
        txt_desc.grid(row=r, column=1, sticky="w", pady=3)
        style_text_widget(txt_desc)
        r += 1

        ttk.Label(form, text="Tip: entry/cwd are relative to this app folder.", foreground=C_MUTED).grid(row=r, column=1, sticky="w", pady=(6, 0))

        sel_idx: Optional[int] = None

        def refresh_tree(select_index: Optional[int] = None):
            for item in tree.get_children():
                tree.delete(item)
            for i, t in enumerate(data["tools"]):
                tree.insert("", "end", iid=str(i), values=(t.get("type","python"), t.get("entry","")))
            if select_index is not None and str(select_index) in tree.get_children():
                tree.selection_set(str(select_index))
                tree.see(str(select_index))
                on_select()

        def load_form(i: int):
            t = data["tools"][i]
            v_id.set(str(t.get("id","")))
            v_name.set(str(t.get("name","")))
            v_type.set(str(t.get("type","python")))
            v_entry.set(str(t.get("entry","")))
            v_cwd.set(str(t.get("cwd","")))
            v_args.set(", ".join(list(t.get("args", []) or [])))
            txt_desc.delete("1.0", "end")
            txt_desc.insert("1.0", str(t.get("description","")))

        def on_select(event=None):
            nonlocal sel_idx
            sel = tree.selection()
            if not sel:
                sel_idx = None
                return
            sel_idx = int(sel[0])
            load_form(sel_idx)

        tree.bind("<<TreeviewSelect>>", on_select)

        def add_new():
            data["tools"].append({
                "id": f"tool_{len(data['tools'])+1}",
                "name": "New Tool",
                "type": "python",
                "entry": "",
                "cwd": "",
                "args": [],
                "description": ""
            })
            refresh_tree(len(data["tools"]) - 1)

        def delete_sel():
            nonlocal sel_idx
            if sel_idx is None:
                return
            if not messagebox.askyesno("Delete", "Delete selected tool?", parent=win):
                return
            del data["tools"][sel_idx]
            sel_idx = 0 if data["tools"] else None
            refresh_tree(sel_idx)

        def move(delta: int):
            nonlocal sel_idx
            if sel_idx is None:
                return
            j = sel_idx + delta
            if j < 0 or j >= len(data["tools"]):
                return
            data["tools"][sel_idx], data["tools"][j] = data["tools"][j], data["tools"][sel_idx]
            sel_idx = j
            refresh_tree(sel_idx)

        def apply_changes():
            if sel_idx is None:
                return
            t = data["tools"][sel_idx]
            t["id"] = (v_id.get() or "").strip()
            t["name"] = (v_name.get() or "").strip()
            t["type"] = (v_type.get() or "python").strip()
            t["entry"] = (v_entry.get() or "").strip()
            t["cwd"] = (v_cwd.get() or "").strip()
            t["args"] = [a.strip() for a in (v_args.get() or "").split(",") if a.strip()]
            t["description"] = txt_desc.get("1.0", "end").strip()
            refresh_tree(sel_idx)

        def save_and_close():
            for t in data["tools"]:
                if not (t.get("id") or "").strip():
                    messagebox.showerror("Invalid", "Every tool must have an id.", parent=win)
                    return
                if not (t.get("name") or "").strip():
                    messagebox.showerror("Invalid", "Every tool must have a name.", parent=win)
                    return
                if t.get("type") not in ("python","exe","command"):
                    messagebox.showerror("Invalid", "Type must be python/exe/command.", parent=win)
                    return
            save_tools(data)
            self.tools_raw = load_tools()
            self.tools = self._parse_tools(self.tools_raw)
            self._refresh_list()
            self._log("Updated tools.json via Manage Tools")
            win.destroy()

        ttk.Button(btns, text="Add", command=add_new, style="Colored.TButton").pack(side="left")
        ttk.Button(btns, text="Delete", command=delete_sel, style="Colored.TButton").pack(side="left", padx=6)
        ttk.Button(btns, text="Up", command=lambda: move(-1), style="Colored.TButton").pack(side="left", padx=6)
        ttk.Button(btns, text="Down", command=lambda: move(1), style="Colored.TButton").pack(side="left")

        actions = ttk.Frame(right)
        actions.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(actions, text="Apply change (stage)", command=apply_changes, style="Colored.TButton").pack(side="left")
        ttk.Button(actions, text="Save tools.json (commit)", command=save_and_close, style="Colored.TButton").pack(side="left", padx=8)
        ttk.Button(actions, text="Cancel", command=win.destroy, style="Colored.TButton").pack(side="right")

        refresh_tree(0 if data["tools"] else None)

    def _open_safe(self, p: pathlib.Path):
        try:
            open_path(p)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _log(self, msg: str):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

        try:
            lf = LOGS_DIR / "control_center.log"
            with open(lf, "a", encoding="utf-8") as f:
                f.write(msg + "\n")
        except Exception:
            pass

    def _reload(self):
        self.tools_raw = load_tools()
        self.tools = self._parse_tools(self.tools_raw)
        self._refresh_list()
        self._log("Reloaded tools.json")
        self.status_var.set("Reloaded.")

    def _open_tools_json(self):
        if not CONFIG_PATH.exists():
            save_tools(DEFAULT_TOOLS)
        self._open_safe(CONFIG_PATH)

    def _tool_status(self, t: ToolItem) -> str:
        p = self._procs.get(t.id)
        if p is not None and p.poll() is None:
            return "🟡 Running"

        entry = abs_path(t.entry)
        if t.type in ("python", "exe"):
            return "🟢 Ready" if entry.exists() else "🔴 Missing"

        if t.type == "command":
            return "🟢 Ready"
        return "?"

    def _refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for idx, t in enumerate(self.tools):
            status = self._tool_status(t)
            self.tree.insert("", "end", iid=str(idx), text=t.name, values=(status,))

        if self.tools:
            self.tree.selection_set("0")
            self._on_select()

    def _tick_processes(self):
        changed = False
        for tid, proc in list(self._procs.items()):
            if proc.poll() is not None:
                del self._procs[tid]
                changed = True

        for idx, t in enumerate(self.tools):
            iid = str(idx)
            if iid in self.tree.get_children():
                self.tree.set(iid, "status", self._tool_status(t))

        if changed:
            self.status_var.set("Ready.")
        self.after(1000, self._tick_processes)

    def _selected_tool(self) -> Optional[ToolItem]:
        sel = self.tree.selection()
        if not sel:
            return None
        try:
            idx = int(sel[0])
            return self.tools[idx]
        except Exception:
            return None

    def _on_select(self):
        t = self._selected_tool()
        if not t:
            return

        self.lbl_name.configure(text=t.name)

        self.txt_desc.configure(state="normal")
        self.txt_desc.delete("1.0", "end")
        self.txt_desc.insert("1.0", t.description or "(no description)")
        self.txt_desc.configure(state="disabled")

        self.lbl_path.configure(text=f"Entry: {abs_path(t.entry)}")
        self.lbl_cwd.configure(text=f"CWD:   {abs_path(t.cwd) if t.cwd else '(default)'}")

        self.status_var.set("Ready.")

    def _open_selected_folder(self):
        t = self._selected_tool()
        if not t:
            return
        p = abs_path(t.cwd) if t.cwd else abs_path(t.entry).parent
        self._open_safe(p)

    def _launch_selected(self):
        t = self._selected_tool()
        if not t:
            messagebox.showwarning("No selection", "Select a tool first.")
            return

        try:
            cmd, cwd = self._build_cmd(t)
            self._log(f"Launching: {t.name}")
            self._log("CMD: " + " ".join(cmd))
            if cwd:
                self._log("CWD: " + str(cwd))
            proc = subprocess.Popen(cmd, cwd=str(cwd) if cwd else None)
            self._procs[t.id] = proc
            self.status_var.set(f"Launched: {t.name}")
            self._tick_processes()
        except Exception as e:
            self._log("ERROR: " + str(e))
            self._log(traceback.format_exc())
            messagebox.showerror("Launch failed", str(e))
            self.status_var.set("Launch failed.")

    def _build_cmd(self, t: ToolItem):
        entry = abs_path(t.entry)
        cwd = abs_path(t.cwd) if t.cwd else None

        if t.type == "python":
            if not entry.exists():
                raise RuntimeError(f"Entry script not found: {entry}")
            cmd = [sys.executable, str(entry)] + list(t.args or [])
            return cmd, cwd

        if t.type == "exe":
            if not entry.exists():
                raise RuntimeError(f"Executable not found: {entry}")
            cmd = [str(entry)] + list(t.args or [])
            return cmd, cwd

        if t.type == "command":
            cmd = [t.entry] + list(t.args or [])
            return cmd, cwd

        raise RuntimeError(f"Unknown tool type: {t.type}")

def main():
    App().mainloop()

if __name__ == "__main__":
    main()
