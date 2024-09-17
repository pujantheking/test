from typing import TypeVar
from pydantic import BaseModel
from pydantic.alias_generators import to_camel  # noqa



class CamelCaseModel(BaseModel):
    """
    A schemas for Camelcase.
    """

    class Config:
        """
        Configuration class for Pydantic models.
        This class defines configuration options for Pydantic models within the codebase. These options affect
        how the models are generated, validated, and populated.
        """

        alias_generator = to_camel
        populate_by_name = True
        arbitrary_types_allowed = True
        from_attributes = True


BaseDataField = TypeVar("BaseDataField", bound=CamelCaseModel)
