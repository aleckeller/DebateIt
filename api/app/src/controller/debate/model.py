"""
Pydantic models for debates
"""

from typing import Annotated
from datetime import datetime

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
    created_by_id: int
    end_at: datetime
    category_ids: list[int]


class UploadFile(BaseModel):
    """
    Parameters for uploading a file
    """

    debate_id: int
    file_location: str
    file_bytes: bytes


class CreateResponse(PsqlModel):
    """
    Parameters for creating a response
    """

    body: Annotated[
        str,
        StringConstraints(
            min_length=1,
            strip_whitespace=True,
        ),
    ]
    debate_id: int
    user_id: int
    agree: int
    disagree: int
