"""
Model for user sign up
"""
from json import loads

from aws_lambda_powertools.utilities.parser import BaseModel


class PsqlModel(BaseModel):
    """
    Model to resolve psql bind variables
    """

    def bind_vars(self) -> dict:
        """
        Bind variables to be used in the query
        """
        return loads(self.json())


class CreateUser(PsqlModel):
    """
    Parameters for creating a user
    """

    id: str
    username: str
