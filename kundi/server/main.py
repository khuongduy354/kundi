from typing import Callable, Union, Annotated, List
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, Request, status
import uuid
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, parse
import firebase_admin
from firebase_admin import auth, firestore
from firebase_admin import credentials

# auth setup
cred = credentials.Certificate("private_key.json")
firebase = firebase_admin.initialize_app(cred)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


db = firestore.client()
batch = db.batch()

Token = Annotated[str, oauth2_scheme]

# TODO: dataclasses here


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


class Card(BaseModel):
    card_id: str
    word: str
    definition: str
    review_counts: int = 0
    review_due: str
    box_id: int = 0


# class CreateCardsPayload(BaseModel):
#     card_id: int
#     word: str
#     definition: str


class UserAuthPayload(BaseModel):
    email: str
    password: str
    display_name: str


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# @app.middleware("http")
# async def verify_auth(request: Request, call_next):
#     try:
#         token = oauth2_scheme(request)
#         auth.verify_id_token(token, check_revoked=True)
#     except:
#         HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     response = await call_next(request)
#     return response


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.post("/test_token")
# def test_token(token: Token = Depends(oauth2_scheme)):
#     return token

# Auth


@app.post("/v1/signup")
def signup_user(payload: UserAuthPayload):
    print(payload)
    try:
        user = auth.create_user(email=payload.email, password=payload.password,
                                display_name=payload.display_name, email_verified=True)
        return user
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)


# @app.post("/v1/signin")
# def signin(token: Annotated[str, Depends(oauth2_scheme)]):
#     try:
#         decoded_jwt = auth.verify_id_token(token, check_revoked=True)
#         return decoded_jwt
#     except:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

# Cards


def get_set_doc(email: str, set: str):
    return db.collection("users").document(email).collection("sets").document(set)


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


async def parse_token(token: Annotated[str, oauth2_scheme]):
    try:
        decoded_jwt: dict = auth.verify_id_token(
            id_token=token, check_revoked=True)

        return decoded_jwt
    except:
        return None


class SetResponse(BaseModel):
    set_name: str
    set_id: str


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


# ROUTE HANDLERS


@app.get("/v1/sets")
async def get_all_sets(user: Annotated[dict, Depends(parse_token)]) -> List[SetResponse]:
    return db_get_all_sets(user["email"])


@ app.post("/v1/set")
def create_set(user: Annotated[dict, Depends(parse_token)], set_payload: CreateSetPayload) -> SetResponse:
    if user == None:
        raise HTTPException(status_code=401)
    result = db_create_set(user["email"], set_payload.set_name)
    return result


@ app.get("/v1/sets/{set_id}/cards")
def get_cards(user: Annotated[dict, Depends(parse_token)], set_id: str, review: bool = False):
    if user == None:
        raise HTTPException(status_code=401)
    return db_get_cards(user["email"], set_id, review)


@ app.post("/v1/sets/{set_id}/cards")
async def create_cards(user: Annotated[dict, Depends(parse_token)], set_id: str, cards: CreateCardsPayload):
    if user == None:
        raise HTTPException(status_code=401)
    await db_create_cards(user["email"], set_id, cards.cardList)


@ app.put("/v1/sets/{set_id}/cards")
def update_card(user: Annotated[dict, Depends(parse_token)], set_id: str, cards: List[Card]):
    if user == None:
        raise HTTPException(status_code=401)
    db_update_cards(user["email"], set_id, cards)


@ app.delete("/v1/sets/{set_id}/cards")
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


@app.post("/v1/sets/{set_id}/cards/{card_id}/review")
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
    pass
