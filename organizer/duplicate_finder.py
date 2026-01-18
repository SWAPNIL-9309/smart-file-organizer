from organizer.hasher import get_file_hash

def find_duplicates(files):
    """
    Detects duplicate files based on content hash.
    READ-ONLY operation.
    
    Input: list of file metadata (from scanner)
    Output: dict -> hash : list of files with same content
    """

    hash_map = {}

    for file in files:
        file_path = file["path"]

        file_hash = get_file_hash(file_path)

        # 🔐 Skip files that couldn't be hashed safely
        if not file_hash:
            continue

        if file_hash not in hash_map:
            hash_map[file_hash] = []

        hash_map[file_hash].append(file)

    # Keep only hashes with duplicates
    duplicates = {
        h: flist for h, flist in hash_map.items()
        if len(flist) > 1
    }

    return duplicates
