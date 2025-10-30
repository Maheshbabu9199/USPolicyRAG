from pydantic import Field, BaseModel


class RewriteOutputFormat(BaseModel):

    rewritten_query: str = Field(..., description='Rewritten query of the user query')