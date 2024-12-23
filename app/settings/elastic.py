from elasticsearch import AsyncElasticsearch
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["elastic_cred", "init_elastic_indexing"]


class ElasticSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='ELASTIC_', env_file="./config/elastic.env")
    api_port: int
    hostname: str
    score_board: float = Field(gt=0.0)
    books_index: str = "books"

    @property
    def min_score(self):
        return self.score_board

    @property
    def elastic_url(self) -> str:
        return f"http://{self.hostname}:{self.api_port}"

    @property
    def index_settings(self):
        return {
            "settings": {"analysis": {"analyzer": {"default": {"type": "standard"}}}},
            "mappings": {
                "dynamic": "strict", "properties": {
                    "genre": {"type": "text"}, "content": {"type": "text"}
                }
            }
        }


elastic_cred = ElasticSettings()
_es = AsyncElasticsearch(elastic_cred.elastic_url)


async def init_elastic_indexing():
    if not await _es.indices.exists(index=elastic_cred.books_index):
        await _es.indices.create(index=elastic_cred.books_index, body=elastic_cred.index_settings)
# TODO: добавляем удаление индекса
