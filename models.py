from typing import Literal
from xmlrpc.client import Boolean
from pydantic import BaseModel, Field
from random import randint
from time import time

class LoginCredentials(BaseModel):
    username: str 
    password: str 


class User(BaseModel):
    employeeId: int
    username: str 
    password: str
    firstName: str 
    lastName: str 
    role: Literal["Admin"] | Literal["Employee"]


class UserInfo(BaseModel):
    employeeId: int
    username: str 
    firstName: str 
    lastName: str 
    role: Literal["Admin"] | Literal["Employee"]


class Suggestion(BaseModel):
    suggestionId: int  = 0
    desc: str 
    priority: Literal["Low"] | Literal["Medium"] | Literal["High"] = Field(description="The percieved urgency of the suggestion")
    upVotes: int = 0
    downVotes: int = 0
    createdAt: int = 0


class SuggestionPayload(BaseModel):
    desc: str
    priority: Literal["Low"] | Literal["Medium"] | Literal["High"] 


class TechRequest(BaseModel):
    requestor: str 
    message: str


class TechReview(BaseModel):
    reviewId: int
    requestor: str 
    message: str
    createdAt: int 
    isClosed: Boolean
