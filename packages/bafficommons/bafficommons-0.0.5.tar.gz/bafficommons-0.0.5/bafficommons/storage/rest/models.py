from pydantic import BaseModel
from typing import List, Tuple

# Files

class CreateFileRestModel(BaseModel):
    name: str
    extension: str
    content_type: str
    content: str


class MutipleFilesRestModel(BaseModel):
    id: str
    name: str
    extension: str
    content_type: str

# Checks

class FileResultRestModel(BaseModel):
    id: str
    name: str
    match_percentage: float
    lines_matched: List[Tuple[int, int]]


class CheckMatchRestModel(BaseModel):
    source_file: FileResultRestModel
    target_file: FileResultRestModel


class CreateCheckRestModel(BaseModel):
    name: str
    matches: List[CheckMatchRestModel]


class MultipleCheckRestModel(BaseModel):
    id: str
    name: str