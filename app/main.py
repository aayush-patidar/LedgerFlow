from fastapi import FastAPI
from .routers import users, auth
from .routers import wallet as wallet_router
from .routers import transaction as transaction_router
from .routers import ledger as ledger_router

# --- Model imports must come before create_all() so SQLAlchemy knows about all tables ---
from .models import user   # noqa: F401
from .models import wallet # noqa: F401
from .models import transaction # noqa: F401
from .models import ledger # noqa: F401

from .database.database import Base, engine
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(wallet_router.router)
app.include_router(transaction_router.router)
app.include_router(ledger_router.router)