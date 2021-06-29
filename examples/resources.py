from typing import Optional

from pydantic import BaseModel

from examples.models import User
from fastapi_rest.resource import Resource


class UserResource(Resource):
    class UserUpdate(BaseModel):
        user: Optional[str]
        age: Optional[str]

    model = User
    update_model = UserUpdate
    fields = ["name", "age"]
