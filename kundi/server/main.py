from typing import Callable, Union, Annotated, List
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


class FirebaseUser(BaseModel):
    name: str
    user_id: str
    email: str


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

# Auth


@app.post("/v1/signup")
def signup_user(payload: UserAuthPayload):
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


def db_get_cards(email: str, set: str):
    docs = db.collection("users").document(
        email).collection("sets").document(set).collection("cards").stream()
    result: list[Card] = []
    for doc in docs:
        result.append(doc.to_dict())
    return result


def db_update_cards(email: str, set: str, cards: list[Card]):
    try:
        for card in cards:
            card_ref = db.collection("users").document(

                email).collection("sets").document(set).collection("cards").document(card.card_id)
            snapshot = card_ref.get()
            if snapshot.exists:
                new_card = {card.card_id: {"word": card.word,
                                           "definition": card.definition}}
                batch.set(card_ref, new_card)
        batch.commit()
    except:
        raise HTTPException(status_code=406)


def db_create_cards(email: str, set: str, cards: list[Card]):
    try:
        for card in cards:
            card_ref = db.collection("users").document(

                email).collection("sets").document(set).collection("cards").document(card.card_id)

            new_card = {card.card_id: {"word": card.word,
                                       "definition": card.definition}}
            batch.set(card_ref, new_card)
        batch.commit()
    except:
        raise HTTPException(status_code=406)


def db_delete_cards(email: str, set: str, cards: list[Card]):
    try:
        for card in cards:
            card_ref = db.collection("users").document(

                email).collection("sets").document(set).collection("cards").document(card.card_id)

            batch.delete(card_ref)
        batch.commit()
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)


@ app.get("/v1/sets/{set_id}/cards")
def get_cards(set_id: str):
    pass


async def parse_token(token: Annotated[str, oauth2_scheme]):
    try:
        decoded_jwt: dict = auth.verify_id_token(
            id_token=token, check_revoked=True)

        return decoded_jwt
    except:
        return None


@ app.post("/v1/sets/{set_id}/cards")
def create_cards(user: Annotated[dict, Depends(parse_token)], set_id: str, cards: List[Card]):
    if user == None:
        raise HTTPException(status_code=401)
    for card in cards:
        card.card_id = str(uuid.uuid4())
    db_create_cards(user["email"], set_id, cards)
    return


@ app.put("/v1/sets/{set_id}/cards")
def update_card(user: Annotated[dict, Depends(parse_token)], set_id: str, cards: List[Card]):
    if user == None:
        raise HTTPException(status_code=401)
    db_update_cards(user["email"], set_id, cards)
    pass


@ app.delete("/v1/cards/{card_id}")
def delete_card(card_id: int):
    pass
