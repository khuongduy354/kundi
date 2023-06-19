
from datetime import datetime, timedelta
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import firestore

from kundi.helpers.tokenauth import parse_token
from kundi.models.card import Card, CreateCardPayload, CreateCardsPayload, CreateSetPayload, SetResponse
from kundi.services.main import db_get_cards, db_create_cards, db_update_cards, db_delete_cards, get_set_doc, db_get_all_sets, db_create_set


router = APIRouter()


@router.get("/sets")
async def get_all_sets(user: Annotated[dict, Depends(parse_token)]) -> List[SetResponse]:
    return db_get_all_sets(user["email"])


@router.post("/set")
def create_set(user: Annotated[dict, Depends(parse_token)], set_payload: CreateSetPayload) -> SetResponse:
    if user == None:
        raise HTTPException(status_code=401)
    result = db_create_set(user["email"], set_payload.set_name)
    return result


@ router.get("/sets/{set_id}/cards")
def get_cards(user: Annotated[dict, Depends(parse_token)], set_id: str, review: bool = False):
    if user == None:
        raise HTTPException(status_code=401)
    return db_get_cards(user["email"], set_id, review)


@ router.post("/sets/{set_id}/cards")
async def create_cards(user: Annotated[dict, Depends(parse_token)], set_id: str, cards: CreateCardsPayload):
    print("here")
    if user == None:
        raise HTTPException(status_code=401)
    await db_create_cards(user["email"], set_id, cards.cardList)


@ router.put("/sets/{set_id}/cards")
def update_card(user: Annotated[dict, Depends(parse_token)], set_id: str, cards: List[Card]):
    if user == None:
        raise HTTPException(status_code=401)
    db_update_cards(user["email"], set_id, cards)


@ router.delete("/sets/{set_id}/cards")
def delete_cards(user: Annotated[dict, Depends(parse_token)], set_id: str, cards: List[Card]):
    if user == None:
        raise HTTPException(status_code=401)
    db_delete_cards(user["email"], set_id, cards)

# REVISION system
# Cards extra attribute:
# review_counts:
# next_review: Date()

# duration=minutes in querystring
# move_dir = right, left, none


@router.post("/sets/{set_id}/cards/{card_id}/review")
def review_cards(card_id: str, set_id: str, user: Annotated[dict, Depends(parse_token)], duration: int = 10, move_dir: str = "right"):
    card_ref = get_set_doc(user["email"], set_id).collection(
        "cards").document(card_id)

    review_due = datetime.now() + timedelta(minutes=duration)
    review_due = review_due.isoformat()
    box_id_in = 1
    if move_dir == "left":
        box_id_in = -1
    if move_dir == "none":
        box_id_in = 0

    update_info = {"review_counts": firestore.firestore.Increment(
        1), "review_due": review_due, "box_id": firestore.firestore.Increment(box_id_in)}
    card_ref.update(update_info)
