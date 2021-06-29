import abc
from typing import Optional, Tuple, Type

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise.queryset import QuerySet

from fastapi_rest.pagination import Paginator


class Resource(abc.ABC):
    model: Type[Model]
    name: Optional[str] = None

    @classmethod
    def resource_name(cls):
        return cls.name or cls.model.__name__.lower()

    @classmethod
    def as_router(cls):
        model_name = cls.model.__name__
        name = cls.resource_name()
        router = APIRouter(prefix=f"/{name}", tags=[model_name])
        return router


class ListView(Resource):
    paginator: Paginator = Paginator()
    fields: Optional[Tuple[str, ...]] = None
    exclude: Optional[Tuple[str, ...]] = None
    queryset: Optional[QuerySet] = None

    @classmethod
    def as_router(cls):
        router = super(ListView, cls).as_router()
        pager_model = cls.paginator.pager
        if cls.fields:
            response_model = pydantic_queryset_creator(cls.model, include=cls.fields)
        elif cls.exclude:
            response_model = pydantic_queryset_creator(cls.model, exclude=cls.exclude)
        else:
            response_model = pydantic_queryset_creator(cls.model)

        @router.get("", summary=f"Get {cls.resource_name()} list", response_model=response_model)
        async def _(pager: pager_model = Depends(pager_model)):
            qs = cls.queryset or cls.model.all()
            size = getattr(pager, cls.paginator.size_name)
            page = getattr(pager, cls.paginator.page_name)
            limit = size
            offset = (page - 1) * size
            if cls.fields:
                return await qs.only(*cls.fields).limit(limit).offset(offset)
            else:
                return await qs.limit(limit).offset(offset)

        return router


class DetailView(Resource):
    fields: Optional[Tuple[str, ...]] = None
    exclude: Optional[Tuple[str, ...]] = None

    @classmethod
    def as_router(cls):
        router = super(DetailView, cls).as_router()

        @router.post(
            "/{pk}",
            summary=f"Get {cls.resource_name()} item",
            response_model=pydantic_model_creator(cls.model),
        )
        async def _(pk: int):
            return await cls.model.get(pk=pk)

        return router


class CreateView(Resource):
    schema: Optional[Type[BaseModel]] = None

    @classmethod
    def as_router(cls):
        router = super(CreateView, cls).as_router()

        create_model = cls.schema or pydantic_model_creator(
            cls.model, name=f"{cls.model.__name__}_create", exclude_readonly=True
        )

        @router.post(
            "",
            summary=f"Create {cls.resource_name()}",
            response_model=pydantic_model_creator(cls.model),
        )
        async def _(data: create_model):  # type:ignore
            return await cls.model.create(**data.dict())  # type:ignore

        return router


class UpdateView(Resource):
    schema: Type[BaseModel]

    @classmethod
    def as_router(cls):
        router = super(UpdateView, cls).as_router()

        @router.put("/{pk}", summary=f"Update {cls.resource_name()}")
        async def _(pk: int, data: cls.schema):  # type:ignore
            obj = await cls.model.get(pk=pk)
            return await obj.update_from_dict(data.dict()).save()

        return router


class DeleteView(Resource):
    @classmethod
    def as_router(cls):
        router = super(DeleteView, cls).as_router()

        @router.delete("/{pk}", summary=f"Delete {cls.resource_name()}")
        async def _(
            pk: int,
        ):
            obj = await cls.model.get(pk=pk)
            return await obj.delete()

        return router
