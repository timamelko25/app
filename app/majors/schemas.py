from pydantic import BaseModel, Field

class MajorSchemeAdd(BaseModel):
    major_name: str = Field(..., description="Major name")
    major_description: str = Field(None, description="Major description")
    count_students: int = Field(0, description="Count students on major")
    
class MajorSchemeUpdate(BaseModel):
    major_name: str = Field(..., description="Major name")
    major_description: str = Field(..., description="Major description")
    
    