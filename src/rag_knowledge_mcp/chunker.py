import os
from pathlib import Path
from typing import List, Dict, Any


class DocumentChunker:
    """
    Reads markdown and text documentation files and breaks them into overlapping text chunks with source metadata.
    """

    SUPPORTED_EXTENSIONS = {".md", ".markdown", ".txt", ".rst", ".json"}

    def __init__(self, chunk_size: int = 400, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def process_directory(self, target_dir: str) -> List[Dict[str, Any]]:
        """
        Recursively scans target_dir for documentation files and returns list of chunk dictionaries.
        """
        resolved_dir = Path(target_dir).resolve()
        if not resolved_dir.exists():
            raise FileNotFoundError(f"Target directory does not exist: {target_dir}")
        if not resolved_dir.is_dir():
            raise NotADirectoryError(f"Target path is not a directory: {target_dir}")

        all_chunks = []

        for root, _, files in os.walk(resolved_dir):
            for file_name in files:
                file_path = Path(root) / file_name
                if file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                    try:
                        chunks = self.chunk_file(file_path)
                        all_chunks.extend(chunks)
                    except Exception:
                        pass

        return all_chunks

    def chunk_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Splits a single file into text chunks.
        """
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        if not content.strip():
            return []

        # Split content into paragraphs or line segments
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        chunks = []
        chunk_idx = 0

        for para in paragraphs:
            # If paragraph is within limit, use as a single chunk
            if len(para) <= self.chunk_size:
                chunks.append({
                    "chunk_id": f"{file_path.name}#chunk_{chunk_idx}",
                    "file_name": file_path.name,
                    "file_path": str(file_path),
                    "text": para,
                    "length": len(para),
                })
                chunk_idx += 1
            else:
                # Sliding window chunking for long paragraphs
                start = 0
                while start < len(para):
                    end = min(start + self.chunk_size, len(para))
                    segment = para[start:end].strip()
                    if segment:
                        chunks.append({
                            "chunk_id": f"{file_path.name}#chunk_{chunk_idx}",
                            "file_name": file_path.name,
                            "file_path": str(file_path),
                            "text": segment,
                            "length": len(segment),
                        })
                        chunk_idx += 1
                    start += self.chunk_size - self.overlap

        return chunks
