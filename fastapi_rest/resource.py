from enum import Enum
from typing import Optional, Tuple, Type

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from fastapi_rest.exceptions import ConfigurationError
from fastapi_rest.pagination import Paginator


class Method(Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"


class Resource:
    model: Type[Model]
    name: Optional[str] = None
    paginator: Paginator = Paginator()
    methods = [method for method in Method]
    create_model: Optional[Type[BaseModel]] = None
    update_model: Optional[Type[BaseModel]] = None
    fields: Optional[Tuple[str]] = None

    @classmethod
    def router(cls):
        model_name = cls.model.__name__
        name = cls.name or model_name.lower()
        router = APIRouter(prefix=f"/{name}", tags=[model_name])
        create_model = cls.create_model or pydantic_model_creator(
            cls.model, name=f"{model_name}_create", exclude_readonly=True
        )
        if Method.GET in cls.methods:
            pager_model = cls.paginator.pager
            if cls.fields:
                response_model = pydantic_queryset_creator(cls.model, include=cls.fields)

            else:
                response_model = pydantic_queryset_creator(cls.model)

            @router.get("", summary=f"Get {name} list", response_model=response_model)
            async def _(pager: pager_model = Depends(pager_model)):
                size = getattr(pager, cls.paginator.size_name)
                page = getattr(pager, cls.paginator.page_name)
                limit = size
                offset = (page - 1) * size
                return await cls.model.all().limit(limit).offset(offset)

        if Method.POST in cls.methods:

            @router.post(
                "", summary=f"Create {name}", response_model=pydantic_model_creator(cls.model)
            )
            async def _(data: create_model):  # type:ignore
                return await cls.model.create(**data.dict())  # type:ignore

        if Method.PUT in cls.methods:
            if not cls.update_model:
                raise ConfigurationError(f"Need update_model set for {cls} when PUT method enabled")

            @router.put("/{pk}", summary=f"Update {name}")
            async def _(pk: int, data: cls.update_model):  # type:ignore
                obj = await cls.model.get(pk=pk)
                return await obj.update_from_dict(data.dict()).save()  # type:ignore

        if Method.DELETE in cls.methods:

            @router.delete("/{pk}", summary=f"Delete {name}")
            async def _(
                pk: int,
            ):
                obj = await cls.model.get(pk=pk)
                return await obj.delete()

        return router
