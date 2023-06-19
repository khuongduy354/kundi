from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials
import kundi.routers.user as UserRouter
import kundi.routers.card as CardRouter

# auth setup
cred = credentials.Certificate("private_key.json")
firebase = firebase_admin.initialize_app(cred)


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


app.include_router(UserRouter.router, prefix="/v1")
app.include_router(CardRouter.router, prefix="/v1")


# @app.post("/test_token")
# def test_token(token: Token = Depends(oauth2_scheme)):
#     return token

# Cards


# ROUTE HANDLERS
