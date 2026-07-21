import tempfile
import pytest
from pathlib import Path
from rag_knowledge_mcp.chunker import DocumentChunker
from rag_knowledge_mcp.vector_store import SemanticVectorStore
from rag_knowledge_mcp.tools import RAGTools


def test_document_chunker():
    with tempfile.TemporaryDirectory() as tmp_dir:
        doc_path = Path(tmp_dir) / "guide.md"
        doc_path.write_text("# Title\n\nThis is paragraph one.\n\nThis is paragraph two about encryption.")

        chunker = DocumentChunker()
        chunks = chunker.process_directory(tmp_dir)
        assert len(chunks) == 3
        file_names = [c["file_name"] for c in chunks]
        assert "guide.md" in file_names


def test_vector_store_semantic_search():
    store = SemanticVectorStore()
    sample_chunks = [
        {"chunk_id": "1", "file_name": "db.md", "file_path": "/db.md", "text": "PostgreSQL database with read replicas and AES-256 encryption."},
        {"chunk_id": "2", "file_name": "auth.md", "file_path": "/auth.md", "text": "OAuth2 authentication with JWT bearer tokens."},
        {"chunk_id": "3", "file_name": "api.md", "file_path": "/api.md", "text": "Rate limits of 100 requests per minute per IP address."},
    ]
    store.add_chunks(sample_chunks)

    # Search query for encryption
    results_enc = store.search("AES data encryption", top_k=1)
    assert len(results_enc) == 1
    assert results_enc[0]["file_name"] == "db.md"
    assert results_enc[0]["similarity_score"] > 0.0

    # Search query for rate limits
    results_rate = store.search("request limits per minute", top_k=1)
    assert len(results_rate) == 1
    assert results_rate[0]["file_name"] == "api.md"


def test_rag_tools_sample_docs():
    store = SemanticVectorStore()
    tools = RAGTools(vector_store=store)

    # Verify auto-indexed sample_docs
    stats = tools.get_kb_stats()
    assert stats["total_chunks"] > 0
    assert stats["unique_files_count"] == 3

    # Semantic search against sample_docs
    res = tools.semantic_search("Kafka message queue Kafka", top_k=1)
    assert len(res) == 1
    assert "architecture.md" in res[0]["file_name"]
