from typing import Callable, Union, Annotated, List
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

# auth setup
cred = credentials.Certificate("private_key.json")
firebase = firebase_admin.initialize_app(cred)
user: auth.UserRecord = auth.get_user("YJEuD5XQSSe4O7sWrNawhaNfiZV2")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Card(BaseModel):
    card_id: int
    word: str
    definition: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    return {"Hello": "World"}
# Auth


@app.post("/v1/login")
def login_user(token: Annotated[str, Depends(oauth2_scheme)]):
    isAuth = auth.verify_id_token(token, check_revoked=True)
    if isAuth:
        return {"name": "someone"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # Cards


@app.get("/v1/cards/{card_id}")
def get_cards(card_id: str):
    pass


@app.post("/v1/cards/")
def create_cards(cards: List[Card]):
    pass


@app.put("/v1/cards/{card_id}")
def update_card(card_id: int, new_card: Card):
    pass


@app.delete("/v1/cards/{card_id}")
def delete_card(card_id: int):

    pass


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
