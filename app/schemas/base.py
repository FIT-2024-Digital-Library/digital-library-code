from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

__all__ = ['CamelCaseBaseModel']


class CamelCaseBaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
