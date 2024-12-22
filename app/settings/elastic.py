from elasticsearch import Elasticsearch
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["elastic_cred", "init_elastic_indexing"]


class ElasticSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='ELASTIC_', env_file="./config/elastic.env")
    api_port: int
    hostname: str
    books_index: str = "books"

    @property
    def elastic_url(self) -> str:
        return f"http://{self.hostname}:{self.api_port}"

    @property
    def index_settings(self):
        return {
            "settings": {"analysis": {"analyzer": {"default": {"type": "standard"}}}},
            "mappings": {"dynamic": "strict", "properties": {
                "title": {"type": "text"}, "author": {"type": "text"},
                "genre": {"type": "keyword"}, "content": {"type": "text"}
            }}
        }


elastic_cred = ElasticSettings()
_es = Elasticsearch(elastic_cred.elastic_url)


def init_elastic_indexing():
    if not _es.indices.exists(index=elastic_cred.books_index):
        _es.indices.create(index=elastic_cred.books_index, body=elastic_cred.index_settings)
