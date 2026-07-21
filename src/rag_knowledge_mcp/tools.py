import os
from typing import Dict, List, Any, Optional
from rag_knowledge_mcp.chunker import DocumentChunker
from rag_knowledge_mcp.vector_store import SemanticVectorStore


class RAGTools:
    """
    Exposes RAG Knowledge Retriever tools for MCP integration.
    """

    def __init__(self, vector_store: Optional[SemanticVectorStore] = None):
        self.chunker = DocumentChunker()
        self.store = vector_store or SemanticVectorStore()
        
        # Auto-index sample_docs directory if present
        sample_path = os.path.abspath("sample_docs")
        if os.path.exists(sample_path):
            self.index_directory(sample_path)

    def index_directory(self, target_dir: str) -> Dict[str, Any]:
        """
        Scans a directory of markdown/text documentation, chunks files, and indexes vectors.
        """
        chunks = self.chunker.process_directory(target_dir)
        self.store.add_chunks(chunks)
        stats = self.store.get_stats()
        return {
            "status": "success",
            "indexed_directory": target_dir,
            "new_chunks_added": len(chunks),
            "total_knowledge_base_chunks": stats["total_chunks"],
            "total_unique_files": stats["unique_files_count"],
        }

    def semantic_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Performs semantic vector search against indexed document chunks.
        """
        return self.store.search(query, top_k=top_k)

    def get_kb_stats(self) -> Dict[str, Any]:
        """
        Returns statistics about the current vector knowledge base.
        """
        return self.store.get_stats()
