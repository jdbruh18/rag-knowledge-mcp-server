import json
from mcp.server.fastmcp import FastMCP
from rag_knowledge_mcp.tools import RAGTools

rag_tools = RAGTools()
mcp = FastMCP("Semantic Knowledge Retriever (RAG) Server")


@mcp.tool()
def index_directory(target_dir: str = "./sample_docs") -> str:
    """
    Scans a directory containing Markdown/Text documentation files, splits them into text chunks, and indexes them in the vector space.
    """
    res = rag_tools.index_directory(target_dir)
    return json.dumps(res, indent=2)


@mcp.tool()
def semantic_search(query: str, top_k: int = 3) -> str:
    """
    Performs semantic vector search against indexed documentation chunks and returns top-k matching snippets with similarity scores and file sources.
    """
    res = rag_tools.semantic_search(query, top_k=top_k)
    return json.dumps(res, indent=2)


@mcp.tool()
def get_kb_stats() -> str:
    """
    Returns statistics for the indexed knowledge base (total chunks, unique files, vocabulary size).
    """
    res = rag_tools.get_kb_stats()
    return json.dumps(res, indent=2)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
