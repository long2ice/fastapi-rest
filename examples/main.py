import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from examples.resources import UserResource

app = FastAPI()
register_tortoise(
    app, db_url="sqlite://:memory:", modules={"models": ["examples.models"]}, generate_schemas=True
)
app.include_router(UserResource.router())

if __name__ == "__main__":
    uvicorn.run("examples.main:app", reload=True, debug=True)
