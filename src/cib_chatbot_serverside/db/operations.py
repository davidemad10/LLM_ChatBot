"""Database operations for vector search and document management."""
import time
import os
import psycopg2.extras
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from .connection import get_db_connection
from ..config.settings import settings
from ..utils.logging import setup_logger

logger = setup_logger("db_operations")

# Initialize embeddings model
embedding_function = OllamaEmbeddings(model=settings.EMBEDDING_MODEL)


def similarity_search_with_scores(query: str, k: int = 3) -> List[Tuple[Document, float]]:
    """Search for similar documents using cosine similarity with query expansion."""
    logger.info(f"Starting similarity search", extra={'stage': 'SIMILARITY_SEARCH'})
    logger.debug(f"Query: {query}")
    
    # Add query expansion for better results
    expanded_query = query
    
    logger.info("Generating query embedding...", extra={'stage': 'EMBEDDING_GENERATION'})
    embed_start_time = time.time()
    query_embedding = embedding_function.embed_query(expanded_query)
    embed_time = time.time() - embed_start_time
    
    logger.debug(f"Embedding generated in {embed_time:.4f} seconds")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        logger.info("Executing vector similarity query...", extra={'stage': 'DATABASE_QUERY'})
        query_start_time = time.time()
        
        # Fetch more results for potential reranking
        fetch_k = k * 2
        
        cur.execute(
            """
            SELECT content, metadata, file_name, 1 - (embedding <=> %s::vector) AS similarity
            FROM document_chunks
            WHERE 1 - (embedding <=> %s::vector) > 0.1  -- Filter very low scores early
            ORDER BY embedding <=> %s::vector
            LIMIT %s
            """,
            (query_embedding, query_embedding, query_embedding, fetch_k)
        )
        
        query_time = time.time() - query_start_time
        logger.debug(f"Database query executed in {query_time:.4f} seconds")
        
        results = []
        rows = cur.fetchall()
        logger.info(f"Retrieved {len(rows)} results from database", extra={'stage': 'RESULTS_PROCESSING'})
        
        for idx, (content, metadata, file_name, similarity) in enumerate(rows):
            doc_metadata = metadata or {}
            doc_metadata["file_name"] = file_name
            doc = Document(page_content=content, metadata=doc_metadata)
            results.append((doc, similarity))
        
        # Optional: Rerank based on keyword overlap
        if len(results) > k:
            results = _rerank_results(results, query, k)
        
        logger.info(f"Similarity search completed. Best score: {results[0][1]:.4f}" if results else "No results found")
        return results
    except Exception as e:
        logger.error(f"Database query error: {str(e)}", exc_info=True)
        raise
    finally:
        cur.close()
        conn.close()


def _rerank_results(results: List[Tuple[Document, float]], query: str, k: int) -> List[Tuple[Document, float]]:
    """Rerank results based on keyword overlap."""
    query_terms = set(query.lower().split())
    
    scored_results = []
    for doc, similarity in results:
        content_terms = set(doc.page_content.lower().split())
        overlap = len(query_terms & content_terms)
        combined_score = similarity * 0.7 + (overlap / len(query_terms)) * 0.3
        scored_results.append((doc, similarity, combined_score))
    
    # Sort by combined score and return top k
    scored_results.sort(key=lambda x: x[2], reverse=True)
    return [(doc, sim) for doc, sim, _ in scored_results[:k]]


def save_to_pgvector(chunks: List[Document]):
    """Save document chunks to PostgreSQL with pgvector."""
    if len(chunks) == 0:
        print("No chunks to add")
        return
    
    print(f"Adding chunks: {len(chunks)}")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        for chunk in chunks:
            chunk_id = chunk.metadata["id"]
            # Extract only the filename from the source path
            file_name = os.path.basename(chunk.metadata.get("source", "unknown"))
            
            # Check if chunk already exists
            cur.execute(
                "SELECT 1 FROM document_chunks WHERE metadata->>'id' = %s",
                (chunk_id,)
            )
            if cur.fetchone():
                print(f"Skipping existing chunk: {chunk_id}")
                continue
            
            # Generate embedding
            embedding = embedding_function.embed_query(chunk.page_content)
            
            # Insert into document_chunks table
            cur.execute(
                """
                INSERT INTO document_chunks (content, embedding, metadata, file_name)
                VALUES (%s, %s, %s, %s)
                """,
                (chunk.page_content, embedding, psycopg2.extras.Json(chunk.metadata), file_name)
            )
        
        conn.commit()
        print("Chunks added successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error adding chunks: {e}")
        raise
    finally:
        cur.close()
        conn.close()
