from enum import Enum

class Roles(str, Enum):
    ADMIN = "admin"
    USER = "user"
    
class PostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"