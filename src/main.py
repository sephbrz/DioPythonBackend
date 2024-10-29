from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.controllers import user, auth, account, transaction
from src.database import database, engine, metadata
from src.exceptions import (
    AccountNotFoundError,
    BusinessError,
    AuthorizationError,
    TransactionsNotFoundError,
    DatabaseError,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.models.user import userTable
    from src.models.account import accountTable
    from src.models.transaction import transactionTable

    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()


app = FastAPI(
    title="Desafio API Bancária Async com FastAPI",
    version="1.0.0",
    summary="API de um sistema de balanço de conta bancária, com transações de saque e depósito.",
    description="""
Sistema bancário assincrono e autenticado com FastAPI!

## Usuário

Você será capaz de fazer:

* **Criar usuário**.
* **Autenticar com usuário**.

## Conta

Você será capaz de fazer:

* **Criar conta**.

## Transação

Você será capaz de fazer:

* **Realizar transação**.
* **Recuperar transação**.
* **Recuperar transação por ID**.
* **Verificar saldo**.
                """,
    redoc_url=None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, tags=["user"])
app.include_router(auth.router, tags=["auth"])
app.include_router(account.router, tags=["account"])
app.include_router(transaction.router, tags=["transaction"])


@app.exception_handler(AccountNotFoundError)
async def account_not_found_error_handler(request: Request, exc: AccountNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Account not found."}
    )


@app.exception_handler(TransactionsNotFoundError)
async def transaction_not_found_error_handler(
    request: Request, exc: TransactionsNotFoundError
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Transactions not found."},
    )


@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
    )


@app.exception_handler(AuthorizationError)
async def authorization_error_handler(request: Request, exc: AuthorizationError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": str(exc)}
    )


@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
    )
