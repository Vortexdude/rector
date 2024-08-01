from enum import Enum
from typing import List
from fastapi import Query
from pydantic.dataclasses import dataclass


class ExportQualities(Enum):
    sd = 'sd'
    hd = 'hd'
    fhd = 'fhd'
    qhd = 'qhd'


@dataclass
class QualitiesModel:
    quality: List[ExportQualities] = Query(...)
