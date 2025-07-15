from pydantic import BaseModel
from utils.enums import RolUsuario

class RolBase(BaseModel):
    nombre: RolUsuario

class RolCreate(RolBase):
    pass

class RolResponse(RolBase):
    id: int

    model_config = {
        "from_attributes": True  
    }