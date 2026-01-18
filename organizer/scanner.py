import os

def scan_files(base_path: str):
    """
    Safely scans files inside the given directory.
    READ-ONLY operation.
    Returns a list of file metadata dictionaries.
    """

    scanned_files = []

    for root, dirs, files in os.walk(base_path):

        # 🔐 Skip hidden/system directories
        dirs[:] = [
            d for d in dirs
            if not d.startswith(".")
        ]

        for file in files:
            # 🔐 Skip hidden/system files
            if file.startswith("."):
                continue

            full_path = os.path.join(root, file)

            try:
                # READ-ONLY metadata
                file_info = {
                    "name": file,
                    "path": full_path,
                    "size": os.path.getsize(full_path),
                    "extension": os.path.splitext(file)[1].lower()
                }

                scanned_files.append(file_info)

            except (PermissionError, FileNotFoundError):
                # 🔐 Skip files we cannot safely read
                continue

    return scanned_files
