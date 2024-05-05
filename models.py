from enum import Enum
from pydantic import BaseModel

# Request
class JavaFile(BaseModel):
    packagePath: str
    className: str
    classText: str

# Supported prediction patterns
class Pattern(str, Enum):
    ADAPTER = "ADAPTER"
    BUILDER = "BUILDER"
    PROTOTYPE = "PROTOTYPE"
    SINGLETON = "SINGLETON"
    NONE = "NONE"

# Response
class PatternPrediction(BaseModel):
    packagePath: str
    className: str
    predictedPattern: Pattern
