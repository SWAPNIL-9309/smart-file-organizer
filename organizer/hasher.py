import hashlib

def get_file_hash(file_path: str, chunk_size: int = 8192):
    """
    Safely generates SHA-256 hash of a file.
    Reads file in chunks to avoid memory issues.
    READ-ONLY operation.
    """

    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                sha256.update(chunk)

        return sha256.hexdigest()

    except (PermissionError, FileNotFoundError, OSError):
        # 🔐 If file cannot be safely read, skip it
        return None
