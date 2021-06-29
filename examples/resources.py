from pydantic import BaseModel

from examples.models import User
from fastapi_rest.resource import Resource


class UserResource(Resource):
    class UserUpdate(BaseModel):
        user: str

    model = User
    update_model = UserUpdate
