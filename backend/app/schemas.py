from pydantic import BaseModel

class ItemIn(BaseModel):
    title: str

class ItemOut(BaseModel):
    id: int
    title: str

    model_config = {"from_attributes": True}

class Health(BaseModel):
    status: str
