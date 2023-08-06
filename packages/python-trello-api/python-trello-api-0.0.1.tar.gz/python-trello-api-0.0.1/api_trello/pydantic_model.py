from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class OldState(BaseModel):
    id_list: str = Field(None, alias="idList")
    closed: bool = None
    pos: int = None


class BadgeObject(BaseModel):
    due_complete: bool = Field(None, alias="dueComplete")


class TrelloCard(BaseModel):
    id: str = None
    short_id: int = Field(None, alias="idShort")
    id_list: str = Field(None, alias="idList")
    due: datetime = None
    pos: int = None
    type: str = None
    name: str = None
    short_link: str = Field(None, alias="shortLink")
    desc: str = None
    closed: bool = None
    id_members: List[str] = Field(None, alias="idMembers")
    badges: BadgeObject = None


class TrelloWebHook(BaseModel):
    id: str
    description: str = None
    idModel: str
    callback_url: str = Field(None, alias="callBackURL")
    active: bool
    cnt_fails: int = Field(None, alias="consecutiveFailures")
    date_fail_first: datetime = Field(None, alias="firstConsecutiveFailDate")


class TrelloBoard(BaseModel):
    id: str
    name: str = None
    short_link: str = Field(None, alias="shortLink")


class TrelloList(BaseModel):
    id: str
    name: str = None
    type: str = None
    text: str = None


class MemberCreator(BaseModel):
    id: str
    type: str = None
    username: str = None
    text: str = None
    full_name: str = Field(None, alias="fullName")


class Entities(BaseModel):
    card: TrelloCard = None
    list_before: TrelloList = Field(None, alias="listBefore")
    list_after: TrelloList = Field(None, alias="listAfter")
    member_creator: MemberCreator = Field(None, alias="memberCreator")


class Display(BaseModel):
    translationKey: str
    entities: Entities


class DataState(BaseModel):
    old: OldState = None
    card: TrelloCard = None
    board: TrelloBoard = None
    list_before: TrelloList = Field(None, alias="listBefore")
    list_after: TrelloList = Field(None, alias="listAfter")


class Model(BaseModel):
    id: str
    name: str


class Action(BaseModel):
    id: str
    id_member_creator: str = Field(None, alias="idMemberCreator")
    data: DataState
    type: str
    date: datetime
    display: Display
    member_creator: MemberCreator = Field(None, alias="memberCreator")


class TrelloUpdate(BaseModel):
    model: Model
    action: Action
