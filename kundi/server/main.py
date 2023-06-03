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


class CreateCardsPayload(BaseModel):
    word: str
    definition: str


class CreateSetPayload(BaseModel):
    set_name: str


class FirebaseUser(BaseModel):
    name: str
    user_id: str
    email: str


class ReviewedCard(BaseModel):
    card_id: str
    word: str
    definition: str
    # session_id:int
    review_counts: int
    review_due: datetime


class Card(BaseModel):
    card_id: str
    word: str
    definition: str


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


def db_get_cards(email: str, set: str):
    try:
        docs = get_set_doc(email, set).collection("cards").stream()
        result: list[Card] = []
        for doc in docs:
            result.append(doc.to_dict())
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


async def db_create_cards(email: str, set: str, cards: list[CreateCardsPayload]):
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

            new_card = {card_id: {"word": card.word,
                                  "definition": card.definition}}
            batch.set(card_ref, new_card)
            print("here")
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
def get_cards(user: Annotated[dict, Depends(parse_token)], set_id: str):
    if user == None:
        raise HTTPException(status_code=401)
    return db_get_cards(user["email"], set_id)


@ app.post("/v1/sets/{set_id}/cards")
async def create_cards(user: Annotated[dict, Depends(parse_token)], set_id: str, cards: List[CreateCardsPayload]):
    if user == None:
        raise HTTPException(status_code=401)
    await db_create_cards(user["email"], set_id, cards)


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
# moveRight = boolean


@app.post("v1/sets/{set_id}/cards/{card_id}/review")
def review_cards(set_id: str, user: Annotated[dict, Depends(parse_token)], duration: int = 3600, moveRight: bool = True):

    pass
