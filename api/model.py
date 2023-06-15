from typing import Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    model: Optional[str] = Field(default="gpt-3.5-turbo-0613", description="Model name")
    messages: list = Field(..., description="Message")
    functions: Optional[list] = Field(default=[],
                                      description="a list of functions the model may generate JSON inputs for")
    function_call: Optional[str] = Field('auto', description="Controls how the model responds to function calls."
                                                             "'none' means the model does not call a function"
                                                             "'auto' means the model can pick between an end-user or calling a function"
                                                             "'none' is the default when no functions are present, 'auto' is the default if functions are present")
    temperature: Optional[float] = Field(default=1.0, description="Temperature")
    top_p: Optional[int] = Field(default=1, description="Top p")
    stream: Optional[bool] = Field(default=False, description='')
    stop: Optional[str] = Field(default=None)
    max_tokens: Optional[int] = Field(default=2048, description="Maximum number of tokens")
    presence_penalty: Optional[float] = Field(default=0.0, description="Presence penalty")
    frequency_penalty: Optional[float] = Field(default=0.0, description="Frequency penalty")
    logit_bias: Optional[dict] = Field(default=dict())
    user: Optional[str] = Field(default='')


def get_parameters(message: Message):
    dt = message.dict()
    if not dt['functions']:
        dt.pop('functions')
        dt.pop('function_call')
    return dt
