import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import os

# ---- Import SAFE backend logic ----
from utils.validator import is_safe_path
from organizer.scanner import scan_files
from organizer.organizer import organize_files_preview
from organizer.duplicate_finder import find_duplicates
from utils.prompts import suggest_duplicates_action


def main():
    root = tk.Tk()
    root.title("Smart File Organizer & Duplicate Detector (SAFE MODE)")
    root.geometry("800x600")
    root.resizable(False, False)

    selected_path = tk.StringVar(value="No folder selected")

    # ---------------- HEADER ----------------
    tk.Label(
        root,
        text="Smart File Organizer & Duplicate Detector",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    tk.Label(
        root,
        text="🔐 SAFE MODE ENABLED — No files will be moved or deleted",
        fg="green",
        font=("Arial", 10, "bold")
    ).pack(pady=5)

    # ---------------- PATH DISPLAY ----------------
    tk.Label(
        root,
        textvariable=selected_path,
        wraplength=760,
        fg="blue"
    ).pack(pady=5)

    # ---------------- OUTPUT AREA ----------------
    output = ScrolledText(
        root,
        height=20,
        width=95,
        state="disabled",
        wrap="word"
    )
    output.pack(padx=10, pady=10)

    def log(msg):
        output.config(state="normal")
        output.insert(tk.END, msg + "\n")
        output.see(tk.END)
        output.config(state="disabled")

    def clear_output():
        output.config(state="normal")
        output.delete("1.0", tk.END)
        output.config(state="disabled")

    # ---------------- FOLDER PICKER ----------------
    def choose_folder():
        folder = filedialog.askdirectory(title="Select Folder (Safe)")
        if folder:
            selected_path.set(folder)
            clear_output()
            log(f"📂 Folder selected: {folder}")
            log("ℹ️ Ready for safe operations.")
        else:
            selected_path.set("No folder selected")
            log("⚠️ No folder selected.")

    # ---------------- SAFE VALIDATION ----------------
    def validate_path():
        path = selected_path.get()
        if not path or path == "No folder selected":
            messagebox.showerror("Error", "Please select a folder first.")
            return None

        if not is_safe_path(path):
            messagebox.showerror(
                "Unsafe Path",
                "System or root directories are blocked.\n"
                "Please select a safe test folder."
            )
            return None

        return path

    # ---------------- SCAN FILES ----------------
    def scan_action():
        path = validate_path()
        if not path:
            return

        clear_output()
        log("🔍 Scanning files (read-only)...")

        files = scan_files(path)
        log(f"📄 Files scanned: {len(files)}")

        if not files:
            log("⚠️ No files found.")
            return

        for f in files[:10]:
            log(f" - {f['path']}")

        if len(files) > 10:
            log("... (output truncated for readability)")

    # ---------------- ORGANIZE PREVIEW ----------------
    def organize_action():
        path = validate_path()
        if not path:
            return

        clear_output()
        log("📁 Organization Preview (DRY-RUN):")

        files = scan_files(path)
        actions = organize_files_preview(files, path)

        if not actions:
            log("✔ Files already appear organized.")
            return

        for a in actions:
            log(f"[DRY-RUN] {a['from']} → {a['to']}")

    # ---------------- DUPLICATE DETECTION ----------------
    def duplicate_action():
        path = validate_path()
        if not path:
            return

        clear_output()
        log("🔁 Detecting duplicates (hash-based, read-only)...")

        files = scan_files(path)
        duplicates = find_duplicates(files)

        log(f"🔎 Duplicate groups found: {len(duplicates)}")

        if not duplicates:
            log("✔ No duplicates found.")
            return

        suggestions = suggest_duplicates_action(duplicates)

        for s in suggestions:
            log("\n✅ Suggested KEEP:")
            log(f"   {s['keep']['path']}")

            log("🗑️ Suggested DELETE (optional):")
            for f in s["delete"]:
                log(f"   {f['path']}")

    # ---------------- BUTTONS ----------------
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(
        btn_frame, text="📂 Select Folder",
        width=18, command=choose_folder
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        btn_frame, text="🔍 Scan Files",
        width=18, command=scan_action
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        btn_frame, text="📁 Organize Preview",
        width=18, command=organize_action
    ).grid(row=0, column=2, padx=5)

    tk.Button(
        btn_frame, text="🔁 Find Duplicates",
        width=18, command=duplicate_action
    ).grid(row=0, column=3, padx=5)

    root.mainloop()


if __name__ == "__main__":
    main()
