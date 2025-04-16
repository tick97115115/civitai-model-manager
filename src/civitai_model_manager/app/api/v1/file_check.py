from blake3 import blake3

def blake3_hash(file_path: str) -> bytes:
    file_hasher = blake3(max_threads=blake3.AUTO)
    file_hasher.update_mmap(file_path)
    return file_hasher.digest()

if __name__ == "__main__":
    hash_data = blake3_hash(r"C:\Users\z005223c\Downloads\debian-12.10.0-amd64-DVD-1.iso")
    print(hash_data.hex())