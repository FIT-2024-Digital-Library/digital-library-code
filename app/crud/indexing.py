import re, io, nltk, pdfplumber
from fastapi import HTTPException

from app.crud.storage import download_file_bytes
from app.settings.elastic import elastic_cred, _es


nltk.download('wordnet')
nltk.download('stopwords')
__english_stop_words = set(nltk.corpus.stopwords.words('english'))


def __extract_pdf_text(content: bytes) -> str:
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    print("BOOK-PROCESSING: Finish extracting")
    return full_text


def __preprocess_text(text, remove_punctuation=True):
    text = text.replace("\n", " ").replace("\t", " ")
    text = re.sub(r'\s+', ' ', text)  ## лишние пробелы

    if remove_punctuation:
        text = re.sub(r'[^\w\s]', '', text)

    text = text.lower()
    return text


async def index_book(book_id: int, genre: str, book_file_path: str):
    document = {
        "genre": genre if genre is not None else "",
        "content": __preprocess_text(__extract_pdf_text(await download_file_bytes(book_file_path)))
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
    search_query = {
        "multi_match": {
            "query": __preprocess_text(query),
            "fields": ["genre", "content"],
            "type": "most_fields",
            "operator": "and",
            "fuzziness": "AUTO"
        }
    }
    return await _es.search(index=elastic_cred.books_index, query=search_query)


def __expand_and_filter_query(query: str) -> str:
    query_words = set([word for word in query.split() if word not in __english_stop_words])
    new_words = set()
    for word in query_words:
        synonyms = nltk.corpus.wordnet.synsets(word)
        for syn in synonyms:
            for lemma in syn.lemmas():
                new_words.add(lemma.name().replace('_', ' '))
    print(f"BOOK-PROCESSING: Expanded query\n{new_words}")
    return " ".join(query_words.union(new_words))


async def semantic_search_books(query: str):
    search_query = {
        "multi_match": {
            "query": __expand_and_filter_query(__preprocess_text(query)),
            "fields": ["genre^3", "content"],
            "type": "most_fields",
            "operator": "or",
            "fuzziness": "AUTO"
        }
    }
    return await _es.search(index=elastic_cred.books_index, query=search_query)
