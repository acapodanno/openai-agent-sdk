from pydantic import BaseModel,Field
class User(BaseModel):
    name: str = Field("Name of user if is present")
    id: int = Field("Unique ID of user")
    email: str = Field("Email of user")
