import argparse
import os

from utils.validator import is_safe_path
from organizer.scanner import scan_files
from organizer.hasher import get_file_hash
from organizer.duplicate_finder import find_duplicates
from utils.prompts import suggest_duplicates_action
from organizer.organizer import organize_files_preview


def main():
    parser = argparse.ArgumentParser(
        description="Smart File Organizer + Duplicate Detector (SAFE MODE)"
    )

    parser.add_argument(
        "--path",
        required=True,
        help="Path to folder to scan (recommended: test_data)"
    )

    parser.add_argument(
        "--organize",
        action="store_true",
        help="Preview file organization by type (dry-run only)"
    )

    parser.add_argument(
        "--duplicates",
        action="store_true",
        help="Find duplicate files (no deletion)"
    )

    args = parser.parse_args()
    target_path = os.path.abspath(args.path)

    print("\n🔐 SAFE MODE ENABLED")
    print(f"📂 Target Path: {target_path}")

    # ---------------- SECURITY CHECK ----------------
    if not is_safe_path(target_path):
        print("❌ ERROR: Unsafe or invalid path.")
        print("This tool cannot run on system or root directories.")
        return

    print("🧪 DRY-RUN MODE (no files will be modified)\n")

    # ---------------- SCAN FILES ----------------
    files = scan_files(target_path)
    print(f"📄 Files scanned: {len(files)}")

    if not files:
        print("⚠️ No files found.")
        return

    # ---------------- ORGANIZE PREVIEW ----------------
    if args.organize:
        print("\n📁 File Organization Preview:")
        actions = organize_files_preview(files, target_path)

        if not actions:
            print("✔ Files already organized.")
        else:
            for a in actions:
                print(f"[DRY-RUN] {a['from']} → {a['to']}")

    # ---------------- DUPLICATE DETECTION ----------------
    if args.duplicates:
        duplicates = find_duplicates(files)

        print(f"\n🔁 Duplicate Groups Found: {len(duplicates)}")

        if duplicates:
            suggestions = suggest_duplicates_action(duplicates)

            for s in suggestions:
                print("\n✅ Suggested KEEP:")
                print(f"   {s['keep']['path']}")

                print("🗑️ Suggested DELETE (optional):")
                for f in s["delete"]:
                    print(f"   {f['path']}")
        else:
            print("✔ No duplicates found.")

    print("\n✅ Operation completed safely.")


if __name__ == "__main__":
    main()
