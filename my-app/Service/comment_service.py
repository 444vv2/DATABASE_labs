from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text

from db.models import Comment
from schemas.comment import CommentResponse

class CommentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_comment(self, user_id: int, descriptions: str) -> CommentResponse:
        try:
            await self.session.execute(
                text("CALL insert_comment_param(:id, :descrip)"),
                {"id": user_id, "descrip": descriptions}
            )
            await self.session.commit()

            result = await self.session.execute(
                select(Comment).order_by(Comment.comment_id.desc()).limit(1)
            )
            comment = result.scalars().first()

            if not comment:
                raise ValueError("Failed to create comment")

            return CommentResponse.model_validate(comment)

        except Exception as e:
            await self.session.rollback()
            raise ValueError(f"Error creating comment: {str(e)}") from e
