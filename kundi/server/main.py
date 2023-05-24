from typing import Callable, Union, Annotated, List
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
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


class Card(BaseModel):
    card_id: int
    word: str
    definition: str


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
                                display_name=payload.display_name, verified=True)
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


def db_get_card(email: str, set: str):
    docs = db.collection("users").document(
        email).collection("sets").document(set).collection("cards").stream()
    result = []
    for doc in docs:
        result.append(doc.to_dict())
    return result


def db_create_cards(email: str, set: str, cards: list[Card]):
    for card in cards:
        card_ref = db.collection("users").document(

            email).collection("sets").document(set).collection("cards").document(str(card.card_id))

        new_card = {str(card.card_id): {"word": card.word,
                                        "definition": card.definition}}
        batch.set(card_ref, new_card)
    batch.commit()


def db_delete_cards(email: str, set: str, cards: list[Card]):
    try:
        for card in cards:
            card_ref = db.collection("users").document(

                email).collection("sets").document(set).collection("cards").document(str(card.card_id))

            batch.delete(card_ref)
        batch.commit()
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
# same as create cards, differences lie on the handler
# def db_update_cards(email: str, set: str, cards: list[Card]):
#     for card in cards:
#         doc_ref = db.collection("users").document(
#
#             email).collection("sets").document(set).collection("cards").document(str(card.card_id))
#         new_card = {str(card.card_id): {"word": card.word,
#                                         "definition": card.definition}}
#
#         batch.doc_ref.set(doc_ref, new_card)
#     batch.commit


@ app.get("/v1/cards/{card_id}")
def get_card(card_id: str):
    pass


@ app.post("/v1/cards/")
def create_cards(token: Token, cards: List[Card]):

    pass


@ app.put("/v1/cards/{card_id}")
def update_card(card_id: int, new_card: Card):
    pass


@ app.delete("/v1/cards/{card_id}")
def delete_card(card_id: int):
    pass
