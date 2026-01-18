import os

# File type mapping
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Music": [".mp3", ".wav"],
}

def get_category(extension: str) -> str:
    for category, exts in FILE_CATEGORIES.items():
        if extension in exts:
            return category
    return "Others"


def organize_files_preview(files, base_path):
    """
    DRY-RUN ONLY
    Shows how files would be organized by type.
    DOES NOT move any file.
    """

    actions = []

    for file in files:
        category = get_category(file["extension"])
        target_dir = os.path.join(base_path, category)
        target_path = os.path.join(target_dir, file["name"])

        # Skip if already in correct folder
        if file["path"] == target_path:
            continue

        actions.append({
            "from": file["path"],
            "to": target_path,
            "category": category
        })

    return actions
