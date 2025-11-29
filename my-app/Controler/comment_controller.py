from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_db
from Service import CommentService
from schemas.comment import CommentCreate, CommentResponse

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/insert_from_procedure", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(comment_data: CommentCreate, db: AsyncSession = Depends(get_db)):
    service = CommentService(db)
    try:
        comment = await service.create_comment(
            user_id=comment_data.user_id,
            descriptions=comment_data.descriptions
        )
        return comment
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        ) from ve
