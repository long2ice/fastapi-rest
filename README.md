# fastapi-rest

[![image](https://img.shields.io/pypi/v/fastapi-rest.svg?style=flat)](https://pypi.python.org/pypi/fastapi-rest)
[![image](https://img.shields.io/github/license/long2ice/fastapi-rest)](https://github.com/long2ice/fastapi-rest)
[![image](https://github.com/long2ice/fastapi-rest/workflows/pypi/badge.svg)](https://github.com/long2ice/fastapi-rest/actions?query=workflow:pypi)
[![image](https://github.com/long2ice/fastapi-rest/workflows/ci/badge.svg)](https://github.com/long2ice/fastapi-rest/actions?query=workflow:ci)

## Introduction

Fast restful API based on FastAPI and TortoiseORM.

## Install

```shell
pip install fastapi-rest
```

## Quick Start

First, define your `ListView` resource.

```python
from fastapi_rest.resource import ListView


class UserList(ListView):
    model = User
    fields = ("name", "age")
```

Second, include router to your app.

```python
app.include_router(UserList.as_router())
```

Now, you can visit the endpoint `/user` to get user list.

### ListView

Export the endpoint `GET /{resource}`.

```python
class ListView(Resource):
    paginator: Paginator = Paginator()
    fields: Optional[Tuple[str, ...]] = None
    exclude: Optional[Tuple[str, ...]] = None
    queryset: Optional[QuerySet] = None
```

### DetailView

Export the endpoint `GET /{resource}/{pk}`.

```python
class DetailView(Resource):
    fields: Optional[Tuple[str, ...]] = None
    exclude: Optional[Tuple[str, ...]] = None
```

### CreateView

Export the endpoint `POST /{resource}`.

```python
class CreateView(Resource):
    schema: Optional[Type[BaseModel]] = None
```

### UpdateView

Export the endpoint `PUT /{resource}/{pk}`.

```python
class UpdateView(Resource):
    schema: Type[BaseModel]
```

### DeleteView

Export the endpoint `DELETE /{resource}/{pk}`.

```python
class DeleteView(Resource):
    pass
```

## Reference

You can see the examples [here](./examples).

## License

This project is licensed under the [Apache2.0](https://github.com/long2ice/fastapi-rest/blob/master/LICENSE) License.
