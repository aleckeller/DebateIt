"""
Pydantic models for debates
"""

from typing import Annotated
from datetime import datetime
from uuid import UUID

from pydantic import StringConstraints

from ..model import PsqlModel, BaseModel


class CreateDebate(PsqlModel):
    """
    Parameters for creating a debate
    """

    title: Annotated[
        str,
        StringConstraints(
            min_length=1,
            strip_whitespace=True,
        ),
    ]
    summary: Annotated[
        str,
        StringConstraints(
            min_length=1,
            strip_whitespace=True,
        ),
    ]
    created_by_id: UUID
    end_at: datetime
    category_ids: list[int]


class UploadFile(BaseModel):
    """
    Parameters for uploading a file
    """

    debate_id: int
    file_location: str
    file_bytes: bytes


class GetDebate(PsqlModel):
    """
    Parameters for getting a debate
    """

    debate_id: int
    user_id: UUID
