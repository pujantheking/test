import json
from typing import List, Any
from io import BytesIO
import pandas as pd

from apps.knowledge_bases.exceptions import (
    InvalidJsonException,
    InvalidFileTypeException,
    InvalidCsvException,
    QuestionNotFoundException,
    ResponseNotFoundException,
)


def json_validator(json_data) -> List[Any]:
    """
    This function validates the json data and if data gets validated it returns the json data.

    :param json_data: The data that needs to be validated and converted into json format.
    :return: json object
    """
    try:
        data = json.loads(json_data)
    except ValueError:
        raise InvalidJsonException
    return data


def csv_validator(csv_data) -> pd.DataFrame:
    """
    This function validates the json data and if data gets validated it returns the json data.
    :param csv_data: The data that needs to be validated and converted into dataframe format.
    :return: dataframe object
    """
    try:
        csv_data = BytesIO(csv_data)
        data = pd.read_csv(csv_data)
        if "question" not in data.columns:
            raise QuestionNotFoundException
        if "response" not in data.columns:
            raise ResponseNotFoundException
    except ValueError:
        raise InvalidCsvException
    return data


def file_validator(file_name) -> None:
    """
    This function validates the file type.

    :param file_name: filename extracted from the file uploaded by the user
    :return: None
    """
    split_file = file_name.split(".")
    if split_file[-1] != "csv":
        raise InvalidFileTypeException
