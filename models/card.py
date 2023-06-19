

from typing import List
from pydantic import BaseModel


def test_out():
    pass


class SetResponse(BaseModel):
    set_name: str
    set_id: str


class Card(BaseModel):
    card_id: str
    word: str
    definition: str
    review_counts: int = 0
    review_due: str
    box_id: int = 0


class CreateCardPayload(BaseModel):
    word: str
    definition: str


class CreateCardsPayload(BaseModel):
    cardList: List[CreateCardPayload]


class CreateSetPayload(BaseModel):
    set_name: str


class FirebaseUser(BaseModel):
    name: str
    user_id: str
    email: str


# class ReviewedCard(BaseModel):
#     card_id: str
#     word: str
#     definition: str
#     # session_id:int
#     review_counts: int
#     review_due: datetime


# class CreateCardsPayload(BaseModel):
#     card_id: int
#     word: str
#     definition: str


class UserAuthPayload(BaseModel):
    email: str
    password: str
    display_name: str
