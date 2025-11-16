from .base import ORMBase
from pydantic import UUID4, BaseModel
from typing import Optional
from typing import List, Optional, Dict, Any


class TransformCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[List[str]] = None


class TransformRead(ORMBase):
    id: UUID4
    name: str
    class_name: str
    description: Optional[str]
    category: Optional[List[str]]
    flow_schema: Optional[Dict[str, Any]]


class TransformUpdate(BaseModel):
    name: Optional[str] = None
    class_name: str = None
    description: Optional[str] = None
    category: Optional[List[str]] = None
