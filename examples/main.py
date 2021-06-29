import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from examples.resources import UserCreate, UserDelete, UserDetail, UserList, UserUpdate

app = FastAPI()
register_tortoise(
    app, db_url="sqlite://:memory:", modules={"models": ["examples.models"]}, generate_schemas=True
)
app.include_router(UserList.as_router())
app.include_router(UserCreate.as_router())
app.include_router(UserDelete.as_router())
app.include_router(UserUpdate.as_router())
app.include_router(UserDetail.as_router())

if __name__ == "__main__":
    uvicorn.run("examples.main:app", reload=True, debug=True)
