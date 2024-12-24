import io, pdfplumber
from fastapi import HTTPException

from app.crud.storage import download_file_bytes
from app.settings.elastic import elastic_cred, _es, _model


def __extract_pdf_text(content: bytes) -> str:
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    print("BOOK-PROCESSING: Finish extracting")
    return full_text


def __encode_text_to_vector(text: str) -> list[float]:
    return _model.encode(text, normalize_embeddings=True).tolist()


async def index_book(book_id: int, genre: str, book_file_path: str):
    book_text: str = __extract_pdf_text(await download_file_bytes(book_file_path))
    document = {
        "genre": genre if genre is not None else "", "content": book_text,
        "content_vector": __encode_text_to_vector(book_text)
    }
    try:
        await _es.index(index=elastic_cred.books_index, id=str(book_id), body=document)
        print("BOOK-PROCESSING: Finish indexing")
    except Exception as e:
        raise HTTPException(status_code=418, detail=f"Indexation error: {e}")


async def delete_book(book_id: int):
    try:
        await _es.delete(index=elastic_cred.books_index, id=str(book_id))
        print(f"BOOK-PROCESSING: Successfully deleted book with ID {book_id}")
    except Exception as e:
        raise HTTPException(status_code=418, detail=f"Deletion error: {e}")


async def context_search_books(query: str):
    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["genre^3", "content"],
                "type": "most_fields",
                "fuzziness": "AUTO"
            }
        }
    }
    return await _es.search(index=elastic_cred.books_index, body=search_body)


async def semantic_search_books(query: str):
    search_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "dotProduct(params.query_vector, 'content_vector')",
                "params": {"query_vector": __encode_text_to_vector(query)}
            }
        }
    }
    try:
        return await _es.search(index=elastic_cred.books_index, query=search_query)
    except Exception as e:
        print(f"Error: {e}")
