"""
Pydantic models for debates
"""

from typing import Annotated
from datetime import datetime

from pydantic import StringConstraints

from ..model import PsqlModel


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
