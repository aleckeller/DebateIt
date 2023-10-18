from typing import Annotated

from pydantic import StringConstraints

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
    created_by_id: int
    agree: int
    disagree: int
