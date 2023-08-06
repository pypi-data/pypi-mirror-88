from pydantic import BaseModel
from enum import Enum
from typing import List, Tuple, Optional

# Algorithms

class AlgorithmName(str, Enum):
    winnowing = "winnowing"

class AlgorithmRestModel(BaseModel):
    algorithm_name: AlgorithmName

# Checks

class OptionsRestModel(BaseModel):
    sensitivity: float


class CreateCheckRestModel(BaseModel):
    check_name: str
    algorithm_name: AlgorithmName
    source_file_ids: List[str]
    target_file_ids: List[str]
    options: Optional[OptionsRestModel]


class FileResultRestModel(BaseModel):
    id: str
    name: str
    match_percentage: float
    lines_matched: List[Tuple[int, int]]


class CheckResultRestModel(BaseModel):
    source_file: FileResultRestModel
    target_file: FileResultRestModel


class CheckRestModel(BaseModel):
    name: str
    matches: List[CheckResultRestModel]

