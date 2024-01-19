from pydantic import BaseModel


class ${NAME}SchemaBase(BaseModel):
    pass
   

class ${NAME}SchemaCreate(${NAME}SchemaBase):
    pass
    

class ${NAME}Schema(${NAME}SchemaBase):
    pass
    
    class Config:
        from_attributes = True