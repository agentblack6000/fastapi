from fastapi import FastAPI

import models
from database import engine

from routes.accounts import router as account_router
from routes.dashboard import router as dashboard_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add the API endpoints
app.include_router(account_router)
app.include_router(dashboard_router)
