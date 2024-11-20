from fastapi import APIRouter
from app.majors.service import MajorsService
from app.majors.schemas import MajorSchemeAdd, MajorSchemeUpdate

router = APIRouter(prefix="/major", tags = ["Major handler"])

@router.post("/add")
async def add_major(major: MajorSchemeAdd) -> dict:
    result = await MajorsService.add(**major.dict())
    if result:
        return {"message": "Added successfully",
                "major": major}
    else:
        return {"message": "Error while add"}
    
@router.put("/upd")
async def upd_major_description(major: MajorSchemeUpdate) -> dict:
    result = await MajorsService.update(
        filter_by = {'major_name': major.major_name},
        major_description = major.major_description
    )
    if result:
        return {"message": "Updated successfully",
                "major": major}
    else:
        return {"message": "Error while updating major"}
    
@router.delete("/delete/{id}")
async def delete_major_id(major_id: int) -> dict:
    result = await MajorsService.delete(id=major_id)
    if result:
        return {
            "message": "Deleted successfully",
            "major_id": major_id,
            }
    else:
        return {"message": "Error while deleting"}