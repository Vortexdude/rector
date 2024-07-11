from fastapi import APIRouter

router = APIRouter()


@router.get("/me")
def get_details():
    return {"status": "doing nothing!"}
