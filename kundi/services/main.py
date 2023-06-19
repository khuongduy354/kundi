from datetime import datetime
import uuid
from fastapi import HTTPException, status
from firebase_admin import firestore

from kundi.models.card import *


db = firestore.client()
batch = db.batch()


def get_set_doc(email: str, set: str):
    return db.collection("users").document(email).collection("sets").document(set)


def db_get_all_sets(email: str):
    try:
        snapshot = db.collection("users").document(
            email).collection("sets").stream()
        result = []
        for doc in snapshot:
            deck = doc.to_dict()
            deck["set_id"] = doc.id
            result.append(SetResponse(**deck))
        return result
    except:
        raise HTTPException(406)


def db_create_set(email: str, set_name: str):
    try:
        set_id = str(uuid.uuid4())
        set_ref = get_set_doc(email, set_id)
        set_ref.set({'set_name': set_name})
        result = set_ref.get().to_dict()
        result["set_id"] = set_id
        return SetResponse(**result)
    except:
        raise HTTPException(406)


def db_get_cards(email: str, set: str, review: bool = False):
    try:
        docs = get_set_doc(email, set).collection("cards").stream()
        result: list[Card] = []
        for doc in docs:
            result.append(Card(**doc.to_dict()))
        if review:
         # [{"review_due":""}]
            result = [x for x in result if x.review_due <=
                      datetime.now().isoformat()]
        print(result)

        return result
    except:
        raise HTTPException(status_code=406)


def db_update_cards(email: str, set: str, cards: list[Card]):
    try:
        for card in cards:
            card_ref = get_set_doc(email, set).collection(
                "cards").document(card.card_id)
            snapshot = card_ref.get()
            if snapshot.exists:
                new_card = {card.card_id: {"word": card.word,
                                           "definition": card.definition}}
                batch.set(card_ref, new_card)
        batch.commit()
    except:
        raise HTTPException(status_code=406)


async def db_create_cards(email: str, set: str, cards: List[CreateCardPayload]):
    try:
        docs_ref = get_set_doc(email, set).collection("cards").stream()
        for doc in docs_ref:
            batch.delete(doc.reference)
        batch.commit()

        for card in cards:
            print("up here")
            card_id = str(uuid.uuid4())
            card_ref = db.collection("users").document(

                email).collection("sets").document(set).collection("cards").document(card_id)
            new_card = Card(card_id=card_id, word=card.word,
                            definition=card.definition, review_due=datetime.now().isoformat())

            batch.set(card_ref, new_card.dict())
        batch.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=406)


def db_delete_cards(email: str, set: str, cards: list[Card]):
    try:
        for card in cards:
            card_ref = get_set_doc(email, set).collection(
                "cards").document(card.card_id)
            snapshot = card_ref.get()
            if snapshot.exists:
                batch.delete(card_ref)
        batch.commit()
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
