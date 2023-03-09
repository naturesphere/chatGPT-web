from typing import Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    model: Optional[str] = Field(default="gpt-3.5-turbo", description="Model name")
    messages: list = Field(..., description="Message")
    temperature: Optional[float] = Field(default=1.0, description="Temperature")
    top_p: Optional[int] = Field(default=1, description="Top p")
    stream: Optional[bool] = Field(default=False, description='')
    stop: Optional[str] = Field(default=None)
    max_tokens: Optional[int] = Field(default=2048, description="Maximum number of tokens")
    presence_penalty: Optional[float] = Field(default=0.0, description="Presence penalty")
    frequency_penalty: Optional[float] = Field(default=0.0, description="Frequency penalty")
    logit_bias: Optional[dict]
    user: Optional[str]