from pydantic import BaseModel, PositiveInt, create_model


class Paginator(BaseModel):
    page_name: str = "page"
    size_name: str = "size"

    @property
    def pager(self):
        members = {
            self.page_name: (PositiveInt, 1),
            self.size_name: (PositiveInt, 10),
        }
        return create_model("Pager", **members)
