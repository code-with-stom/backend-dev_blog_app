from pydantic import BaseModel, ConfigDict, computed_field
from datetime import datetime
from typing import List
from utils.enums import PostStatus
from schemas.tag import TagData, TagResponse
from schemas.comment import CommentResponse
from schemas.like import LikeResponse
class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    slug: str
    created_at: int
    updated_at: int | None = None
    category_id: int
    author_id: int
    status: str | None = PostStatus.DRAFT.value
    tags: List[str] | None = None
    comments: List[str] | None = None
    
class PostCreate(BaseModel):
    """Pydantic BaseModel for PostCreate

    Args:
        BaseModel (pydantic.BaseModel): Pydantic BaseModel
    Params:
        title (str): Title of the post
        content (str): Content of the post
        category_id (int): Category ID of the post
        tags list(TagData): List of tags
    """
    title: str
    content: str
    category_id: int
    status: str | None = PostStatus.DRAFT.value
    tags: List[TagData] | None = None

class PostResponse(BaseModel):
    """Pydantic BaseModel for PostResponse

    Args:
        BaseModel (pydantic.BaseModel): Pydantic BaseModel
    Params:
        title (str): Title of the post
        content (str): Content of the post
        slug (str): Slug of the post
        created_at (datetime): Creation timestamp of the post
        updated_at (datetime | None): Update timestamp of the post
        category_id (int): Category ID of the post
        status (str | None): Status of the post, default value of draft
        author_id (int): Author of the post
        tags list(TagResponse): Tags of the post
        comments list(CommentResponse): Comments of the post
        likes list(ListResponse): Likes on a post
        likes_count (int): Total number of likes on the post, computed from the likes list
    """
    title: str
    content: str
    slug: str
    created_at: datetime
    updated_at: datetime | None = None
    category_id: int
    status: str | None = PostStatus.DRAFT.value
    author_id: int
    tags: List[TagResponse] = []
    comments: List[CommentResponse] = []
    likes: List[LikeResponse] = []
    
    @computed_field
    @property
    def likes_count(self) -> int:
        return len(self.likes)
    
    @computed_field
    @property
    def comments_count(self) -> int:
        return len(self.comments)
    
    model_config = ConfigDict(from_attributes=True)