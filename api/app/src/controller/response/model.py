from typing import Annotated
from uuid import UUID

from pydantic import StringConstraints

from models import VoteChoice
from ..model import PsqlModel


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
    created_by_id: UUID


class CreateVote(PsqlModel):
    """
    Parameters for creating a vote
    """

    response_id: int
    created_by_id: UUID
    vote_type: VoteChoice


class UpdateVote(PsqlModel):
    """
    Parameters for updating a vote
    """

    vote_id: int
    vote_type: VoteChoice


class DeleteVote(PsqlModel):
    """
    Parameters for updating a vote
    """

    vote_id: int
