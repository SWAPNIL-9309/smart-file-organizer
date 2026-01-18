import os

# ❌ Absolute paths that should NEVER be touched
BLOCKED_PATH_KEYWORDS = [
    "windows",
    "program files",
    "program files (x86)",
    "system32"
]

def is_safe_path(path: str) -> bool:
    """
    Checks whether the given path is safe to operate on.
    Blocks system directories and root-level paths.
    """

    # Convert to absolute normalized path
    path = os.path.abspath(path)
    path_lower = path.lower()

    # 1️⃣ Block Windows system directories
    for keyword in BLOCKED_PATH_KEYWORDS:
        if keyword in path_lower:
            return False

    # 2️⃣ Block root directories like C:\ or D:\
    drive, tail = os.path.splitdrive(path)
    if drive and tail in ["\\", "/"]:
        return False

    # 3️⃣ Path must exist
    if not os.path.exists(path):
        return False

    # 4️⃣ Must be a directory
    if not os.path.isdir(path):
        return False

    return True

