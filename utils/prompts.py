import os

def suggest_duplicates_action(duplicate_groups):
    """
    Suggests which file to keep and which can be deleted.
    DOES NOT perform any delete.
    """

    suggestions = []

    for file_hash, files in duplicate_groups.items():

        # Sort by path length (shorter path = usually original)
        sorted_files = sorted(
            files,
            key=lambda f: (f["size"], len(f["path"]))
        )

        keep_file = sorted_files[0]
        delete_candidates = sorted_files[1:]

        suggestions.append({
            "hash": file_hash,
            "keep": keep_file,
            "delete": delete_candidates
        })

    return suggestions
