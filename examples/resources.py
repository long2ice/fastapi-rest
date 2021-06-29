from typing import Optional

from pydantic import BaseModel

from examples.models import User
from fastapi_rest.resource import CreateView, DeleteView, DetailView, ListView, UpdateView


class UserSchema(BaseModel):
    user: Optional[str]
    age: Optional[int]


class UserList(ListView):
    model = User
    fields = ("name", "age")


class UserDetail(DetailView):
    model = User
    fields = ("name", "age")


class UserDelete(DeleteView):
    model = User


class UserCreate(CreateView):
    model = User


class UserUpdate(UpdateView):
    model = User
    schema = UserSchema
