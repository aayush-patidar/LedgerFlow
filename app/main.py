from fastapi import FastAPI
from .routers import users as users_router, auth as auth_router, wallet as wallet_router, transaction as transaction_router, ledger as ledger_router


from .models import user   # noqa: F401
from .models import wallet # noqa: F401
from .models import transaction # noqa: F401
from .models import ledger # noqa: F401

from .database.database import Base, engine
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router.router)
app.include_router(auth_router.router)
app.include_router(wallet_router.router)
app.include_router(transaction_router.router)
app.include_router(ledger_router.router)